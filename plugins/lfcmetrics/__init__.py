"""
Set of Nagios probes for testing LFC grid service.

Contains the following Nagios probe:
LFC-probe.

- The probes can run in active and/or passives modes (in Nagios sense).
  Publication of passive test results from inside of probes can be done
  via Nagios command file or NSCA.
- On worker nodes Nagios is used as probes scheduler and executer. Metrics
  results from WNs are sent to Message Broker.

.. packagetree::
   :style: UML
"""

__docformat__ = 'restructuredtext en'
