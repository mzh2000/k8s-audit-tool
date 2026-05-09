# 🔒 Kubernetes 集群安全审计报告

## 📋 报告概览

- **报告生成时间**: 2026-05-09 15:38:34
- **审计工具**: K8s 权限审计小工具 v1.0
- **审计范围**: 所有 RoleBinding 和 ClusterRoleBinding
- **审计对象**: 所有 ServiceAccount 的权限绑定

## 📊 风险统计摘要

| 风险等级 | 数量 | 说明 |
|---------|------|------|
| 🔴 高风险 | 4 | 非系统 ServiceAccount 绑定了高风险角色（如 cluster-admin） |
| 🟡 中风险 | 1 | 系统 ServiceAccount 绑定了高风险角色（需确认必要性） |
| 🟢 低风险 | 136 | ServiceAccount 绑定了普通角色，权限在合理范围内 |
| **总计** | **141** | 所有 ServiceAccount 绑定总数 |

## 🔴 高风险条目

> ⚠️ 以下 ServiceAccount 绑定了高风险角色，且不属于系统 Namespace，建议立即审查并降低权限。

| 名称空间 | 绑定名称 | 绑定类型 | 角色名称 | ServiceAccount | 风险等级 | 说明 |
|---------|---------|---------|---------|---------------|---------|------|
| cluster-wide | kuboard-admin-crb | ClusterRoleBinding | cluster-admin | kuboard/kuboard-admin | 🔴 高风险 | 非系统 ServiceAccount 'kuboard-admin' 通过 ClusterRoleBinding 绑定了高风险角色 'cluster-admin'，可能拥有过大的集群权限 |
| cluster-wide | kuboard-boostrap-crb | ClusterRoleBinding | cluster-admin | kuboard/kuboard-boostrap | 🔴 高风险 | 非系统 ServiceAccount 'kuboard-boostrap' 通过 ClusterRoleBinding 绑定了高风险角色 'cluster-admin'，可能拥有过大的集群权限 |
| cluster-wide | rancher | ClusterRoleBinding | cluster-admin | cattle-system/rancher | 🔴 高风险 | 非系统 ServiceAccount 'rancher' 通过 ClusterRoleBinding 绑定了高风险角色 'cluster-admin'，可能拥有过大的集群权限 |
| cluster-wide | rancher-webhook | ClusterRoleBinding | cluster-admin | cattle-system/rancher-webhook | 🔴 高风险 | 非系统 ServiceAccount 'rancher-webhook' 通过 ClusterRoleBinding 绑定了高风险角色 'cluster-admin'，可能拥有过大的集群权限 |

## 🟡 中风险条目

> ℹ️ 以下系统 ServiceAccount 绑定了高风险角色，通常是集群组件正常运行所需，建议确认其必要性。

| 名称空间 | 绑定名称 | 绑定类型 | 角色名称 | ServiceAccount | 风险等级 | 说明 |
|---------|---------|---------|---------|---------------|---------|------|
| cluster-wide | velero | ClusterRoleBinding | cluster-admin | velero/velero | 🟡 中风险 | 系统 ServiceAccount 'velero' 绑定了高风险角色 'cluster-admin'，请确认是否为必要权限 |

## 🟢 低风险条目

> ✅ 以下 ServiceAccount 的权限绑定在合理范围内，属于正常使用场景。

