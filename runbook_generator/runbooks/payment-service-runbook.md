# Incident Runbook

## Executive Summary

The Payment service is returning HTTP 500 errors shortly after a recent deployment. CPU utilization increased significantly from approximately 35% to 95%, and service pods have restarted three times. The incident began roughly 10 minutes after a deployment completed, making the deployment a likely contributing factor.

Primary goals:

- Restore Payment service availability.
- Reduce HTTP 500 error rate.
- Stabilize pod restarts and CPU utilization.
- Determine whether the recent deployment introduced a regression.

---

## Initial Assessment

Immediate observations:

- Payment service is returning HTTP 500 responses.
- CPU utilization increased from 35% baseline to 95%.
- Payment service pods have restarted three times.
- A deployment completed approximately 10 minutes before the incident began.
- High CPU and pod restarts may indicate:
  - Application bug or infinite loop.
  - Increased request latency or thread exhaustion.
  - Memory/CPU resource pressure.
  - Misconfiguration introduced by deployment.
  - Dependency failure causing retry storms.

Initial impact:

- Payment flows may be failing.
- Customers may be unable to complete transactions.
- Downstream or upstream services may also be affected by retries or timeouts.

---

## Investigation Steps

1. **Confirm incident scope**
   - Check whether all Payment service endpoints are affected or only specific APIs.
   - Confirm if HTTP 500 errors are occurring across all regions, clusters, or availability zones.
   - Determine if the issue affects all customers or a subset.

2. **Check deployment details**
   - Identify the deployment version released 10 minutes before the incident.
   - Review the deployment changelog, commits, configuration changes, and feature flags.
   - Confirm whether any database migrations, dependency upgrades, or infrastructure changes were included.

3. **Review service health metrics**
   - Check:
     - HTTP 500 error rate.
     - Request latency.
     - Request throughput.
     - CPU utilization.
     - Memory utilization.
     - Pod restart count.
     - Container OOM kills.
     - Saturation metrics such as thread pool, connection pool, or queue depth.

4. **Inspect Kubernetes pod status**
   - Run:
     ```bash
     kubectl get pods -n <namespace> -l app=payment-service
     kubectl describe pod <pod-name> -n <namespace>
     ```
   - Look for:
     - CrashLoopBackOff.
     - OOMKilled.
     - Failed liveness/readiness probes.
     - CPU throttling.
     - Image pull or startup errors.
     - Recent events around restart times.

5. **Check application logs**
   - Review logs from the failing pods:
     ```bash
     kubectl logs <pod-name> -n <namespace> --previous
     kubectl logs <pod-name> -n <namespace>
     ```
   - Look for:
     - Exceptions or stack traces.
     - Timeout errors.
     - Dependency errors.
     - Payment provider failures.
     - Database connection failures.
     - Repeated retries.
     - Configuration loading errors.

6. **Compare logs before and after deployment**
   - Compare error patterns from before and after the deployment.
   - Identify new exception types, warnings, or high-frequency log messages.

7. **Check CPU-related behavior**
   - Determine whether CPU is high due to:
     - Increased traffic.
     - Expensive code path.
     - Retry loops.
     - Infinite loop.
     - Serialization/deserialization issue.
     - Cryptographic/payment processing workload increase.
   - Check CPU throttling metrics if resource limits are configured.

8. **Review readiness and liveness probe behavior**
   - Verify whether pods are restarting due to failed health checks.
   - Confirm that probe thresholds are appropriate and were not changed in the deployment.

9. **Check dependencies**
   - Verify health of:
     - Payment gateway/provider.
     - Database.
     - Cache.
     - Message queues.
     - Fraud/risk service.
     - Authentication/authorization service.
   - Look for increased latency, errors, or connection failures.

10. **Inspect recent configuration and secret changes**
    - Confirm whether environment variables, config maps, secrets, credentials, certificates, or API endpoints changed.
    - Validate that the deployed pods are using expected configuration values.

