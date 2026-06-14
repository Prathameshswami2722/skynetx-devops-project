# SkyNetX Kubernetes Deployment

This folder contains simple Kubernetes manifests for deploying the existing SkyNetX Flask Docker application in a local college DevOps demonstration setup.

## Files
- `namespace.yaml`
- `configmap.yaml`
- `secret.yaml`
- `deployment.yaml`
- `service.yaml`
- `hpa.yaml`

## Apply All Kubernetes Files
Run these commands from the project root directory:

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml
```

You can also apply the entire folder:

```bash
kubectl apply -f kubernetes/
```

## Verify the Deployment
Check the namespace:

```bash
kubectl get namespaces
```

Check the pods:

```bash
kubectl get pods -n skynetx
```

Check the deployment:

```bash
kubectl get deployment -n skynetx
```

Check the service:

```bash
kubectl get service -n skynetx
```

Check the Horizontal Pod Autoscaler:

```bash
kubectl get hpa -n skynetx
```

## Access the Application
Because the service type is `NodePort`, access the SkyNetX Flask application using:

```text
http://localhost:30080
```

You can also verify the health endpoint:

```text
http://localhost:30080/health
```

And the Prometheus metrics endpoint:

```text
http://localhost:30080/metrics
```

## Troubleshooting Note
If you are using Docker Desktop Kubernetes with a local Docker image such as `skynetx-app:1.0`, Kubernetes may fail to start the pod if it cannot find the image in the expected local image store.

Important note:
- When using a local Docker image with Docker Desktop Kubernetes, `imagePullPolicy: IfNotPresent` should be used so Kubernetes can use the locally available image instead of trying to pull it from a remote registry.

If pods are not starting, inspect them with:

```bash
kubectl describe pod -n skynetx
```

Check pod logs with:

```bash
kubectl logs -n skynetx -l app=skynetx-app
```
