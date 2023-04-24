K8S_VERSION=v1.27.1
RELEASE=0

.PHONY: rpm-repo
rpm-repo:
	createrepo -v ./repo && \
	podman stop packages-repo --ignore && \
	podman run -d --rm \
	-v ./repo:/usr/share/nginx/repo \
	-v ./nginx.conf:/etc/nginx/nginx.conf \
	--security-opt label=disable \
	-p 8080:80 \
	--name packages-repo \
	nginx

.PHONY: kube-images
kube-images: images-exports
	cd kube-images && \
	mock --clean -r rocky-8-x86_64 --spec=./kube-images.spec --sources=. --resultdir=./mock/SRPM --buildsrpm && \
	mock --clean -r rocky-8-x86_64 --resultdir=./mock/RPM --rebuild ./mock/SRPM/kube-images-$(K8S_VERSION)-$(RELEASE).src.rpm && \
	cp -R ./mock/RPM/kube-images-$(K8S_VERSION)-$(RELEASE).noarch.rpm ../repo

.PHONY: images-exports
images-exports:
ifeq (,$(wildcard kube-images/kube-images:$(K8S_VERSION)))
	ctr image pull registry.k8s.io/kube-apiserver:$(K8S_VERSION) && \
	ctr image pull registry.k8s.io/kube-controller-manager:$(K8S_VERSION) && \
	ctr image pull registry.k8s.io/kube-scheduler:$(K8S_VERSION) && \
	ctr image pull registry.k8s.io/kube-proxy:$(K8S_VERSION) && \
	ctr image pull registry.k8s.io/pause:3.9 && \
	ctr image pull registry.k8s.io/etcd:3.5.7-0 && \
	ctr image pull registry.k8s.io/coredns/coredns:v1.10.1 && \
	ctr image export kube-images/kube-images:$(K8S_VERSION) \
	registry.k8s.io/kube-apiserver:$(K8S_VERSION) \
	registry.k8s.io/kube-controller-manager:$(K8S_VERSION) \
	registry.k8s.io/kube-scheduler:$(K8S_VERSION) \
	registry.k8s.io/kube-proxy:$(K8S_VERSION) \
	registry.k8s.io/pause:3.9 \
	registry.k8s.io/etcd:3.5.7-0 \
	registry.k8s.io/coredns/coredns:v1.10.1
	chmod 0777 kube-images/kube-images:$(K8S_VERSION)
endif

.PHONY: machine-id-hostname
machine-id-hostname:
	cd machine-id-hostname && \
	mock --clean -r rocky-8-x86_64 --spec=./machine-id-hostname.spec --sources=. --resultdir=mock/SRPM --buildsrpm && \
	mock --clean -r rocky-8-x86_64 --resultdir=mock/RPM --rebuild mock/SRPM/machine-id-hostname-v0.0.1-0.src.rpm && \
	cp -R ./mock/RPM/machine-id-hostname-v0.0.1-0.noarch.rpm ../repo