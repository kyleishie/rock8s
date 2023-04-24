%global	package_version v0.0.1

Name: machine-id-hostname
Summary:	Sets hostname to /etc/machine-id unless otherwise set.
Version:	%{package_version}
Release:    0
Group:		System Environment/Base
License:	Apache V2
BuildArch:  noarch

Requires:	hostname
Requires:	systemd
Requires:   grep

%description

%install

# install systemd unit to ctr image import on boot
# FIXME: This isn't working
mkdir -p %{buildroot}/usr/lib/systemd/system/
cat << EOF >>%{buildroot}/usr/lib/systemd/system/machine-id-hostname.service
[Unit]
Description=Sets hostname to /etc/machine-id unless otherwise set.
Requires=systemd-machine-id-commit.service
Before=kubelet.service
ConditionPathExists=/etc/machine-id

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash -c "hostnamectl --static | grep 'localhost.localdomain' && hostnamectl set-hostname node-$(cat /etc/machine-id)"

[Install]
WantedBy=multi-user.target
EOF

%files
%attr(0444, root, root) /usr/lib/systemd/system/machine-id-hostname.service
