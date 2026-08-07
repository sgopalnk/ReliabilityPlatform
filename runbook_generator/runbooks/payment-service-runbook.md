# Incident Runbook

## Executive Summary

The payment service is returning HTTP 500 errors shortly after a deployment completed. CPU utilization increased significantly from approximately 35% to 95%, and service pods have restarted three times. The incident likely relates to the recent deployment, increased resource consumption, crash loops, or a downstream dependency failure causing excessive load or unhandled errors.

Primary objectives:

- Restore payment service availability.
- Reduce HTTP 500 error rate.
- Stabilize pod restarts and CPU utilization.
- Determine whether the recent deployment introduced the issue.

---

## Initial Assessment

Immediate observations:

- Payment service is returning HTTP 500 responses.
- CPU utilization increased from 35% to 95%.
- Pods restarted three times.
- A deployment completed approximately 10 minutes before the incident.
- The issue is likely production-impacting and may affect customer payments.
- Recent deployment timing strongly suggests a possible regression or misconfiguration.

Initial severity recommendation:

- **SEV-1 or SEV-2**, depending on payment volume impact and customer-facing availability.
- Treat as high priority because payment failures directly affect revenue and user experience.

---

## Investigation Steps

1. **Confirm the scope of impact**
   - Check whether all payment endpoints are affected or only specific APIs.
   - Confirm if HTTP 500s are occurring across all regions, clusters, or availability zones.
   - Review error rate, request volume, and latency trends.

2. **Check deployment timeline**
   - Identify the exact deployment timestamp.
   - Confirm the deployed version, image tag, commit SHA, and configuration changes.
   - Compare the start of HTTP 500s, CPU spike, and pod restarts against the deployment time.

3. **Review Kubernetes pod status**
   - Check pod health:
     ```bash
     kubectl get pods -n <namespace> -l app=payment-service
     ```
   - Describe affected pods:
     ```bash
     kubectl describe pod <pod-name> -n <namespace>
     ```
   - Look for:
     - `CrashLoopBackOff`
     - `OOMKilled`
     - Failed readiness or liveness probes
     - CPU throttling
     - Image pull or startup errors

4. **Inspect recent pod logs**
   - Review logs from currently running pods:
     ```bash
     kubectl logs <pod-name> -n <namespace>
     ```
   - Review previous crashed container logs:
     ```bash
     kubectl logs <pod-name> -n <namespace> --previous
     ```
   - Look for:
     - Stack traces
     - Dependency failures
     - Database connection errors
     - Timeout errors
     - Authentication or secret-related errors
     - Unexpected retry loops

5. **Analyze HTTP 500 errors**
   - Check application logs for exception types and affected routes.
   - Correlate request IDs or trace IDs from API gateway/load balancer logs to application logs.
   - Determine whether errors are caused by:
     - Application exceptions
     - Failed downstream calls
     - Database errors
     - Payment gateway errors
     - Resource exhaustion

6. **Check CPU and resource usage**
   - Review CPU usage per pod and container.
   - Check whether CPU usage is evenly distributed or isolated to specific pods.
   - Check for CPU throttling:
     ```bash
     kubectl top pods -n <namespace>
     ```
   - Review resource requests and limits from the deployment manifest.

7. **Review pod restart reasons**
   - Determine whether restarts are due to:
     - Liveness probe failures
     - Application crashes
     - OOM kills
     - Node-level issues
   - Use:
     ```bash
     kubectl describe pod <pod-name> -n <namespace>
     ```

8. **Check readiness and liveness probes**
   - Confirm probes are not failing due to increased latency or dependency checks.
   - Validate whether the probes were changed in the recent deployment.
   - Check Kubernetes events:
     ```bash
     kubectl get events -n <namespace> --sort-by='.lastTimestamp'
     ```

9. **Review dependency health**
   - Check downstream systems used by the payment service:
     - Payment processor/gateway
     - Database
     - Cache
     - Message queues
     - Fraud/risk services
     - Authentication/authorization services
   - Look for latency spikes, error rates, saturation, or connection pool exhaustion.

10. **Compare with previous stable version**
    - Compare configuration, environment variables, secrets, resource limits, and dependencies between the current and previous deployment.
    - Check whether migrations or feature flags were introduced.

11. **Check autoscaling behavior**
    - Review Horizontal Pod Autoscaler status:
      ```bash
      kubectl get hpa -n <namespace>
      ```
    - Confirm whether pods scaled up as expected.
    - Check if CPU utilization exceeds target but scaling is blocked by max replicas or cluster capacity.

