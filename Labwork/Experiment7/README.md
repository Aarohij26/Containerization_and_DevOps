# 🚀 CI/CD Pipeline using Jenkins, GitHub & Docker Hub

## 📌 Overview
This project demonstrates a complete CI/CD pipeline using Jenkins for automation, GitHub for source code management, and Docker Hub for container image storage. The pipeline automatically builds and pushes a Docker image whenever code is updated in GitHub.

## 🎯 Aim
To design and implement a CI/CD pipeline that fetches source code from GitHub, builds a Docker image, and pushes the image to Docker Hub.

## 🎯 Objectives
- Understand CI/CD workflow using Jenkins
- Create a structured GitHub repository
- Automate Docker image build & push
- Securely manage credentials in Jenkins
- Trigger builds automatically using webhooks

## ⚙️ Tech Stack
Jenkins (Docker container), GitHub, Docker & Docker Compose, Docker Hub, Python (Flask)

## 📁 Project Structure
my-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile

## 🧠 Concept
CI (Continuous Integration): Automatically builds and tests code after every commit  
CD (Continuous Deployment): Automatically deploys the built application  

Workflow:
Developer → GitHub → Webhook → Jenkins → Build → Docker Hub

## 🛠️ Setup Instructions

### 🔹 Prerequisites
- Docker installed
- Docker Compose installed
- GitHub account
- Docker Hub account

## 🧩 Part A: GitHub Setup

### 1. Create Repository
Create a repository named: my-app

### 2. Application Code (app.py)
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from CI/CD Pipeline!"

app.run(host="0.0.0.0", port=80)

### 3. requirements.txt
flask

### 4. Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "app.py"]

### 5. Jenkinsfile
pipeline {
    agent any
    environment {
        IMAGE_NAME = "your-dockerhub-username/myapp"
    }
    stages {
        stage('Clone Source') {
            steps {
                git 'https://github.com/your-username/my-app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }
        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
                    sh 'echo $DOCKER_TOKEN | docker login -u your-dockerhub-username --password-stdin'
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                sh 'docker push $IMAGE_NAME:latest'
            }
        }
    }
}

## 🐳 Part B: Jenkins Setup (Docker)

### docker-compose.yml
version: '3.8'
services:
  jenkins:
    image: jenkins/jenkins:lts
    container_name: jenkins
    restart: always
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    user: root
volumes:
  jenkins_home:

### Run Jenkins
docker-compose up -d

Access: http://localhost:8080

## ⚙️ Part C: Jenkins Configuration
- Go to Manage Jenkins → Credentials → Add Credentials
- Type: Secret Text
- ID: dockerhub-token
- Value: Docker Hub Access Token

Create Pipeline Job:
- New Item → Pipeline
- Pipeline script from SCM
- Add GitHub repo URL
- Script Path: Jenkinsfile

## 🔗 Part D: GitHub Webhook
- Go to GitHub → Settings → Webhooks → Add Webhook
- Payload URL: http://<your-server-ip>:8080/github-webhook/
- Select Push Events

## 🔄 Execution Flow
1. Developer pushes code to GitHub
2. Webhook triggers Jenkins
3. Jenkins pipeline runs:
   - Clone code
   - Build Docker image
   - Login to Docker Hub
   - Push image
4. Docker image is available globally

## 🔐 withCredentials Explained
withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
    sh 'echo $DOCKER_TOKEN | docker login -u username --password-stdin'
}
This ensures secure handling of secrets without hardcoding passwords.

## 📊 Observations
- Jenkins simplifies CI/CD automation
- GitHub manages source code and pipeline definition
- Docker ensures consistent builds
- Webhooks enable full automation

## ✅ Result
Successfully implemented a CI/CD pipeline where code is automatically fetched, Docker image is built, and securely pushed to Docker Hub.

## ❓ Viva Questions
- What is Jenkinsfile?
- What is a webhook?
- Why use Docker in CI/CD?
- How are credentials secured in Jenkins?
- What is the role of Docker socket?

## 🧾 Key Takeaways
- CI/CD improves development speed
- Jenkins pipelines are code-driven
- Always store secrets securely
- Automation reduces manual effort