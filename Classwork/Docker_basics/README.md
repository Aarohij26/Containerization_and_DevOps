# Docker Commands & Flags – HandsOn

## 1. Docker Basics

```bash
docker version
```

![docker version](/Classwork/Docker_basics/Images/image1.png)

```bash
docker info
```

![docker info](/Classwork/Docker_basics/Images/image2.png)

## 2. Image Management

```bash
docker images
```

![docker images](/Classwork/Docker_basics/Images/image3.png)

```bash
docker pull ubuntu
docker pull ubuntu:22.04
```

![docker pull](/Classwork/Docker_basics/Images/image4.png)

```bash
docker rmi ubuntu
```

![docker rmi](/Classwork/Docker_basics/Images/image5.png)

## 3. Container Lifecycle

```bash
docker run -it --name test ubuntu bash
```

![docker run](/Classwork/Docker_basics/Images/image6.png)

```bash
docker ps
```

![docker ps](/Classwork/Docker_basics/Images/image7.png)

```bash
docker start test
docker stop test
docker restart test
```

![docker lifecycle](/Classwork/Docker_basics/Images/image8.png)

```bash
docker rm test
```

![docker rm](/Classwork/Docker_basics/Images/image9.png)

## 4. Execute Commands Inside Container

```bash
docker exec -it test bash
```

![docker exec](/Classwork/Docker_basics/Images/image10.png)

## 5. Networking & Ports

```bash
docker run -d -p 8080:80 nginx
```

![port mapping](/Classwork/Docker_basics/Images/image11.png)

```bash
docker network ls
```

![network list](/Classwork/Docker_basics/Images/image12.png)

```bash
docker network create mynet
```

![network create](/Classwork/Docker_basics/Images/image13.png)

## 6. Volumes & Data Persistence

```bash
docker volume create mydata
docker run -v mydata:/data ubuntu
```

![volume](/Classwork/Docker_basics/Images/image14.png)

## 7. Logs & Monitoring

```bash
docker logs test
```

![logs](/Classwork/Docker_basics/Images/image15.png)

```bash
docker stats
```

![stats](/Classwork/Docker_basics/Images/image16.png)

## 8. Inspect & Metadata

```bash
docker inspect test
```

![inspect](/Classwork/Docker_basics/Images/image17.png)

## 9. Docker Build

```bash
docker build -t myapp .
```

![build](/Classwork/Docker_basics/Images/image18.png)

Dockerfile:

```Dockerfile
FROM ubuntu:22.04
RUN apt update && apt install -y nginx
CMD ["nginx", "-g", "daemon off;"]
```

![dockerfile](/Classwork/Docker_basics/Images/image19.png)


## 10. Minimal Lab Example

```bash
docker pull nginx
docker run -d --name web -p 8080:80 nginx
docker ps
docker logs web
docker stop web
docker rm web
```

![lab](/Classwork/Docker_basics/Images/image20.png)

## 11. Key Concepts

Image → Blueprint
Container → Running instance
Volume → Persistent data
Network → Communication
Dockerfile → Build instructions
