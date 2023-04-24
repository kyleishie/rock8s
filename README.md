![Rock8s Linux](docs/images/Rock8s.png "Rock8s Linux")

# Rock8s Linux
This repo contains the rpm-ostree configuration for a k8s focused spin of Rocky Linux OSTree.

## What's in the box?
- Vanilla k8s (containerd, kubelet, kubeadm, kubectl)
- flannel cni (see Flannel section for details)
- Almost everything included in Rocky 8 Minimal
- RPM-OSTree
- Bundled offline images - Machines can be provisioned without internet access. 

## CNI - Flannel
[flannel v0.21.4](https://github.com/flannel-io/flannel/releases/tag/v0.21.4) is employed as the cluster CNI. There are a 
few subtle changes needed for flannel to work with ostree, however.

The first change we make is to disable the `install-cni-plugin` init container because it will fail to write `/opt/cni/bin/flannel`.
This happens because `/opt/cni` is linked to `/usr/lib/opt/cni` which is read only at runtime.  To mimic this behavior, 
we run the init container at compose time, copy out the flannel binary, and place it in `/usr/lib/opt/cni`.

In order to make sure that `install-cni-plugin` init container isn't reintroduced we also bundle a modified manifest at 
`/usr/kube-flannel.yaml`.  The only different between this manifest and that available from flannel's GitHub is the removal
if the `install-cni-plugin` init container.  **Note that the location of this manifest is subject to change.**

**We will enable other CNIs in the future.**


## Setup K8S
#### Control Plane Node
Run the following commands.  **Do not change the ip address**
```
kubeadm init --pod-network-cidr=10.244.0.0/16
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl apply -f /usr/kube-flannel.yaml
```

If you wish your control plane node to accept any work deployed to the cluster run the following:
```
kubectl taint node $(hostname) node-role.kubernetes.io/control-plane- 
```


#### Worker Nodes
On the control-plane node run the following:
```
kubeadm token create --print-join-command
```

Run the output command on your worker nodes.
```
kubeadm join 172.16.61.15:6443 --token blah.blahblahblah  --discovery-token-ca-cert-hash sha256:blahblahblah
```

## Upgrading your installation
Rock8s is an RPM-OSTree based system. If you are not familiar with what that means it is recommended that you read the 
[ostree documentation](https://ostreedev.github.io/ostree/) as well as the 
[rpm-ostree documentation](https://coreos.github.io/rpm-ostree/).  The **most important** thing to read and understand is 
[ RPM-OSTree Client Administration](https://coreos.github.io/rpm-ostree/administrator-handbook/).

### Reference Commands
Upgrade your deployment.
```
rpm-ostree upgrade --reboot
```

Rebase to a new version.
```
rpm-ostree rebase -b rock8s:rock8s/x86_64/v1.27.1-devel --reboot
```

Rollback to previous deployment.
```
rpm-ostree rollback --reboot
```


## TODOs
### Must Have List
- [ ] Bundle flannel images for version
- [ ] Automatically Apply kube-flannel.yaml
- [ ] Automate version setup (downloading flannel bin and daemonset manifest)

### Nice to Have List
- [ ] Rocky 9
- [ ] Support Other architectures
  - Automatically taint arch?
- [ ] Cilium
- [ ] Calico
- [ ] default ingress?
- [ ] setup convenience scripts/cli:
  - Easy config retrieval
  - Easy control plane setup based on settings, e.g., selected cni.
- [ ] Remote rpm-ostree management

