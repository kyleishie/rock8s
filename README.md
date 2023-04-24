![Rock8s Linux](docs/images/Rock8s.png "Rock8s Linux")

# Rock8s Linux 
This repo contains the rpm-ostree configuration for a k8s focused spin of Rocky Linux OSTree.

## Whats in the box?
- Vanilla k8s (containerd, kubelet, kubeadm, kubectl)
- kubectl bash completion
- flannel cni (see Flannel section for details)
- Almost everything included in Rocky 8 Minimal
- RPM-OSTree0

# CNI - Flannel


# How To
- No swap
- Set hostname

## Must Have List
- [x] Bundle kubeadm config images for version
- [ ] Bundle flannel images for version
- [ ] Automatically Apply kube-flannel.yaml
- [ ] Automate version setup (downloading flannel bin and daemonset manifest)
- [ ] randomize hostname when not set.  Maybe an oneshot service to check for localhost.localdomain then `hostnamectl set-hostname $(uuidgen)` 
- [ ] generate ISO
- [ ] test join workers

## Nice to Have List
- [ ] Rocky 9
- [ ] Support Other architectures
  - Automatically taint arch?

## Maybe List
- [ ] Cilium instead of Flannel
- [ ] default ingress?
- [ ] setup convenience scripts/cli:
  - Easy config retrieval
    - mkdir -p $HOME/.kube
    - sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    - sudo chown $(id -u):$(id -g) $HOME/.kube/config
  - Easy control plane setup based on settings, e.g., selected cni.