12. **Check node-level health**
    - Verify whether affected pods are running on the same node.
    - Check node CPU, memory, disk, and kubelet health:
      ```bash
      kubectl get nodes
      kubectl describe node <node-name>
      ```

13. **Review recent configuration or secret changes**
    - Check if secrets, config maps, payment credentials, or environment variables changed with the deployment.
    - Confirm the application can authenticate to required services.

14. **Inspect distributed traces**
    - Use tracing tools to identify where requests are failing.
    - Look for high-latency spans, repeated retries, or failing downstream calls.

15. **Decide mitigation path**
    - If the new deployment is strongly correlated and no quick fix is available, initiate rollback.
    - If CPU saturation is the primary issue and the application is otherwise healthy, consider temporary scaling.
    - If a dependency is failing, apply circuit breakers, disable affected feature paths, or fail over if available.

---

## Possible Root Causes

Most likely causes:

- Recent deployment introduced an application bug causing HTTP 500 errors.
- Recent deployment introduced inefficient code causing CPU saturation.
- Configuration change caused incorrect behavior, failed authentication, or broken dependency access.
- New code path triggered excessive retries to a downstream dependency.
- Liveness or readiness probes are misconfigured, causing pod restarts under load.
- Resource limits are too low or CPU throttling is causing application instability.
- Dependency latency or failure is causing request pileups and high CPU usage.
- Database query regression introduced by the deployment.
- Connection pool exhaustion to database, cache, or payment gateway.
- Feature flag enabled a faulty or CPU-intensive code path.
- Memory pressure or OOM kills causing repeated pod restarts.
- Bad container image or incompatible library/runtime version.
- Autoscaling did not respond quickly enough or hit maximum replica limits.

---

## Immediate Mitigation

Actions to restore service:

1. **Declare incident and notify stakeholders**
   - Open an incident channel.
   - Assign roles:
     - Incident Commander
     - Communications Lead
     - Operations Lead
     - Application Owner
   - Notify payment service owners and on-call engineers.

2. **Reduce customer impact**
   - If available, route traffic away from affected region or cluster.
   - Enable degraded mode if supported.
   - Temporarily disable non-critical payment features that may be causing failures.
   - Enable queueing or retry-safe handling where appropriate.

3. **Scale the service horizontally**
   - If CPU saturation is contributing to failures and cluster capacity exists:
     ```bash
     kubectl scale deployment payment-service -n <namespace> --replicas=<higher-count>
     ```
   - Confirm HPA limits are not preventing scale-out.
   - Increase max replicas temporarily if needed.

4. **Increase CPU limits if throttling is observed**
   - If CPU throttling is severe, increase CPU limits or requests temporarily.
   - Redeploy only if this can be done safely and quickly.

5. **Rollback the recent deployment**
   - If the incident started immediately after deployment and symptoms point to the new version, roll back to the last known good version.
   - This is the preferred mitigation if no immediate safe fix exists.

6. **Restart unhealthy pods if necessary**
   - If pods are stuck or degraded after rollback/config change:
     ```bash
     kubectl rollout restart deployment payment-service -n <namespace>
     ```
   - Avoid repeated restarts without addressing the cause.

7. **Disable faulty feature flags**
   - If a new feature flag was enabled, disable it immediately.
   - Confirm the change propagates to all pods.

8. **Protect downstream services**
   - Reduce retry rates if they are amplifying load.
   - Enable circuit breakers if available.
   - Temporarily rate-limit traffic if downstream systems are being overwhelmed.

9. **Monitor service recovery**
   - Watch HTTP 500 rate, CPU, pod restarts, latency, and payment success rate during and after mitigation.

---

## Rollback Strategy

Rollback should be initiated if:

- HTTP 500 errors began shortly after the deployment.
- CPU utilization spike correlates with the new version.
- Pods started restarting after the new deployment.
- No safe configuration or feature flag mitigation is immediately available.
- Payment success rate remains degraded.

Rollback steps:

1. **Identify the previous stable revision**
   ```bash
   kubectl rollout history deployment payment-service -n <namespace>
   ```

2. **Rollback to the previous deployment**
   ```bash
   kubectl rollout undo deployment payment-service -n <namespace>
   ```

   Or roll back to a specific revision:
   ```bash
   kubectl rollout undo deployment payment-service -n <namespace> --to-revision=<revision-number>
   ```

3. **Monitor rollout status**
   ```bash
   kubectl rollout status deployment payment-service -n <namespace>
   ```

