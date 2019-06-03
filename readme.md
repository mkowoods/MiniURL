# MiniURL

----

Yet another URL Shortening Application.
The application has deployments in both `docker-compose` and `kubernetes`, this was built mostly to learn the different methods for deploying application clusters.

Also, demos integration of `node/express` (Client), `flask` (API), `postgres` (Persistence Layer) and `redis` (Cache Layer) 

## Docker Deployment:
```
docker-compose up --build -d --remove-orphans   # Run the container
docker-compose down -v --remove-orphans  # Stop and shutdown
``` 
## Kubernetes Deployment:
```
kubectl apply -f ./k8s/postgres-volumeclaim.yaml
kubectl apply -f ./k8s/postgres.yaml
kubectl rollout status -f ./k8s/postgres.yaml

kubectl apply -f ./k8s/redis.yaml
kubectl rollout status -f ./k8s/redis.yaml

kubectl apply -f ./k8s/miniurl-backend.yaml
kubectl apply -f ./k8s/miniurl-frontend.yaml
```


#### Good References 
 - https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3
