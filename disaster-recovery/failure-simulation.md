# SkyNetX Failure Simulation

This file lists safe demo actions to simulate failure and recovery scenarios for the SkyNetX platform.

## Pod Failure
Delete a pod and observe Kubernetes recreate it:

```bash
kubectl delete pod -n skynetx <pod-name>
```

## Bad Deployment Recovery
Undo the current deployment rollout:

```bash
kubectl rollout undo deployment/skynetx-app -n skynetx
```

## Traffic Spike Handling
Scale the deployment manually:

```bash
kubectl scale deployment skynetx-app --replicas=5 -n skynetx
```

## Event Inspection
Review cluster events after a failure:

```bash
kubectl get events -n skynetx
```

## Demo Guidance
- Use non-production test data only.
- Explain each failure before running the command.
- Validate recovery using `kubectl get pods -n skynetx` and the application health endpoint.