11. **Check traffic patterns**
    - Determine whether there was a traffic spike coinciding with the incident.
    - Review ingress/load balancer metrics.
    - Check for retry amplification from upstream services.

12. **Evaluate autoscaling behavior**
    - Check Horizontal Pod Autoscaler status:
      ```bash
      kubectl get hpa -n <namespace>
      kubectl describe hpa <hpa-name> -n <namespace>
      ```
    - Confirm whether scaling occurred or failed.
    - Verify CPU requests/limits are set correctly.

13. **Determine if rollback is required**
    - If the new deployment correlates strongly with the error spike and no quick configuration fix is available, proceed with rollback.

---

## Possible Root Causes

Most likely causes:

- Defective application code introduced in the recent deployment.
- New code path causing excessive CPU usage.
- Infinite loop or inefficient processing in payment logic.
- Misconfigured deployment, environment variable, feature flag, or secret.
- Failed or incompatible database migration.
- Dependency timeout causing retry storm and CPU exhaustion.
- Payment provider or downstream service degraded, causing unhandled exceptions.
- Liveness/readiness probe misconfiguration causing unnecessary pod restarts.
- Resource limits too low for the new version, resulting in CPU throttling or instability.
- Memory leak or OOM condition, if pod restarts are caused by `OOMKilled`.

---

## Immediate Mitigation

Actions to restore service:

1. **Declare incident and start coordination**
   - Open an incident channel.
   - Assign incident commander, communications lead, and technical lead.
   - Notify relevant teams: Payments, Platform/SRE, Backend, Customer Support.

2. **Reduce customer impact**
   - If possible, temporarily disable non-critical Payment service features introduced in the latest release.
   - Disable risky feature flags related to the deployment.
   - Route traffic away from unhealthy pods or regions if applicable.

3. **Scale the Payment service**
   - If CPU saturation is contributing to failures, temporarily increase replicas:
     ```bash
     kubectl scale deployment payment-service -n <namespace> --replicas=<higher-count>
     ```
   - Confirm the cluster has enough capacity.
   - Scaling may reduce CPU pressure but should not replace rollback if the deployment is faulty.

4. **Restart unhealthy pods if necessary**
   - If pods are stuck or degraded:
     ```bash
     kubectl rollout restart deployment payment-service -n <namespace>
     ```
   - Use caution: if the new version is defective, restarting may not help.

5. **Limit retry amplification**
   - If upstream services are retrying aggressively, reduce retry volume or enable circuit breakers.
   - Confirm client timeouts are reasonable.
   - Protect downstream dependencies from overload.

6. **Increase resource limits temporarily**
   - If CPU throttling is observed and the new workload is expected:
     - Increase CPU requests/limits.
     - Redeploy with updated resources.
   - This should be used as a temporary mitigation unless capacity changes are validated.

7. **Rollback if the deployment is suspected**
   - Since the incident started shortly after deployment, prepare to roll back immediately if no safe fix is available.

---

## Rollback Strategy

Rollback is applicable because a deployment completed 10 minutes before the incident.

### When to Roll Back

Rollback should be initiated if:

- HTTP 500 errors increased after the latest deployment.
- CPU utilization increased after the latest deployment.
- Pod restarts began after the latest deployment.
- Logs show new exceptions introduced by the new version.
- No quick and safe configuration or feature flag mitigation is available.
- Payment success rate is materially impacted.

### How to Roll Back

1. **Identify current and previous revisions**
   ```bash
   kubectl rollout history deployment payment-service -n <namespace>
   ```

2. **Rollback to the previous stable version**
   ```bash
   kubectl rollout undo deployment payment-service -n <namespace>
   ```

3. **Monitor rollout status**
   ```bash
   kubectl rollout status deployment payment-service -n <namespace>
   ```

4. **Verify pods are running the previous image**
   ```bash
   kubectl get pods -n <namespace> -l app=payment-service -o wide
   kubectl describe deployment payment-service -n <namespace>
   ```

