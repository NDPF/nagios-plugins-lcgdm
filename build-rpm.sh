#!/bin/bash

VERSION='0.9.7'
RELEASE='2'

tar --transform "s,^.,nagios-plugins-lcgdm-${VERSION}," -czvf ~/rpmbuild/SOURCES/nagios-plugins-lcgdm-${VERSION}.tar.gz .
rpmbuild -bb --define "__version ${VERSION}" --define "__release ${RELEASE}" dist/nagios-plugins-lcgdm.spec
