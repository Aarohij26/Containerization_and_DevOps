# 🚀 Experiment 4: Docker Essentials

This experiment demonstrates Docker basics: containerizing apps, building images, running containers, multi-stage builds, and publishing to Docker Hub.

--------------------------------------------------

## 🐍 Part 1: Flask Application

### Create App
mkdir flaskapp
cd flaskapp
![Creaation](./Images/1.png)

app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Docker!"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

requirements.txt
Flask==2.3.3

### Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]

📸 Screenshot:
(Add Dockerfile screenshot)

--------------------------------------------------

## 🚫 Part 2: .dockerignore

__pycache__/
*.pyc
.env
venv/
.vscode/
.git/
.DS_Store
*.log
tests/

📸 Screenshot:
(Add .dockerignore screenshot)

Why:
- Reduces image size
- Faster builds
- Better security

--------------------------------------------------

## 🏗️ Part 3: Build Images

docker build -t my-flask-app .

📸 Screenshot:
(Add build output screenshot)

docker build -t my-flask-app:1.0 .

📸 Screenshot:
(Add version build screenshot)

docker build -t my-flask-app:latest -t my-flask-app:1.0 .

📸 Screenshot:
(Add multi-tag screenshot)

docker images

📸 Screenshot:
(Add image list screenshot)

--------------------------------------------------

## ▶️ Part 4: Run Containers

docker run -d -p 5000:5000 --name flask-container my-flask-app

📸 Screenshot:
(Add running container screenshot)

curl http://localhost:5000

📸 Screenshot:
(Add browser/curl output)

docker logs flask-container

📸 Screenshot:
(Add logs screenshot)

### Manage

docker stop flask-container  
📸 Screenshot:

docker start flask-container  
📸 Screenshot:

docker rm flask-container  
📸 Screenshot:

docker rm -f flask-container  
📸 Screenshot:

--------------------------------------------------

## ⚡ Part 5: Multi-stage Build

FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY app.py .
RUN useradd -m appuser
USER appuser
EXPOSE 5000
CMD ["python", "app.py"]

📸 Screenshot:
(Add multi-stage Dockerfile screenshot)

Build:

docker build -t flask-regular .
📸 Screenshot:

docker build -f Dockerfile.multistage -t flask-multistage .
📸 Screenshot:

docker images | grep flask
📸 Screenshot:

--------------------------------------------------

## ☁️ Part 6: Docker Hub

docker login
📸 Screenshot:

docker tag my-flask-app username/my-flask-app:1.0
📸 Screenshot:

docker push username/my-flask-app:1.0
📸 Screenshot:

Pull:

docker pull username/my-flask-app:latest
📸 Screenshot:

docker run -d -p 5000:5000 username/my-flask-app:latest
📸 Screenshot:

--------------------------------------------------

## 🟢 Part 7: Node.js Example

docker build -t my-node-app .
📸 Screenshot:

docker run -d -p 3000:3000 --name node-container my-node-app
📸 Screenshot:

curl http://localhost:3000
📸 Screenshot:

--------------------------------------------------

## 🧪 Part 8: Practice

docker build -t myapp:latest -t myapp:v2.0 -t username/myapp:production .
📸 Screenshot:

docker build --no-cache -t clean-app .
📸 Screenshot:

--------------------------------------------------

## 📌 Docker Cheatsheet

docker build     -> Build image  
docker run       -> Run container  
docker ps        -> List containers  
docker images    -> List images  
docker tag       -> Tag image  
docker push      -> Push image  
docker pull      -> Pull image  
docker rm        -> Remove container  
docker rmi       -> Remove image  
docker logs      -> View logs  
docker exec      -> Run command  

--------------------------------------------------

## 🔄 Workflow

Development:

docker build -t myapp .
📸 Screenshot:

docker run -p 8080:8080 myapp
📸 Screenshot:

docker tag myapp myapp:v1.0
📸 Screenshot:

docker push myapp:v1.0
📸 Screenshot:

Production:

docker pull myapp:v1.0
📸 Screenshot:

docker run -d -p 80:8080 myapp:v1.0
📸 Screenshot:

docker logs -f myapp
📸 Screenshot:

--------------------------------------------------

## 🎯 Key Takeaways

- Dockerfile builds images
- .dockerignore improves speed & security
- Tagging helps versioning
- Multi-stage reduces size
- Docker Hub for sharing
- Always test locally

--------------------------------------------------

## 🧹 Cleanup

docker container prune
📸 Screenshot:

docker image prune
📸 Screenshot:

docker system prune -a
📸 Screenshot: