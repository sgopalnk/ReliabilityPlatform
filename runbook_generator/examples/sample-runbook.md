# Incident Runbook

## Executive Summary

The Payment service is returning HTTP 500 errors shortly after a deployment. CPU utilization increased significantly from approximately 35% to 95%, and service pods have restarted three times. The incident began about 10 minutes after a deployment completed, suggesting a likely correlation with the recent release.

Primary impact: users may be unable to complete payments or may experience failed payment requests.

---

## Initial Assessment

Immediate observations:

- Payment service is returning HTTP 500 responses.
- CPU utilization increased from 35% to 95%.
- Payment service pods restarted three times.
- A deployment completed approximately 10 minutes before the incident.
- The issue may be related to:
  - A faulty deployment.
  - Increased CPU usage caused by a code change.
  - CrashLoopBackOff or pod instability.
  - Dependency failures triggered by the new release.
  - Resource limits being exceeded.

Initial severity should be treated as high because payment processing is business-critical.

---

## Investigation Steps

1. **Confirm service impact**
   - Check current HTTP 500 error rate.
   - Confirm whether all payment endpoints are affected or only specific routes.
   - Determine if the issue impacts all users, a subset of users, or specific regions.

2. **Check recent deployment details**
   - Identify the deployed version or image tag.
   - Review deployment timestamp.
   - Compare the incident start time with the deployment completion time.
   - Check deployment logs and CI/CD pipeline status.

3. **Inspect pod status**
   - Run:
     ```bash
     kubectl get pods -n <namespace> -l app=payment-service
     ```
   - Look for:
     - Restart count.
     - CrashLoopBackOff.
     - OOMKilled.
     - Pending or failed pods.

4. **Describe affected pods**
   - Run:
     ```bash
     kubectl describe pod <pod-name> -n <namespace>
     ```
   - Check for:
     - Container restart reasons.
     - CPU throttling.
     - Failed readiness or liveness probes.
     - Resource limit violations.
     - Kubernetes events.

5. **Review application logs**
   - Run:
     ```bash
     kubectl logs <pod-name> -n <namespace> --previous
     kubectl logs <pod-name> -n <namespace>
     ```
   - Look for:
     - Stack traces.
     - Timeout errors.
     - Dependency failures.
     - Database connection errors.
     - Payment provider API failures.
     - Out-of-memory or CPU-related errors.

6. **Check service metrics**
   - Review:
     - Request rate.
     - Error rate.
     - Latency.
     - CPU usage.
     - Memory usage.
     - Pod restart count.
     - Thread count or goroutine count, if available.
     - Garbage collection metrics, if applicable.

7. **Check CPU throttling**
   - Verify whether the service is hitting CPU limits.
   - Review container CPU usage against requested and limited CPU.
   - Look for sustained CPU throttling after deployment.

8. **Check readiness and liveness probes**
   - Verify whether pods are being restarted due to failing health checks.
   - Confirm whether health check endpoints are functioning correctly.

9. **Compare current version with previous stable version**
   - Review recent code changes.
   - Look for changes related to:
     - Payment processing logic.
     - Database queries.
     - External payment provider calls.
     - Retry behavior.
     - Background jobs.
     - Caching.
     - Serialization/deserialization.
     - Authentication or request validation.

10. **Check dependencies**
    - Verify health of:
      - Payment gateway/provider.
      - Database.
      - Cache layer.
      - Message queue.
      - Internal services used by Payment service.
    - Confirm whether dependency latency or errors increased after deployment.

11. **Check traffic patterns**
    - Determine whether traffic increased unexpectedly.
    - Review ingress/load balancer metrics.
    - Check if a spike in requests coincided with the deployment.

12. **Review autoscaling behavior**
    - Check Horizontal Pod Autoscaler status:
      ```bash
      kubectl get hpa -n <namespace>
      kubectl describe hpa <hpa-name> -n <namespace>
      ```
    - Confirm whether scaling occurred or failed to occur.

13. **Check configuration changes**
    - Review recent changes to:
      - Environment variables.
      - ConfigMaps.
      - Secrets.
      - Feature flags.
      - Resource requests and limits.

---

## Possible Root Causes

Most likely causes include:

- **Faulty recent deployment**
  - New code introduced a bug causing HTTP 500 errors.
  - A new execution path is consuming excessive CPU.
  - A regression is causing crashes or failed health checks.

- **CPU exhaustion**
  - The service is CPU-bound after deployment.
  - Inefficient logic, infinite loop, excessive retries, or expensive queries may have been introduced.
  - CPU throttling may be causing request timeouts and readiness failures.

- **Pod instability**
  - Pods are restarting due to failed liveness probes.
  - Pods may be crashing because of unhandled exceptions.
  - Resource limits may be too low for the new workload.

- **Dependency failure or timeout**
  - Payment provider, database, cache, or internal dependency may be timing out.
  - New deployment may have changed how dependencies are called.

- **Configuration issue**
  - Incorrect environment variable, secret, or feature flag.
  - Misconfigured resource requests or limits.
  - Invalid endpoint or credential for a dependency.

- **Traffic or load spike**
  - Increased request volume may have coincided with deployment.
  - Autoscaling may not have reacted quickly enough.

---

## Immediate Mitigation

Actions to restore service:

1. **Declare incident and notify stakeholders**
   - Open an incident channel.
   - Notify engineering, SRE, product, and customer support teams.
   - Assign incident commander, communications owner, and technical lead.

2. **Reduce customer impact**
   - If available, route traffic to a healthy previous version.
   - Temporarily disable non-critical payment features through feature flags.
   - Enable graceful degradation if supported.

