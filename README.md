# Hangman
## This Application is the classic game "Hangman" o "Ahorcado" in spanish developed in Python with Flask and implemented with Devops Practices.


![N|Devops](https://github.com/diegokalpa/ahorcado_webserver_devops/blob/main/devopscycle.png?raw=true)


#### Plan: Notion
#### Code: Python + Flask
#### Build: Github - Git
#### CI/CD: Github Actions
#### Deploy: Terraform
#### Cloud: GCP + GKE
#### Monitoring: Istio + Grafana + Prometheus

## Features

- How to create an APP with Python and Flask - Here (https://github.com/diegokalpa/curso_python_intermedio)
- Docker and minikube utilities used locally (https://docs.docker.com/desktop/install/mac-install/) (https://minikube.sigs.k8s.io/docs/start/)
- Connect to GCP Cluster created before (https://github.com/diegokalpa/website-GCP-TERRA)
- Integrate ISTIO, Grafana and Prometheus (https://github.com/diegokalpa/istio-service-mesh)

## Installation

### 1. Build Dockerfile and push to DockerHUB

```FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt requirements.txt 
COPY venv/archivos/data.txt venv/
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=venv/"ahorcado.py"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

### 2. Build deployment.yaml file
(https://github.com/diegokalpa/ahorcado_webserver_devops/blob/main/k8s/deployment.yaml)

```
#Creacion de Namespace

apiVersion: v1
kind: Namespace
metadata:
  name: ns-ahorcado
  labels:
    app: label-ahorcado

---
#Creacion de Deployment

apiVersion: apps/v1
kind: Deployment
metadata:
  name: ahorcado-app
  namespace: ns-ahorcado
spec:
  replicas: 3
  selector:
    matchLabels:
      app: label-ahorcado
  template:                     #Desde aqui se construye el pod
    metadata:
      labels:
        app: label-ahorcado
    spec:
      containers:
      - name: ahorcado
        image: diegokalpa/ahorcado:v2
        ports:
        - containerPort: 80

---

#Aqui empieza a crearse el servicio de tipo ClusterIP

apiVersion: v1
kind: Service
metadata:
  name: svc-ahorcado
  namespace: ns-ahorcado
  labels:
    app: label-ahorcado
spec:
  type: ClusterIP
  selector:
    app: label-ahorcado
  ports:
    - protocol: TCP
      port: 80

---

apiVersion: v1
kind: Service
metadata:
  name: svc-nodeport-ahorcado
  namespace: ns-ahorcado
  labels:
    app: label-ahorcado
spec:
  type: NodePort
  selector:
    app: label-ahorcado
  ports:
    - protocol: TCP
      port:       80        #puerto donde estara escuchando el servicio
      targetPort: 5000      #puerto donde escucha la app

---

#Se crea LoadBalancer para poder acceder a Grafana desde afuera.
apiVersion: v1
kind: Service
metadata:
  name: lb-grafana
  namespace: istio-system
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 3000
  selector:
    app: grafana
---

#Se crea LoadBalancer para poder acceder a Grafana desde afuera.
apiVersion: v1
kind: Service
metadata:
  name: lb-prometheus
  namespace: istio-system
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 9090
  selector:
    app: prometheus
```

### 3. Create Workflow.yaml for Github Actions:
(https://github.com/diegokalpa/ahorcado_webserver_devops/blob/main/.github/workflows/deploy_gke.yml)
```
#Creacion de Namespace

apiVersion: v1
kind: Namespace
metadata:
  name: ns-ahorcado
  labels:
    app: label-ahorcado

---
#Creacion de Deployment

apiVersion: apps/v1
kind: Deployment
metadata:
  name: ahorcado-app
  namespace: ns-ahorcado
spec:
  replicas: 3
  selector:
    matchLabels:
      app: label-ahorcado
  template:                     #Desde aqui se construye el pod
    metadata:
      labels:
        app: label-ahorcado
    spec:
      containers:
      - name: ahorcado
        image: diegokalpa/ahorcado:v2
        ports:
        - containerPort: 80

---
#Aqui empieza a crearse el servicio de tipo ClusterIP

apiVersion: v1
kind: Service
metadata:
  name: svc-ahorcado
  namespace: ns-ahorcado
  labels:
    app: label-ahorcado
spec:
  type: ClusterIP
  selector:
    app: label-ahorcado
  ports:
    - protocol: TCP
      port: 80

---

apiVersion: v1
kind: Service
metadata:
  name: svc-nodeport-ahorcado
  namespace: ns-ahorcado
  labels:
    app: label-ahorcado
spec:
  type: NodePort
  selector:
    app: label-ahorcado
  ports:
    - protocol: TCP
      port:       80        #puerto donde estara escuchando el servicio
      targetPort: 5000      #puerto donde escucha la app
```

### 4. Installing Istio and Monitoring tools:

after following the previous steps add two Load Balancer Services more one for Grafana and another for Prometheus:

```
apiVersion: v1
kind: Service
metadata:
  name: lb-grafana
  namespace: istio-system
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 3000
  selector:
    app: grafana
    
#Se crea LoadBalancer para poder acceder a Prometheus desde afuera.
apiVersion: v1
kind: Service
metadata:
  name: lb-prometheus
  namespace: istio-system
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 9090
  selector:
    app: prometheus    
```
![N|Grafana](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/c26f65d4-5fb6-4ea9-b9c1-4c3cb23ade68/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230320%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230320T191204Z&X-Amz-Expires=86400&X-Amz-Signature=09f88186f4a874e7382adf995aec39041171ef2620f9133b8b839cd8034de026&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22Untitled.png%22&x-id=GetObject)

![N|Prometheus](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/f0a98626-9dcf-4e8f-b89a-4801aaf4bb6e/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230320%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230320T191359Z&X-Amz-Expires=86400&X-Amz-Signature=c834c51f32c76aaf95c7d57ddf0f0af70086a5d84748cc692fe0e4543d325cfa&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22Untitled.png%22&x-id=GetObject)

### Workloads:

![N|Workloads](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/b4114f86-b904-4d47-b715-c9521ccbaf48/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230320%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230320T191831Z&X-Amz-Expires=86400&X-Amz-Signature=29159215c4e42d95bef0525b9a34ea4b65d27a272dc50b2c6674396f70e3045b&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22Untitled.png%22&x-id=GetObject)


### Service and Ingress:

![N|Prometheus](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/d15c3531-df74-40e2-bbb9-23d3f01a5061/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230320%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230320T191621Z&X-Amz-Expires=86400&X-Amz-Signature=1ffb0af93104544aec4b212bdcfe0c1428ecd69e17720a10c3cb02b26ff9e52b&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22Untitled.png%22&x-id=GetObject)


## License

MIT

**Free Software, Hell Yeah!**

