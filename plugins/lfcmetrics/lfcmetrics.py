##############################################################################
#
# NAME:        lfcmetrics.py
#
# FACILITY:    SAM (Service Availability Monitoring)
#
# COPYRIGHT:
#         Copyright (c) 2009, Members of the EGEE Collaboration.
#         http://www.eu-egee.org/partners/
#         Licensed under the Apache License, Version 2.0.
#         http://www.apache.org/licenses/LICENSE-2.0
#         This software is provided "as is", without warranties
#         or conditions of any kind, either express or implied.
#
# DESCRIPTION:
#
#         LFC metrics.
#
# AUTHORS:     Konstantin Skaburskas, CERN
#
# CREATED:     24-Aug-2010
#
# NOTES:
#
# MODIFIED:
#
##############################################################################

"""
LFC metrics.

LFC metrics.

Konstantin Skaburskas <konstantin.skaburskas@cern.ch>, CERN
SAM (Service Availability Monitoring)
"""

import re
import os
import sys
import time
import signal
import commands

try:
    from gridmon import probe
    from gridmon import utils as samutils
    from threadpool import ThreadPool
    import lfc2 as lfc
except ImportError as e:
    print("UNKNOWN: Error loading modules : %s" % (e))
    sys.exit(3)

class LFCMetrics(probe.MetricGatherer):

    ns = 'org.sam'

    # Cleanup metric
    cleanup_timeout = 60*5
    cleanup_file_ttl = 15*24*3600
    cleanup_files_max = sys.maxint
    cleanup_nthreads = 5
    cleanup_file_names = ['sam-choose-LFC',
                          'sam-nag-choose',
                          'sft-lcg-rm-cr',
                          'sam-lcg-rm-cr',
                          'SRM-put']

    def __init__(self, tuples, lfctype):
        probe.MetricGatherer.__init__(self, tuples, lfctype)

        self.cleanup_dir = '/grid/%s/SAM' % self.voName
        self.usage = """     Metrics specific parameters:

%s.LFC-Cleanup
--cleanup-timeout   <sec>   Cleanup timeout. (Default: %i sec)
--cleanup-dir       <dir>   Directory to clean. (Default: %s)
--cleanup-file-ttl  <hrs>   Time for a file to stay on LFC. (Default: %i hrs)
--cleanup-files-max <num>   Number of files to delete at most before timeout
                            kicks in. (Default: %i)
--cleanup-threads   <num>   Number of cleanup threads. (Default: %i)
""" % (self.ns,
       self.cleanup_timeout,
       self.cleanup_dir,
       self.cleanup_file_ttl/3600,
       self.cleanup_files_max,
       self.cleanup_nthreads)

        self.probeinfo = { 'probeName' : self.ns+'.LFC-probe',
                           'probeVersion' : '0.1',
                           'serviceVersion' : '>= 0.1.1'}
        self._metrics = {
                        'Cleanup' : {
                                'metricDescription' : "Clean test area on LFC",
                                'metricLocality'    : 'remote',
                                'metricType'        : 'status',
                                'metricVersion'     : '0.1',
                                'cmdLineOptions'    : ['cleanup-timeout=',
                                                       'cleanup-dir=',
                                                       'cleanup-file-ttl=',
                                                       'cleanup-files-max=',
                                                       'cleanup-threads=',
                                                       ],
                                'metricChildren'    : []
                                }
                        }

        self.set_metrics(self._metrics)

        self.parse_cmd_args(tuples)

        self.make_workdir()
        self.cleanup_persist_lfns_fn = self.workdir_metric+'/lfns.db'


    def parse_args(self, opts):
        for o,v in opts:
            if o == '--cleanup-timeout':
                self.cleanup_timeout = int(v)
            elif o == '--cleanup-dir':
                self.cleanup_dir = v
            elif o == '--cleanup-file-ttl':
                self.cleanup_file_ttl = int(v)
            elif o == '--cleanup-files-max':
                self.cleanup_files_max = int(v)
            elif o == '--cleanup-threads':
                self.cleanup_nthreads = int(v)
            else:
                pass

    def metricCleanup(self):
        """Cleanup of test area on LFC.

        NOTE:
        Can't use lfc_delfilesbypattern as we need to take into account dates.
        pattern = '(%s)*' % '|'.join(self.cleanup_file_names)
        results = lfc.lfc_delfilesbypattern(self.cleanup_dir, pattern, 0)
        """
        # XXXX: lfc.S_ISDIR is not in lfc2 module. Use this magic number.
        LFC_MAGIC_FILEMODE = 33204

        status = 'OK'
        os.environ['LFC_HOST'] = self.hostName

        def persist_lfns(data):
            import pickle
            fp = open(self.cleanup_persist_lfns_fn, 'w')
            pickle.dump(data, fp)
            fp.close()

        def load_lfns():
            import pickle
            try:
                fp = open(self.cleanup_persist_lfns_fn)
                lfns = pickle.load(fp)
                fp.close()
                return lfns
            except Exception:
                return []

        def del_lfn_file(lfn):
            cmd = 'lcg-del -a %s' % lfn
            rc, out = commands.getstatusoutput(cmd)
            if rc == 0:
                return True
            else:
                if re.search('Permission denied', out, re.M):
                    return False
                elif re.search('No such file or directory', out, re.M):
                    return False
                else:
                    'surl=$(lcg-lr lfn:$1) guid=$(lcg-lg $surl) lcg-uf $guid $surl'
                    cmd = 'lcg-lr %s' % lfn
                    rc, surls = commands.getstatusoutput(cmd)
                    if rc == 0:
                        for surl in surls.strip('\n').split('\n'):
                            cmd = 'lcg-lg %s' % surl
                            rc, guid = commands.getstatusoutput(cmd)
                            if rc != 0:
                                return False
                            else:
                                cmd = 'lcg-uf %s %s' % (guid, surl)
                                rc, _ = commands.getstatusoutput(cmd)
                                if rc != 0:
                                    return False
                    else:
                        return False
                return True

        def del_lfn_dir(dirn):
            cmd = 'lfc-rm -f -r %s' % dirn
            try:
                rc, _ = commands.getstatusoutput(cmd)
            except Exception as e:
                return False
            if rc == 0:
                return True
            else:
                return False

        T_ttl = self.cleanup_file_ttl

        dirname = self.cleanup_dir
        fnames_re = re.compile('|'.join(self.cleanup_file_names))

        dir_pt = lfc.lfc_opendir(dirname)
        if not dir_pt:
            self.prints("Couldn't open %s" % dirname)
            return 'UNKNOWN'

        global pool, tasks
        tasks = []
        pool = ThreadPool(self.cleanup_nthreads)
        def sighandler(a, b):
            global pool, tasks
            self.printd('caught signal: %s' % samutils.time_now())
            tasks = pool.dropAll()
            while 1:
                if pool.getThreadCount() == 0 and pool.getTasksCount() == 0:
                    break
                time.sleep(.5)
        signal.signal(signal.SIGALRM, sighandler)
        signal.alarm(self.cleanup_timeout)
        self.printd('set timeout for %i sec' % self.cleanup_timeout)

        i_tot = 0
        i_match_name = 0
        i_match_all = 0

        global i_deleted
        i_deleted = 0
        def task_callback(val):
            global i_deleted
            i_deleted += val and 1 or 0

        t_start = time.time()
        t_stop  = t_start + self.cleanup_timeout

        self.printd('initialised: %s' % samutils.time_now())
        lfns_loaded = load_lfns()
        if lfns_loaded:
            self.printd("loaded %i lfns from previous run" % len(lfns_loaded))
            i_tot += len(lfns_loaded)
            for i,lfn in enumerate(lfns_loaded[:]):
                if lfn.startswith('lfn'):
                    pool.enqueueTask(del_lfn_file, lfn, task_callback)
                else:
                    pool.enqueueTask(del_lfn_dir, lfn, task_callback)
                    lfns_loaded[i] = 'lfn:%s' % lfn

        # first, clear 2/3 of the cache, then proceed further
        lfns_len_stop = len(lfns_loaded) / 3
        while pool.getTasksCount() > lfns_len_stop and time.time() < t_stop:
            time.sleep(2)

        while i_deleted <= self.cleanup_files_max and time.time() < t_stop:
            entry = lfc.lfc_readdirx(dir_pt)
            if not entry:
                self.printd("no more files to delete")
                break
            self.printdvm("file: %s" % entry.d_name)
            if fnames_re.match(entry.d_name):
                e_fullname = '%s/%s' % (dirname, entry.d_name)
                lfn = 'lfn:%s' % e_fullname
                if lfn in lfns_loaded:
                    self.printdvm("already in local cache %s" % entry.d_name)
                    continue
                if entry.mtime < time.time() - T_ttl:
                    self.printdvm("match name&time: %s" % entry.d_name)
                    i_match_all += 1
                    if entry.filemode == LFC_MAGIC_FILEMODE:
                        # assume this is a file
                        pool.enqueueTask(del_lfn_file, lfn, task_callback)
                    else:
                        # this is a directory
                        pool.enqueueTask(del_lfn_dir, e_fullname, task_callback)
                else:
                    self.printdvm("match name: %s" % entry.d_name)
                i_match_name += 1
            else:
                self.printdvm("not matched: %s" % entry.d_name)
            i_tot += 1

        self.printd('finished processing: %s' % samutils.time_now())

        if len(tasks) == 0:
            tasks = pool.delTasks()

        pool.joinAll(waitForTasks=False, waitForThreads=False)

        self.printd('done with cleanup for now: time spent %i sec' % \
                        (time.time() - t_start))
        if len(tasks) > 0:
            self.printd('persisting %i unprocessed lfns' % len(tasks))
            persist_lfns([x[1] for x in tasks[:]])
        else:
            try:
                os.unlink(self.cleanup_persist_lfns_fn)
            except Exception: pass

        self.printd("total %i" % i_tot)
        self.printd("match name&time %i" % i_match_all)
        self.printd("match name %i" % i_match_name)
        self.printd("deleted %i" % i_deleted)

        self.prints('total %i, match name&time %i, match name %i, deleted %i' % \
                    (i_tot, i_match_all, i_match_name, i_deleted,))
        return status