4. **Confirm pods are running the expected image**
   ```bash
   kubectl get pods -n <namespace> -l app=payment-service -o wide
   kubectl describe deployment payment-service -n <namespace>
   ```

5. **Validate no database migration incompatibility**
   - Confirm the previous application version is compatible with any schema changes.
   - If a migration is not backward-compatible, escalate before rollback or follow the database rollback plan.

6. **Confirm service recovery**
   - Check HTTP 500 rate.
   - Check payment success rate.
   - Check CPU utilization.
   - Confirm pod restart count stops increasing.

7. **Freeze further deployments**
   - Block additional deployments to the payment service until root cause is identified.

---

## Verification Steps

Verify the incident has been resolved by confirming:

1. **HTTP 500 error rate returns to baseline**
   - Check service-level and endpoint-level error rates.
   - Confirm no sustained spike remains.

2. **Payment success rate returns to normal**
   - Confirm successful authorization/capture rates.
   - Check business metrics for failed or abandoned payments.

3. **CPU utilization normalizes**
   - CPU should return near historical baseline or within expected autoscaling target.
   - Confirm no ongoing CPU throttling.

4. **Pods remain stable**
   - Restart count should stop increasing.
   - Pods should be in `Running` and `Ready` state:
     ```bash
     kubectl get pods -n <namespace> -l app=payment-service
     ```

5. **Deployment rollout is healthy**
   ```bash
   kubectl rollout status deployment payment-service -n <namespace>
   ```

6. **Latency returns to normal**
   - Check p50, p95, and p99 latency.
   - Confirm no queue buildup or request timeouts.

7. **Logs no longer show critical errors**
   - Confirm stack traces or repeated exceptions have stopped.
   - Check both application and gateway logs.

8. **Downstream dependencies are healthy**
   - Database, cache, payment provider, and message queues should show normal latency and error rates.

9. **Synthetic and manual payment tests pass**
   - Run synthetic transaction tests.
   - If allowed, perform a controlled test payment through the production path.

10. **Customer support impact stabilizes**
    - Confirm no continued increase in payment-related support tickets or alerts.

---

## Escalation

Escalate immediately if:

- Payment failures are widespread or revenue-impacting.
- HTTP 500 error rate remains elevated after initial mitigation.
- Rollback fails or cannot be performed safely.
- Pods continue restarting after rollback.
- CPU remains near saturation after scaling or rollback.
- A database migration may be incompatible with rollback.
- Downstream payment provider issues are suspected.
- Data consistency, duplicate charges, or failed captures are possible.
- Customer transactions may be stuck in an unknown state.
- Security, compliance, or financial reconciliation concerns exist.

Escalation contacts/teams:

- Payment service application owner
- Platform/SRE on-call
- Database on-call
- Kubernetes/Infrastructure on-call
- Payment gateway/vendor support
- Incident Commander
- Engineering manager/director
- Customer support and communications teams
- Security/compliance team if financial integrity is at risk

---

## References

Review the following dashboards, logs, metrics, and documentation:

### Dashboards

- Payment service overview dashboard
- Kubernetes workload dashboard for payment service
- HTTP error rate and latency dashboard
- CPU/memory utilization dashboard
- HPA/autoscaling dashboard
- Node health dashboard
- Payment success/failure business metrics dashboard
- Downstream dependency dashboards:
  - Database
  - Cache
  - Message queue
  - Payment gateway/provider
  - Fraud/risk service

### Logs

- Payment service application logs
- Previous container logs for restarted pods:
  ```bash
  kubectl logs <pod-name> -n <namespace> --previous
  ```
- API gateway or ingress logs
- Load balancer logs
- Kubernetes event logs:
  ```bash
  kubectl get events -n <namespace> --sort-by='.lastTimestamp'
  ```
- Database slow query and error logs
- Payment provider integration logs
- Audit logs for deployments, config maps, secrets, and feature flags

### Metrics

- HTTP 5xx rate
- Request throughput
- p50/p95/p99 latency
- CPU utilization
- CPU throttling
- Memory utilization
- Pod restart count
- Readiness and liveness probe failures
- HPA desired/current replicas
- Database connection pool usage
- Downstream timeout/error rate
- Retry rate
- Queue depth
- Payment authorization/capture success rate

### Documentation

- Payment service deployment guide
- Payment service rollback procedure
- Kubernetes runbook for pod restarts and crash loops
- Feature flag management documentation
- Database migration rollback policy
- Incident response process
- Payment provider integration documentation
- Service ownership and escalation matrix
- Recent release notes and change logs for the payment service