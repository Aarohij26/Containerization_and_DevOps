# Docker Commands & Flags – HandsOn

## 1. Docker Basics

```bash
docker version
```

![docker version](images/image1.png)

```bash
docker info
```

![docker info](images/image2.png)

## 2. Image Management

```bash
docker images
```

![docker images](images/image3.png)

```bash
docker pull ubuntu
docker pull ubuntu:22.04
```

![docker pull](images/image4.png)

```bash
docker rmi ubuntu
```

![docker rmi](images/image5.png)

## 3. Container Lifecycle

```bash
docker run -it --name test ubuntu bash
```

![docker run](images/image6.png)

```bash
docker ps
```

![docker ps](images/image7.png)

```bash
docker start test
docker stop test
docker restart test
```

![docker lifecycle](images/image8.png)

```bash
docker rm test
```

![docker rm](./Images/image1.png)

## 4. Execute Commands Inside Container

```bash
docker exec -it test bash
```

![docker exec](images/image10.png)

## 5. Networking & Ports

```bash
docker run -d -p 8080:80 nginx
```

![port mapping](images/docker-port.png)

```bash
docker network ls
```

![network list](images/docker-network-ls.png)

```bash
docker network create mynet
```

![network create](images/docker-network-create.png)

## 6. Volumes & Data Persistence

```bash
docker volume create mydata
docker run -v mydata:/data ubuntu
```

![volume](images/docker-volume.png)

## 7. Logs & Monitoring

```bash
docker logs test
```

![logs](images/docker-logs.png)

```bash
docker stats
```

![stats](images/docker-stats.png)

## 8. Inspect & Metadata

```bash
docker inspect test
```

![inspect](images/docker-inspect.png)

## 9. Docker Build

```bash
docker build -t myapp .
```

![build](images/docker-build.png)

Dockerfile:

```Dockerfile
FROM ubuntu:22.04
RUN apt update && apt install -y nginx
CMD ["nginx", "-g", "daemon off;"]
```

![dockerfile](images/dockerfile.png)

## 10. Cleanup Commands

```bash
docker container prune
docker image prune
docker system prune
```

![cleanup](images/docker-cleanup.png)

## 11. Docker Compose

```bash
docker compose up -d --build
docker compose down
```

![compose](images/docker-compose.png)

## 12. Minimal Lab Example

```bash
docker pull nginx
docker run -d --name web -p 8080:80 nginx
docker ps
docker logs web
docker stop web
docker rm web
```

![lab](images/docker-lab.png)

## 13. Key Concepts

Image → Blueprint
Container → Running instance
Volume → Persistent data
Network → Communication
Dockerfile → Build instructions