3. **Scale the service horizontally**
   - If pods are running but CPU is saturated, increase replicas:
     ```bash
     kubectl scale deployment payment-service -n <namespace> --replicas=<higher-count>
     ```
   - Confirm new pods become ready and traffic is distributed.

4. **Increase CPU resources if safe**
   - If CPU limits are too restrictive, increase CPU requests/limits.
   - Apply only if the cluster has available capacity.

5. **Restart unhealthy pods**
   - If pods are stuck or degraded:
     ```bash
     kubectl rollout restart deployment payment-service -n <namespace>
     ```
   - Use caution if restarts may worsen availability.

6. **Disable suspected feature flags**
   - If the deployment enabled a new payment path or integration, disable it immediately.

7. **Rollback if deployment is strongly correlated**
   - Since the deployment completed 10 minutes before the incident, prepare to roll back quickly if no obvious non-deployment cause is found.

---

## Rollback Strategy

Rollback is recommended if:

- HTTP 500 errors began shortly after the deployment.
- CPU utilization increased after the deployment.
- Pods started restarting after the deployment.
- Logs indicate application errors from the new version.
- Immediate scaling does not stabilize the service.
- No external dependency outage explains the issue.

Rollback steps:

1. **Identify previous stable revision**
   ```bash
   kubectl rollout history deployment/payment-service -n <namespace>
   ```

2. **Rollback to previous revision**
   ```bash
   kubectl rollout undo deployment/payment-service -n <namespace>
   ```

3. **Monitor rollout status**
   ```bash
   kubectl rollout status deployment/payment-service -n <namespace>
   ```

4. **Verify pods are healthy**
   ```bash
   kubectl get pods -n <namespace> -l app=payment-service
   ```

5. **Confirm error rate and CPU return to normal**
   - HTTP 500 rate should decline.
   - CPU should trend back toward baseline.
   - Pod restarts should stop.

6. **Pause further deployments**
   - Disable automatic promotion or progressive rollout until root cause is understood.

If using a deployment platform such as Argo CD, Spinnaker, Flux, or Helm, perform rollback using the approved internal process.

---

## Verification Steps

Verify the incident is resolved by checking:

1. **HTTP error rate**
   - Payment service HTTP 500 rate returns to normal baseline.
   - No sustained spike in 4xx or 5xx responses.

2. **CPU utilization**
   - CPU returns near expected baseline, approximately 35% or within normal operating range.
   - No continued CPU saturation or throttling.

3. **Pod stability**
   - Pods remain in `Running` and `Ready` state.
   - Restart count stops increasing.
   - No CrashLoopBackOff or failed health checks.

4. **Request latency**
   - P95 and P99 latency return to normal.
   - No elevated timeout rate.

5. **Payment success rate**
   - Payment authorization and capture success rates return to expected levels.
   - Failed transaction count decreases.

6. **Application logs**
   - No recurring stack traces.
   - No repeated dependency timeout errors.
   - No fatal process crashes.

7. **Dependency health**
   - Database, cache, payment gateway, and internal service dependencies are healthy.

8. **Synthetic and manual tests**
   - Run synthetic payment flow checks.
   - If safe, execute a test transaction in production using approved procedures.

9. **Customer support signals**
   - Confirm decrease in payment-related complaints or alerts.

---

## Escalation

Escalate immediately if:

- Payment failures are widespread or revenue-impacting.
- HTTP 500 errors remain elevated after initial mitigation.
- CPU remains above 85–90% after scaling.
- Pods continue restarting.
- Rollback fails or does not resolve the issue.
- Database, payment provider, or other critical dependency appears involved.
- There is potential data integrity risk, duplicate charging, or transaction inconsistency.
- Incident exceeds the organization’s SLO or error budget thresholds.

Escalation targets:

- Payment service owning engineering team.
- SRE/on-call platform team.
- Database team, if database latency or errors are observed.
- Network or infrastructure team, if cluster or routing issues are suspected.
- Third-party payment provider support, if provider errors are detected.
- Incident management or leadership for major customer or revenue impact.

---

## References

Review the following dashboards, logs, metrics, and documentation:

### Dashboards

- Payment Service Golden Signals dashboard:
  - Request rate.
  - Error rate.
  - Duration/latency.
  - Saturation.
- Kubernetes workload dashboard:
  - Pod status.
  - Restart count.
  - CPU and memory usage.
  - CPU throttling.
- Deployment dashboard:
  - Recent deployment status.
  - Current and previous versions.
  - Rollout events.
- Payment business metrics dashboard:
  - Payment success rate.
  - Authorization failures.
  - Capture failures.
  - Refund or reversal anomalies.
- Dependency dashboards:
  - Database latency and error rate.
  - Cache hit rate and errors.
  - Queue depth and processing lag.
  - External payment provider status.

### Logs

- Payment service application logs.
- Previous pod logs:
  ```bash
  kubectl logs <pod-name> -n <namespace> --previous
  ```
- Kubernetes events:
  ```bash
  kubectl get events -n <namespace> --sort-by=.metadata.creationTimestamp
  ```
- Ingress or API gateway logs.
- Payment provider API response logs.
- CI/CD deployment logs.

### Metrics

- `http_requests_total` by status code.
- `http_request_duration_seconds`.
- Container CPU usage.
- Container CPU throttling.
- Container memory usage.
- Pod restart count.
- Readiness and liveness probe failures.
- Database query latency.
- External payment provider latency and error rate.
- HPA desired vs current replicas.

### Documentation

- Payment service architecture documentation.
- Payment incident response procedure.
- Deployment and rollback procedure.
- Kubernetes runbook for pod restarts and CrashLoopBackOff.
- Feature flag operation guide.
- External payment provider escalation guide.