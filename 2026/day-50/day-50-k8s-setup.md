# Day 50 – Kubernetes: Architecture, Cluster Setup, and First Commands

## Why Kubernetes Exists

Docker solved the "how do I run this container" problem. But the moment you have 50 containers across 10 servers, Docker alone doesn't know what to do. Which server has capacity? What happens when a container crashes at 2 am? How do services find each other?

Kubernetes — originally built at Google, based on their internal system called Borg — was open-sourced in 2014 to answer exactly those questions. The name comes from the Greek word for "helmsman" or "pilot." The K8S shorthand comes from the 8 letters between K and s. Google had been running containerised workloads in production for years before Kubernetes existed, and they essentially packaged that experience into an open-source project.

You tell Kubernetes *what you want* — 3 replicas of this app, always — and it figures out the how, and keeps it that way even if servers die.

---

## Kubernetes Architecture

### Control Plane (the brain)

**API Server** — every single kubectl command hits this first. Nothing in the cluster bypasses it. It's the front door.

**etcd** — a key-value store that holds the entire cluster state. If etcd goes down, the cluster goes blind. Nothing gets created or deleted until it's back.

**Scheduler** — When a new pod needs to run, the scheduler looks at all the nodes, checks their available CPU and memory, and picks the best fit.

**Controller Manager** — this is what watches the cluster constantly. If you said "I want 3 replicas" and one pod dies, the controller manager is what notices and tells the API server to spin up a replacement.

### Worker Nodes (where workloads actually run)

**kubelet** — the agent sitting on every worker node. It talks to the API server and makes sure the pods that are supposed to be on that node are actually running.

**kube-proxy** — handles the networking rules. Every time a pod needs to reach another pod or service, kube-proxy is what makes that routing work.

**Container Runtime** — the actual engine running the containers. In modern clusters, this is usually `containerd` or `CRI-O`. Docker used to be here, but Kubernetes dropped direct Docker support a while back.

### What happens when you run `kubectl apply -f pod.yaml`?

1. kubectl sends the request to the **API Server**
2. API Server validates it and writes the desired state to **etcd**
3. The **Scheduler** sees the unscheduled pod and picks a node
4. The **kubelet** on that node gets the instruction and pulls the image
5. The container starts running via the **container runtime**

If the API server goes down, nothing new can be created or modified, but existing pods keep running. The cluster isn't dead; it just can't accept any changes.

If a worker node goes down, the controller manager notices the pods on that node are gone and reschedules them to healthy nodes.

---

## Tool Choice: kind

I went with **kind** (Kubernetes in Docker). The main reason: it works inside WSL without needing a separate VM. Minikube may need a hypervisor driver depending on your setup, and that adds friction. With kind, as long as Docker is running, you're good.

I used a `config.yml` to create a multi-node cluster instead of the default single-node — one control plane and three workers. More realistic setup for actually practising scheduling and node behaviour.

```yaml
# config.yml used to create the cluster
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
  - role: worker
```

---

## Cluster Setup

### Local cluster (WSL)

```bash
kind create cluster --config config.yml --name demo-cluster
```

**kubectl get nodes output:**

```
NAME                        STATUS   ROLES           AGE     VERSION
demo-cluster-control-plane  Ready    control-plane   2m28s   v1.35.0
demo-cluster-worker         Ready    <none>          2m10s   v1.35.0
demo-cluster-worker2        Ready    <none>          2m10s   v1.35.0
demo-cluster-worker3        Ready    <none>          2m10s   v1.35.0
```

*(Screenshot: Image 1 — `kubectl get nodes` showing all 4 nodes Ready)*

---

### EC2 cluster (Ubuntu)

Ran a separate kind cluster on an EC2 instance to practice in a real Linux environment — not just WSL.

```
NAME                       STATUS   ROLES           AGE     VERSION
my-cluster-control-plane   Ready    control-plane   5d20h   v1.31.2
my-cluster-worker          Ready    <none>          5d19h   v1.31.2
my-cluster-worker2         Ready    <none>          5d19h   v1.31.2
my-cluster-worker3         Ready    <none>          5d19h   v1.31.2
```

*(Screenshot: Image 4 — nodes + full kube-system pod list)*

---

## kube-system Pods Explained

```bash
kubectl get pods -n kube-system
```

Here's what's actually running there and what each one does:

| Pod | What it does |
|---|---|
| `kube-apiserver-*` | The API server — every request goes through this |
| `etcd-*` | Cluster database — stores all state |
| `kube-scheduler-*` | Decides which node a pod runs on |
| `kube-controller-manager-*` | Watches cluster state, runs reconciliation loops |
| `coredns-*` (2 pods) | DNS inside the cluster — pods use this to find each other by service name |
| `kube-proxy-*` (one per node) | Networking rules on each node |
| `kindnet-*` (one per node) | kind's CNI — handles pod-to-pod networking across nodes |

The fact that etcd, the API server, scheduler, and controller manager all show up here as actual running pods is the thing that clicked for me. The control plane isn't some separate magical thing — it's pods, just like everything else. They just happen to run in a dedicated namespace.

---

## Namespaces

```bash
kubectl get ns
```

```
NAME               STATUS   AGE
default            Active   8h
kube-node-lease    Active   8h
kube-public        Active   8h
kube-system        Active   8h
local-path-storage Active   8h
nginx-ns           Active   21s
```

`nginx-ns` is a custom namespace I created to practice isolating workloads.

```bash
kubectl apply -f namespace.yml
kubectl config set-context --current --namespace=nginx-ns
```

Switching the default namespace in context means you don't have to add `-n nginx-ns` to every command. It saves keystrokes but can also catch you off guard when you forget you're not in `default` anymore.

---

## What is a kubeconfig?

kubeconfig is the file kubectl uses to know *which cluster to talk to* and *who you are*. It stores cluster addresses, credentials (certificates), and contexts.

Default location: `~/.kube/config`

```bash
kubectl config current-context   # shows which cluster you're connected to
kubectl config get-contexts      # lists all available clusters/contexts
kubectl config view              # shows the full file (with secrets omitted)
```

A context ties together three things: a cluster, a user, and a namespace. When I ran `set-context --current --namespace=nginx-ns`, I modified the existing context to point at nginx-ns by default — I didn't create a new context.

*(Screenshot: Image 5 — `kubectl config view` showing kind-my-cluster context with nginx-ns)*

---

## Key Commands from Today

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes
kubectl get nodes -o wide

# Explore all running pods across the cluster
kubectl get pods -A

# kube-system specifically
kubectl get pods -n kube-system

# Namespace operations
kubectl get ns
kubectl apply -f namespace.yml
kubectl config set-context --current --namespace=<name>

# kubeconfig
kubectl config current-context
kubectl config get-contexts
kubectl config view

# Cluster lifecycle
kind create cluster --config config.yml --name demo-cluster
kind delete cluster --name demo-cluster
Kind get clusters
```

---

## What I Actually Ran Today

Across both environments (WSL + EC2), I:

- Created kind clusters using a custom `config.yml` with 1 control plane + 3 workers
- Ran `kubectl get nodes`, `kubectl cluster-info`, `kubectl get pods -A`
- Matched every pod in `kube-system` to its architecture component
- Created a custom namespace (`nginx-ns`) and switched the context to it
- Deployed a `two-tier-app` pod and verified it was running
- Explored `kubectl config view` and understood the kubeconfig structure

Day 50 done. The orchestration chapter is open.

---

`#90DaysOfDevOps` `#DevOpsKaJosh` `#TrainWithShubham`


![alt text](k8s_architecture_full_communication.svg)