5. **If using progressive delivery**
   - Abort the rollout in the deployment tool.
   - Shift traffic back to the stable version.
   - Disable canary or blue/green traffic for the new version.

6. **If database migrations were included**
   - Verify whether migrations are backward-compatible.
   - Do not roll back application code blindly if schema changes are incompatible.
   - Escalate to the database/application owner before rollback if data compatibility is uncertain.

---

## Verification Steps

Confirm resolution using the following checks:

1. **HTTP 500 error rate returns to normal**
   - Verify Payment service 5xx rate drops to baseline.
   - Check both service-level and endpoint-level metrics.

2. **Payment success rate recovers**
   - Confirm successful payment authorization/capture flows.
   - Validate business KPIs if available.

3. **CPU utilization stabilizes**
   - CPU should return near baseline or acceptable operating range.
   - Confirm no sustained CPU saturation or throttling.

4. **Pod restarts stop**
   - Check restart counts:
     ```bash
     kubectl get pods -n <namespace> -l app=payment-service
     ```
   - Ensure pods remain healthy for at least 15–30 minutes.

5. **Pods pass readiness and liveness checks**
   - Confirm all replicas are ready:
     ```bash
     kubectl get deployment payment-service -n <namespace>
     ```

6. **Application logs are clean**
   - Verify no recurring stack traces, timeout loops, or high-volume errors.

7. **Dependency health is normal**
   - Confirm database, payment provider, cache, and queues are healthy.
   - Check connection pool and timeout metrics.

8. **Synthetic and manual transaction tests pass**
   - Run synthetic payment test flows.
   - If permitted, perform controlled test transactions.

9. **No new alerts are firing**
   - Confirm related alerts have resolved:
     - High CPU.
     - Pod restart count.
     - HTTP 5xx rate.
     - Latency.
     - Payment failure rate.

---

## Escalation

Escalate immediately if:

- Payment failures continue after rollback.
- CPU remains high despite rollback and scaling.
- Pods continue restarting.
- Database migration or data corruption is suspected.
- Payment provider or critical third-party dependency appears degraded.
- Multiple regions or clusters are affected.
- Customer impact is severe or increasing.
- There is uncertainty around financial correctness, duplicate charges, or lost transactions.

Escalation contacts:

- Payment service engineering team.
- SRE/on-call platform team.
- Database team, if database errors or migrations are involved.
- Security/compliance team, if sensitive payment data or PCI-related concerns are suspected.
- Incident management leadership for major customer impact.
- Third-party payment provider support, if provider errors are observed.

---

## References

Review the following resources during investigation and mitigation:

- **Dashboards**
  - Payment Service Overview dashboard.
  - HTTP error rate and latency dashboard.
  - Kubernetes workload dashboard.
  - CPU/memory utilization dashboard.
  - Pod restart and container health dashboard.
  - Payment success/failure business metrics dashboard.
  - Dependency health dashboard.
  - Ingress/load balancer dashboard.

- **Logs**
  - Payment service application logs.
  - Previous pod logs:
    ```bash
    kubectl logs <pod-name> -n <namespace> --previous
    ```
  - Kubernetes events:
    ```bash
    kubectl get events -n <namespace> --sort-by=.lastTimestamp
    ```
  - Ingress/load balancer access logs.
  - Payment provider integration logs.
  - Database logs and slow query logs.

- **Metrics**
  - HTTP 5xx rate.
  - Request latency p50/p95/p99.
  - Request throughput.
  - CPU utilization and throttling.
  - Memory utilization and OOM kills.
  - Pod restart count.
  - Readiness/liveness probe failures.
  - Database connection pool usage.
  - Downstream timeout and retry counts.
  - Queue depth, if applicable.

- **Documentation**
  - Payment service deployment guide.
  - Rollback procedure.
  - Kubernetes operational guide.
  - Feature flag management documentation.
  - Payment provider integration documentation.
  - Recent release notes and changelog.
  - Database migration documentation.