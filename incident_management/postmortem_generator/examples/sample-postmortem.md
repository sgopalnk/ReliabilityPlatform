# Incident Postmortem

## Incident Summary
On 2026-08-15, the payment-service experienced elevated HTTP 500 errors starting at approximately 10:02 UTC. Application logs showed repeated database connection timeout errors, and database monitoring showed the application connection pool operating near its configured maximum. Traffic to the payment-service was temporarily reduced at 10:14 UTC, after which error rates declined and payment success rates returned to normal by 10:22 UTC.

## Impact
Some customers were unable to complete payment transactions between approximately 10:02 UTC and 10:22 UTC.

## Timeline
- **2026-08-15T10:02:00Z** — Monitoring detected an increase in HTTP 500 responses from the payment-service.
  - Evidence: Monitoring detected an increase in HTTP 500 responses from the payment-service.
  - Evidence: HTTP 500 error rate increased sharply.
- **2026-08-15T10:04:00Z** — The on-call engineer acknowledged the alert.
  - Evidence: On-call engineer acknowledged the alert.
  - Evidence: The on-call engineer acknowledged the alert within two minutes.
- **2026-08-15T10:07:00Z** — Application logs showed repeated database connection timeout errors.
  - Evidence: Application logs showed repeated database connection timeout errors.
  - Evidence: Database connection timeout errors were present in application logs.
- **2026-08-15T10:10:00Z** — Database monitoring showed the application connection pool operating near its configured maximum.
  - Evidence: Database monitoring showed the application connection pool operating near its configured maximum.
  - Evidence: Connection pool utilization was near its configured maximum.
- **2026-08-15T10:14:00Z** — Traffic to the payment-service was temporarily reduced.
  - Evidence: Traffic to the payment-service was temporarily reduced.
- **2026-08-15T10:17:00Z** — Error rates began to decline.
  - Evidence: Error rates began to decline.
  - Evidence: Error rates decreased after traffic was reduced.
- **2026-08-15T10:22:00Z** — Payment success rates returned to normal.
  - Evidence: Payment success rates returned to normal.

## Root Cause
**Status:** hypothesis

Database connection pool exhaustion may have contributed to payment-service failures, but the available evidence does not conclusively establish it as the confirmed root cause.

**Evidence:**
- Application logs showed repeated database connection timeout errors.
- Database monitoring showed the application connection pool operating near its configured maximum.
- The available evidence suggests database connection pool exhaustion may have contributed to the failures.
- The investigation has not yet conclusively established this as the confirmed root cause.

## Contributing Factors
- The application connection pool was operating near its configured maximum.
- Database connection timeout errors were present in application logs.
- No dedicated alert existed for connection pool saturation.
- Engineers had to manually correlate application logs and database metrics.

## What Went Well
- Monitoring detected the incident quickly.
- The on-call engineer acknowledged the alert within two minutes.
- Reducing traffic to the payment-service was followed by declining error rates.
- Payment success rates returned to normal by 10:22 UTC.

## What Went Poorly
- Some customers were unable to complete payment transactions.
- Engineers had to manually correlate application logs and database metrics.
- No dedicated alert existed for connection pool saturation.
- The root cause was not conclusively established from the available evidence.

## Corrective Actions
- **Add a dedicated alert for payment-service database connection pool saturation.** — No dedicated alert existed for connection pool saturation, and connection pool utilization was observed near its configured maximum during the incident.
- **Create a dashboard or runbook view that correlates payment-service HTTP 500 rates, database connection timeout logs, and connection pool utilization.** — Engineers had to manually correlate application logs and database metrics during the response.
- **Continue the investigation to determine whether connection pool exhaustion was the root cause or only a contributing factor.** — The evidence suggests connection pool exhaustion may have contributed, but it has not been conclusively established as the confirmed root cause.

## Preventive Actions
- **Define and monitor thresholds for connection pool utilization before it reaches the configured maximum.** — Connection pool utilization was near its configured maximum, and earlier visibility could reduce time to detect saturation conditions.
- **Review payment-service behavior under high connection pool utilization and database connection timeouts.** — The incident included database connection timeout errors and elevated HTTP 500 responses, indicating a need to understand and reduce the impact of similar conditions.
- **Document the traffic reduction mitigation procedure for payment-service incidents involving elevated 500 errors and suspected database connection pressure.** — Traffic reduction was followed by a decline in error rates, and documenting the procedure can help responders apply the mitigation consistently when appropriate.

## Lessons Learned
- HTTP 500 error alerts can detect user-facing symptoms quickly, but supporting alerts for underlying resource saturation are needed for faster diagnosis.
- Manual correlation across logs and metrics slows incident analysis.
- Connection pool saturation is a plausible failure mode for payment-service availability and should be directly monitored and investigated.
