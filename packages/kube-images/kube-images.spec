%global	package_version v1.27.1

Name: kube-images
Summary:	The images needed by kubeadm to start a cluster.
Version:	%{package_version}
Release:	0
Group:		System Environment/Base
License:	Apache V2
BuildArch:  noarch

Source201: kube-images:%{package_version}

Requires:	containerd
Requires:	systemd
Requires:   grep

%description
Prefetched copies of the images needed by kubeadm to start a cluster.  The purpose of this package
is to allow distros like Rock8s to embed the images instead of allowing pull at runtime.

%install
mkdir -p %{buildroot}/usr/content
install -m 0444 -t %{buildroot}/usr/content %{SOURCE201}

# install systemd unit to ctr image import on boot
mkdir -p %{buildroot}/usr/lib/systemd/system/
cat << EOF >>%{buildroot}/usr/lib/systemd/system/kube-images.service
[Unit]
Description=Imports images needed by kubeadm (replaces kubeadm config images pull)
Requires = containerd.service
Before=kubelet.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash -c "ctr -n=k8s.io image check --quiet | grep "registry.k8s.io/kube-apiserver:%{package_version}" || ctr -n=k8s.io image import /usr/content/kube-images:%{package_version}"

[Install]
WantedBy=multi-user.target
EOF

%files
%attr(0444, root, root) /usr/content/kube-images:%{package_version}
%attr(0444, root, root) /usr/lib/systemd/system/kube-images.service