| 名称空间 | 绑定名称 | 绑定类型 | 角色名称 | ServiceAccount | 风险等级 | 说明 |
|---------|---------|---------|---------|---------------|---------|------|
| cattle-fleet-clusters-system | import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321-creds | RoleBinding | import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321-creds | fleet-local/import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321 | 🟢 低风险 | ServiceAccount 'import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321' 绑定了角色 'import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321-creds'，权限在合理范围内 |
| cattle-fleet-system | fleet-controller | RoleBinding | fleet-controller | cattle-fleet-system/fleet-controller | 🟢 低风险 | ServiceAccount 'fleet-controller' 绑定了角色 'fleet-controller'，权限在合理范围内 |
| cattle-fleet-system | gitjob | RoleBinding | gitjob | cattle-fleet-system/gitjob | 🟢 低风险 | ServiceAccount 'gitjob' 绑定了角色 'gitjob'，权限在合理范围内 |
| cluster-fleet-local-local-1a3d67d0a899 | request-fv2kf | RoleBinding | fleet-bundle-deployment | cluster-fleet-local-local-1a3d67d0a899/request-fv2kf-aa226cb6-862d-402c-a9a4-37717cb23b8a | 🟢 低风险 | ServiceAccount 'request-fv2kf-aa226cb6-862d-402c-a9a4-37717cb23b8a' 绑定了角色 'fleet-bundle-deployment'，权限在合理范围内 |
| fleet-local | import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321-to-role | RoleBinding | import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321-role | fleet-local/import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321 | 🟢 低风险 | ServiceAccount 'import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321' 绑定了角色 'import-token-local-47347215-aa4e-49d7-b8f5-4eca1c028321-role'，权限在合理范围内 |
| fleet-local | request-fv2kf | RoleBinding | request-fv2kf | cluster-fleet-local-local-1a3d67d0a899/request-fv2kf-aa226cb6-862d-402c-a9a4-37717cb23b8a | 🟢 低风险 | ServiceAccount 'request-fv2kf-aa226cb6-862d-402c-a9a4-37717cb23b8a' 绑定了角色 'request-fv2kf'，权限在合理范围内 |
| istio-ingress | istio-ingressgateway | RoleBinding | istio-ingressgateway | istio-ingress/istio-ingressgateway | 🟢 低风险 | ServiceAccount 'istio-ingressgateway' 绑定了角色 'istio-ingressgateway'，权限在合理范围内 |
| istio-system | istiod | RoleBinding | istiod | istio-system/istiod | 🟢 低风险 | 正常权限绑定 |
| istio-system | istiod-istio-system | RoleBinding | istiod-istio-system | istio-system/istiod-service-account | 🟢 低风险 | 正常权限绑定 |
| kube-public | system:controller:bootstrap-signer | RoleBinding | system:controller:bootstrap-signer | kube-system/bootstrap-signer | 🟢 低风险 | 正常权限绑定 |
| kube-system | keda-operator-auth-reader | RoleBinding | extension-apiserver-authentication-reader | keda/keda-operator | 🟢 低风险 | ServiceAccount 'keda-operator' 绑定了角色 'extension-apiserver-authentication-reader'，权限在合理范围内 |
| kube-system | leader-locking-nfs-client-provisioner | RoleBinding | leader-locking-nfs-client-provisioner | kube-system/nfs-client-provisioner | 🟢 低风险 | 正常权限绑定 |
| kube-system | system::leader-locking-kube-controller-manager | RoleBinding | system::leader-locking-kube-controller-manager | kube-system/kube-controller-manager | 🟢 低风险 | 正常权限绑定 |
| kube-system | system::leader-locking-kube-scheduler | RoleBinding | system::leader-locking-kube-scheduler | kube-system/kube-scheduler | 🟢 低风险 | 正常权限绑定 |
| kube-system | system:controller:bootstrap-signer | RoleBinding | system:controller:bootstrap-signer | kube-system/bootstrap-signer | 🟢 低风险 | 正常权限绑定 |
| kube-system | system:controller:cloud-provider | RoleBinding | system:controller:cloud-provider | kube-system/cloud-provider | 🟢 低风险 | 正常权限绑定 |
| kube-system | system:controller:token-cleaner | RoleBinding | system:controller:token-cleaner | kube-system/token-cleaner | 🟢 低风险 | 正常权限绑定 |
| metallb-system | controller | RoleBinding | controller | metallb-system/controller | 🟢 低风险 | 正常权限绑定 |
| metallb-system | pod-lister | RoleBinding | pod-lister | metallb-system/speaker | 🟢 低风险 | 正常权限绑定 |
| monitoring | kube-prometheus-stack-admission | RoleBinding | kube-prometheus-stack-admission | monitoring/kube-prometheus-stack-admission | 🟢 低风险 | ServiceAccount 'kube-prometheus-stack-admission' 绑定了角色 'kube-prometheus-stack-admission'，权限在合理范围内 |
| monitoring | kube-prometheus-stack-grafana | RoleBinding | kube-prometheus-stack-grafana | monitoring/kube-prometheus-stack-grafana | 🟢 低风险 | ServiceAccount 'kube-prometheus-stack-grafana' 绑定了角色 'kube-prometheus-stack-grafana'，权限在合理范围内 |
| postgresql | pg-cluster | RoleBinding | pg-cluster | postgresql/pg-cluster | 🟢 低风险 | ServiceAccount 'pg-cluster' 绑定了角色 'pg-cluster'，权限在合理范围内 |
| cluster-wide | calico-kube-controllers | ClusterRoleBinding | calico-kube-controllers | kube-system/calico-kube-controllers | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | calico-node | ClusterRoleBinding | calico-node | kube-system/calico-node | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | cattle-fleet-local-system-fleet-agent-role-binding | ClusterRoleBinding | cattle-fleet-local-system-fleet-agent-role | cattle-fleet-local-system/fleet-agent | 🟢 低风险 | ServiceAccount 'fleet-agent' 绑定了角色 'cattle-fleet-local-system-fleet-agent-role'，权限在合理范围内 |
| cluster-wide | cattle-impersonation-u-b4qkhsnliz | ClusterRoleBinding | cattle-impersonation-u-b4qkhsnliz | cattle-impersonation-system/cattle-impersonation-u-b4qkhsnliz | 🟢 低风险 | ServiceAccount 'cattle-impersonation-u-b4qkhsnliz' 绑定了角色 'cattle-impersonation-u-b4qkhsnliz'，权限在合理范围内 |
| cluster-wide | cattle-impersonation-u-mo773yttt4 | ClusterRoleBinding | cattle-impersonation-u-mo773yttt4 | cattle-impersonation-system/cattle-impersonation-u-mo773yttt4 | 🟢 低风险 | ServiceAccount 'cattle-impersonation-u-mo773yttt4' 绑定了角色 'cattle-impersonation-u-mo773yttt4'，权限在合理范围内 |
| cluster-wide | cnpg-manager-rolebinding | ClusterRoleBinding | cnpg-manager | cnpg-system/cnpg-manager | 🟢 低风险 | ServiceAccount 'cnpg-manager' 绑定了角色 'cnpg-manager'，权限在合理范围内 |
| cluster-wide | fleet-controller | ClusterRoleBinding | fleet-controller | cattle-fleet-system/fleet-controller | 🟢 低风险 | ServiceAccount 'fleet-controller' 绑定了角色 'fleet-controller'，权限在合理范围内 |
| cluster-wide | fleet-controller-bootstrap | ClusterRoleBinding | fleet-controller-bootstrap | cattle-fleet-system/fleet-controller-bootstrap | 🟢 低风险 | ServiceAccount 'fleet-controller-bootstrap' 绑定了角色 'fleet-controller-bootstrap'，权限在合理范围内 |
| cluster-wide | gitjob-binding | ClusterRoleBinding | gitjob | cattle-fleet-system/gitjob | 🟢 低风险 | ServiceAccount 'gitjob' 绑定了角色 'gitjob'，权限在合理范围内 |
| cluster-wide | haproxy-assistvoice-binding | ClusterRoleBinding | haproxy-ingress | haproxy-ingress-controller/haproxy-assistvoice | 🟢 低风险 | ServiceAccount 'haproxy-assistvoice' 绑定了角色 'haproxy-ingress'，权限在合理范围内 |
| cluster-wide | istio-reader-clusterrole-istio-system | ClusterRoleBinding | istio-reader-clusterrole-istio-system | istio-system/istio-reader-service-account | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | istio-reader-istio-system | ClusterRoleBinding | istio-reader-istio-system | istio-system/istio-reader-service-account | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | istiod-clusterrole-istio-system | ClusterRoleBinding | istiod-clusterrole-istio-system | istio-system/istiod | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | istiod-gateway-controller-istio-system | ClusterRoleBinding | istiod-gateway-controller-istio-system | istio-system/istiod | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | istiod-istio-system | ClusterRoleBinding | istiod-istio-system | istio-system/istiod-service-account | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | keda-operator | ClusterRoleBinding | keda-operator | keda/keda-operator | 🟢 低风险 | ServiceAccount 'keda-operator' 绑定了角色 'keda-operator'，权限在合理范围内 |
| cluster-wide | keda-operator-hpa-controller-external-metrics | ClusterRoleBinding | keda-operator-external-metrics-reader | kube-system/horizontal-pod-autoscaler | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | keda-operator-system-auth-delegator | ClusterRoleBinding | system:auth-delegator | keda/keda-operator | 🟢 低风险 | ServiceAccount 'keda-operator' 绑定了角色 'system:auth-delegator'，权限在合理范围内 |
| cluster-wide | kube-prometheus-stack-admission | ClusterRoleBinding | kube-prometheus-stack-admission | monitoring/kube-prometheus-stack-admission | 🟢 低风险 | ServiceAccount 'kube-prometheus-stack-admission' 绑定了角色 'kube-prometheus-stack-admission'，权限在合理范围内 |
| cluster-wide | kube-prometheus-stack-grafana-clusterrolebinding | ClusterRoleBinding | kube-prometheus-stack-grafana-clusterrole | monitoring/kube-prometheus-stack-grafana | 🟢 低风险 | ServiceAccount 'kube-prometheus-stack-grafana' 绑定了角色 'kube-prometheus-stack-grafana-clusterrole'，权限在合理范围内 |
| cluster-wide | kube-prometheus-stack-kube-state-metrics | ClusterRoleBinding | kube-prometheus-stack-kube-state-metrics | monitoring/kube-prometheus-stack-kube-state-metrics | 🟢 低风险 | ServiceAccount 'kube-prometheus-stack-kube-state-metrics' 绑定了角色 'kube-prometheus-stack-kube-state-metrics'，权限在合理范围内 |
| cluster-wide | kube-prometheus-stack-operator | ClusterRoleBinding | kube-prometheus-stack-operator | monitoring/kube-prometheus-stack-operator | 🟢 低风险 | ServiceAccount 'kube-prometheus-stack-operator' 绑定了角色 'kube-prometheus-stack-operator'，权限在合理范围内 |
| cluster-wide | kube-prometheus-stack-prometheus | ClusterRoleBinding | kube-prometheus-stack-prometheus | monitoring/kube-prometheus-stack-prometheus | 🟢 低风险 | ServiceAccount 'kube-prometheus-stack-prometheus' 绑定了角色 'kube-prometheus-stack-prometheus'，权限在合理范围内 |
| cluster-wide | kuboard-viewer-crb | ClusterRoleBinding | view | kuboard/kuboard-viewer | 🟢 低风险 | ServiceAccount 'kuboard-viewer' 绑定了角色 'view'，权限在合理范围内 |
| cluster-wide | local-path-provisioner-bind | ClusterRoleBinding | local-path-provisioner-role | local-path-storage/local-path-provisioner-service-account | 🟢 低风险 | ServiceAccount 'local-path-provisioner-service-account' 绑定了角色 'local-path-provisioner-role'，权限在合理范围内 |
| cluster-wide | metallb-system:controller | ClusterRoleBinding | metallb-system:controller | metallb-system/controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | metallb-system:speaker | ClusterRoleBinding | metallb-system:speaker | metallb-system/speaker | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | pod-impersonation-helm-op-2lvjl | ClusterRoleBinding | pod-impersonation-helm-op-xbmt9 | cattle-system/pod-impersonation-helm-op-jhd5n | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-jhd5n' 绑定了角色 'pod-impersonation-helm-op-xbmt9'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-2nbc5 | ClusterRoleBinding | pod-impersonation-helm-op-47lxx | cattle-system/pod-impersonation-helm-op-mhdd4 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-mhdd4' 绑定了角色 'pod-impersonation-helm-op-47lxx'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-4rxrg | ClusterRoleBinding | pod-impersonation-helm-op-fhrpq | cattle-system/pod-impersonation-helm-op-5ktww | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-5ktww' 绑定了角色 'pod-impersonation-helm-op-fhrpq'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-5kst2 | ClusterRoleBinding | pod-impersonation-helm-op-v8l6c | cattle-system/pod-impersonation-helm-op-2ctbv | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-2ctbv' 绑定了角色 'pod-impersonation-helm-op-v8l6c'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-6brrn | ClusterRoleBinding | pod-impersonation-helm-op-9jrm4 | cattle-system/pod-impersonation-helm-op-6jq8r | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-6jq8r' 绑定了角色 'pod-impersonation-helm-op-9jrm4'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-6pr6j | ClusterRoleBinding | pod-impersonation-helm-op-zbgrl | cattle-system/pod-impersonation-helm-op-fnm9k | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-fnm9k' 绑定了角色 'pod-impersonation-helm-op-zbgrl'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-6xxb2 | ClusterRoleBinding | pod-impersonation-helm-op-5s8gr | cattle-system/pod-impersonation-helm-op-cthvw | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-cthvw' 绑定了角色 'pod-impersonation-helm-op-5s8gr'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-82b9b | ClusterRoleBinding | pod-impersonation-helm-op-8wp96 | cattle-system/pod-impersonation-helm-op-2gdj7 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-2gdj7' 绑定了角色 'pod-impersonation-helm-op-8wp96'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-9gs7x | ClusterRoleBinding | pod-impersonation-helm-op-gbvrl | cattle-system/pod-impersonation-helm-op-8cbxf | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-8cbxf' 绑定了角色 'pod-impersonation-helm-op-gbvrl'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-9jt58 | ClusterRoleBinding | pod-impersonation-helm-op-757zp | cattle-system/pod-impersonation-helm-op-h75lf | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-h75lf' 绑定了角色 'pod-impersonation-helm-op-757zp'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-9k9c2 | ClusterRoleBinding | pod-impersonation-helm-op-rcj8w | cattle-system/pod-impersonation-helm-op-ml2nr | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-ml2nr' 绑定了角色 'pod-impersonation-helm-op-rcj8w'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-bddvb | ClusterRoleBinding | pod-impersonation-helm-op-jbbkt | cattle-system/pod-impersonation-helm-op-wqw7h | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-wqw7h' 绑定了角色 'pod-impersonation-helm-op-jbbkt'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-bff8v | ClusterRoleBinding | pod-impersonation-helm-op-c5lcf | cattle-system/pod-impersonation-helm-op-6qdrm | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-6qdrm' 绑定了角色 'pod-impersonation-helm-op-c5lcf'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-bklrr | ClusterRoleBinding | pod-impersonation-helm-op-f94sj | cattle-system/pod-impersonation-helm-op-2z5sx | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-2z5sx' 绑定了角色 'pod-impersonation-helm-op-f94sj'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-bpsb2 | ClusterRoleBinding | pod-impersonation-helm-op-sjdp9 | cattle-system/pod-impersonation-helm-op-sjr2r | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-sjr2r' 绑定了角色 'pod-impersonation-helm-op-sjdp9'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-c6nnc | ClusterRoleBinding | pod-impersonation-helm-op-tr74c | cattle-system/pod-impersonation-helm-op-26g4q | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-26g4q' 绑定了角色 'pod-impersonation-helm-op-tr74c'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-ckbbq | ClusterRoleBinding | pod-impersonation-helm-op-l4kpk | cattle-system/pod-impersonation-helm-op-gkv6w | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-gkv6w' 绑定了角色 'pod-impersonation-helm-op-l4kpk'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-crrsp | ClusterRoleBinding | pod-impersonation-helm-op-tkvwf | cattle-system/pod-impersonation-helm-op-jfcch | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-jfcch' 绑定了角色 'pod-impersonation-helm-op-tkvwf'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-dpgn4 | ClusterRoleBinding | pod-impersonation-helm-op-6xh8b | cattle-system/pod-impersonation-helm-op-244dl | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-244dl' 绑定了角色 'pod-impersonation-helm-op-6xh8b'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-dwmj4 | ClusterRoleBinding | pod-impersonation-helm-op-tmqbs | cattle-system/pod-impersonation-helm-op-xfjms | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-xfjms' 绑定了角色 'pod-impersonation-helm-op-tmqbs'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-ffkjt | ClusterRoleBinding | pod-impersonation-helm-op-w7zbh | cattle-system/pod-impersonation-helm-op-c4g8b | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-c4g8b' 绑定了角色 'pod-impersonation-helm-op-w7zbh'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-gqb8w | ClusterRoleBinding | pod-impersonation-helm-op-dcj58 | cattle-system/pod-impersonation-helm-op-fzhsq | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-fzhsq' 绑定了角色 'pod-impersonation-helm-op-dcj58'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-jx4h4 | ClusterRoleBinding | pod-impersonation-helm-op-qtpkq | cattle-system/pod-impersonation-helm-op-qmflv | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-qmflv' 绑定了角色 'pod-impersonation-helm-op-qtpkq'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-jzc57 | ClusterRoleBinding | pod-impersonation-helm-op-gnmwf | cattle-system/pod-impersonation-helm-op-cqwwl | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-cqwwl' 绑定了角色 'pod-impersonation-helm-op-gnmwf'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-k4dpm | ClusterRoleBinding | pod-impersonation-helm-op-h9w8w | cattle-system/pod-impersonation-helm-op-qxrx4 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-qxrx4' 绑定了角色 'pod-impersonation-helm-op-h9w8w'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-kw6x7 | ClusterRoleBinding | pod-impersonation-helm-op-m5nsk | cattle-system/pod-impersonation-helm-op-cw6r5 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-cw6r5' 绑定了角色 'pod-impersonation-helm-op-m5nsk'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-lgwxj | ClusterRoleBinding | pod-impersonation-helm-op-wtl6p | cattle-system/pod-impersonation-helm-op-czvd4 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-czvd4' 绑定了角色 'pod-impersonation-helm-op-wtl6p'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-mlt49 | ClusterRoleBinding | pod-impersonation-helm-op-cn889 | cattle-system/pod-impersonation-helm-op-2tm55 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-2tm55' 绑定了角色 'pod-impersonation-helm-op-cn889'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-mqxvt | ClusterRoleBinding | pod-impersonation-helm-op-t4hnf | cattle-system/pod-impersonation-helm-op-q2fjj | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-q2fjj' 绑定了角色 'pod-impersonation-helm-op-t4hnf'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-mwr2n | ClusterRoleBinding | pod-impersonation-helm-op-5nvhv | cattle-system/pod-impersonation-helm-op-xw4jr | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-xw4jr' 绑定了角色 'pod-impersonation-helm-op-5nvhv'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-n9fst | ClusterRoleBinding | pod-impersonation-helm-op-w7nrj | cattle-system/pod-impersonation-helm-op-k66r4 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-k66r4' 绑定了角色 'pod-impersonation-helm-op-w7nrj'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-pmzmq | ClusterRoleBinding | pod-impersonation-helm-op-pt42m | cattle-system/pod-impersonation-helm-op-msbqf | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-msbqf' 绑定了角色 'pod-impersonation-helm-op-pt42m'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-pnf7s | ClusterRoleBinding | pod-impersonation-helm-op-2vl4x | cattle-system/pod-impersonation-helm-op-qwgw2 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-qwgw2' 绑定了角色 'pod-impersonation-helm-op-2vl4x'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-pqjms | ClusterRoleBinding | pod-impersonation-helm-op-4wxq5 | cattle-system/pod-impersonation-helm-op-mt9tx | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-mt9tx' 绑定了角色 'pod-impersonation-helm-op-4wxq5'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-r8n22 | ClusterRoleBinding | pod-impersonation-helm-op-vx9p2 | cattle-system/pod-impersonation-helm-op-qjrmm | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-qjrmm' 绑定了角色 'pod-impersonation-helm-op-vx9p2'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-r8rcd | ClusterRoleBinding | pod-impersonation-helm-op-66g2d | cattle-system/pod-impersonation-helm-op-4db5z | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-4db5z' 绑定了角色 'pod-impersonation-helm-op-66g2d'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-rh5m5 | ClusterRoleBinding | pod-impersonation-helm-op-lckv5 | cattle-system/pod-impersonation-helm-op-lm2jx | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-lm2jx' 绑定了角色 'pod-impersonation-helm-op-lckv5'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-rjhpr | ClusterRoleBinding | pod-impersonation-helm-op-6k2jf | cattle-system/pod-impersonation-helm-op-m92sg | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-m92sg' 绑定了角色 'pod-impersonation-helm-op-6k2jf'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-sqvw9 | ClusterRoleBinding | pod-impersonation-helm-op-5lptx | cattle-system/pod-impersonation-helm-op-zwdxt | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-zwdxt' 绑定了角色 'pod-impersonation-helm-op-5lptx'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-t5n5g | ClusterRoleBinding | pod-impersonation-helm-op-hhwcp | cattle-system/pod-impersonation-helm-op-bgtgd | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-bgtgd' 绑定了角色 'pod-impersonation-helm-op-hhwcp'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-t8jtj | ClusterRoleBinding | pod-impersonation-helm-op-m48qz | cattle-system/pod-impersonation-helm-op-thz7c | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-thz7c' 绑定了角色 'pod-impersonation-helm-op-m48qz'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-twt6q | ClusterRoleBinding | pod-impersonation-helm-op-rqbtz | cattle-system/pod-impersonation-helm-op-94h7d | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-94h7d' 绑定了角色 'pod-impersonation-helm-op-rqbtz'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-v286q | ClusterRoleBinding | pod-impersonation-helm-op-2tc9l | cattle-system/pod-impersonation-helm-op-rlvwt | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-rlvwt' 绑定了角色 'pod-impersonation-helm-op-2tc9l'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-v8g88 | ClusterRoleBinding | pod-impersonation-helm-op-k77h6 | cattle-system/pod-impersonation-helm-op-x6zw4 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-x6zw4' 绑定了角色 'pod-impersonation-helm-op-k77h6'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-vbxs4 | ClusterRoleBinding | pod-impersonation-helm-op-9xbgj | cattle-system/pod-impersonation-helm-op-n8mj2 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-n8mj2' 绑定了角色 'pod-impersonation-helm-op-9xbgj'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-vc785 | ClusterRoleBinding | pod-impersonation-helm-op-k6sjq | cattle-system/pod-impersonation-helm-op-hrjlg | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-hrjlg' 绑定了角色 'pod-impersonation-helm-op-k6sjq'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-vx5vc | ClusterRoleBinding | pod-impersonation-helm-op-gxlbs | cattle-system/pod-impersonation-helm-op-ntnc9 | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-ntnc9' 绑定了角色 'pod-impersonation-helm-op-gxlbs'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-w82tx | ClusterRoleBinding | pod-impersonation-helm-op-9xrt2 | cattle-system/pod-impersonation-helm-op-pqtrm | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-pqtrm' 绑定了角色 'pod-impersonation-helm-op-9xrt2'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-wfnc6 | ClusterRoleBinding | pod-impersonation-helm-op-hnm9z | cattle-system/pod-impersonation-helm-op-m78wc | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-m78wc' 绑定了角色 'pod-impersonation-helm-op-hnm9z'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-ww8qh | ClusterRoleBinding | pod-impersonation-helm-op-hwvnj | cattle-system/pod-impersonation-helm-op-9kdkh | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-9kdkh' 绑定了角色 'pod-impersonation-helm-op-hwvnj'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-wxvwz | ClusterRoleBinding | pod-impersonation-helm-op-vswxt | cattle-system/pod-impersonation-helm-op-5bzsf | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-5bzsf' 绑定了角色 'pod-impersonation-helm-op-vswxt'，权限在合理范围内 |
| cluster-wide | pod-impersonation-helm-op-xlb2g | ClusterRoleBinding | pod-impersonation-helm-op-nw4rp | cattle-system/pod-impersonation-helm-op-78n5w | 🟢 低风险 | ServiceAccount 'pod-impersonation-helm-op-78n5w' 绑定了角色 'pod-impersonation-helm-op-nw4rp'，权限在合理范围内 |
| cluster-wide | request-fv2kf-content | ClusterRoleBinding | fleet-content | cluster-fleet-local-local-1a3d67d0a899/request-fv2kf-aa226cb6-862d-402c-a9a4-37717cb23b8a | 🟢 低风险 | ServiceAccount 'request-fv2kf-aa226cb6-862d-402c-a9a4-37717cb23b8a' 绑定了角色 'fleet-content'，权限在合理范围内 |
| cluster-wide | run-nfs-client-provisioner | ClusterRoleBinding | nfs-client-provisioner-runner | kube-system/nfs-client-provisioner | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:attachdetach-controller | ClusterRoleBinding | system:controller:attachdetach-controller | kube-system/attachdetach-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:certificate-controller | ClusterRoleBinding | system:controller:certificate-controller | kube-system/certificate-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:clusterrole-aggregation-controller | ClusterRoleBinding | system:controller:clusterrole-aggregation-controller | kube-system/clusterrole-aggregation-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:cronjob-controller | ClusterRoleBinding | system:controller:cronjob-controller | kube-system/cronjob-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:daemon-set-controller | ClusterRoleBinding | system:controller:daemon-set-controller | kube-system/daemon-set-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:deployment-controller | ClusterRoleBinding | system:controller:deployment-controller | kube-system/deployment-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:disruption-controller | ClusterRoleBinding | system:controller:disruption-controller | kube-system/disruption-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:endpoint-controller | ClusterRoleBinding | system:controller:endpoint-controller | kube-system/endpoint-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:endpointslice-controller | ClusterRoleBinding | system:controller:endpointslice-controller | kube-system/endpointslice-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:endpointslicemirroring-controller | ClusterRoleBinding | system:controller:endpointslicemirroring-controller | kube-system/endpointslicemirroring-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:ephemeral-volume-controller | ClusterRoleBinding | system:controller:ephemeral-volume-controller | kube-system/ephemeral-volume-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:expand-controller | ClusterRoleBinding | system:controller:expand-controller | kube-system/expand-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:generic-garbage-collector | ClusterRoleBinding | system:controller:generic-garbage-collector | kube-system/generic-garbage-collector | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:horizontal-pod-autoscaler | ClusterRoleBinding | system:controller:horizontal-pod-autoscaler | kube-system/horizontal-pod-autoscaler | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:job-controller | ClusterRoleBinding | system:controller:job-controller | kube-system/job-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:namespace-controller | ClusterRoleBinding | system:controller:namespace-controller | kube-system/namespace-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:node-controller | ClusterRoleBinding | system:controller:node-controller | kube-system/node-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:persistent-volume-binder | ClusterRoleBinding | system:controller:persistent-volume-binder | kube-system/persistent-volume-binder | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:pod-garbage-collector | ClusterRoleBinding | system:controller:pod-garbage-collector | kube-system/pod-garbage-collector | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:pv-protection-controller | ClusterRoleBinding | system:controller:pv-protection-controller | kube-system/pv-protection-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:pvc-protection-controller | ClusterRoleBinding | system:controller:pvc-protection-controller | kube-system/pvc-protection-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:replicaset-controller | ClusterRoleBinding | system:controller:replicaset-controller | kube-system/replicaset-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:replication-controller | ClusterRoleBinding | system:controller:replication-controller | kube-system/replication-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:resourcequota-controller | ClusterRoleBinding | system:controller:resourcequota-controller | kube-system/resourcequota-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:root-ca-cert-publisher | ClusterRoleBinding | system:controller:root-ca-cert-publisher | kube-system/root-ca-cert-publisher | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:route-controller | ClusterRoleBinding | system:controller:route-controller | kube-system/route-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:service-account-controller | ClusterRoleBinding | system:controller:service-account-controller | kube-system/service-account-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:service-controller | ClusterRoleBinding | system:controller:service-controller | kube-system/service-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:statefulset-controller | ClusterRoleBinding | system:controller:statefulset-controller | kube-system/statefulset-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:ttl-after-finished-controller | ClusterRoleBinding | system:controller:ttl-after-finished-controller | kube-system/ttl-after-finished-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:controller:ttl-controller | ClusterRoleBinding | system:controller:ttl-controller | kube-system/ttl-controller | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:coredns | ClusterRoleBinding | system:coredns | kube-system/coredns | 🟢 低风险 | 正常权限绑定 |
| cluster-wide | system:kube-dns | ClusterRoleBinding | system:kube-dns | kube-system/kube-dns | 🟢 低风险 | 正常权限绑定 |

---

## 💡 安全建议

1. **最小权限原则**: 始终遵循最小权限原则，只授予 ServiceAccount 完成任务所需的最小权限。
2. **定期审计**: 建议定期运行此审计工具，及时发现并处理权限过大问题。
3. **使用自定义角色**: 避免直接绑定 cluster-admin 等高权限角色，应创建自定义角色并授予必要权限。
4. **监控异常绑定**: 关注非系统 Namespace 中出现的高风险角色绑定，这可能是安全事件的征兆。
5. **及时清理**: 删除不再使用的 ServiceAccount 和 RoleBinding，减少攻击面。

---

*报告由 K8s 权限审计小工具自动生成于 2026-05-09 15:38:34*