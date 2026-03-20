# 🐳 Container Persistence

## 1. Run Base Container
docker run -it --name java_lab ubuntu:22.04 bash

![run container](/Classwork/2_Container_Persistence/Images/image1.png)

---

## 2. Install Java
apt update  
apt install -y openjdk-17-jdk  
javac --version  

![install java](/Classwork/2_Container_Persistence/Images/image2.png)

---

## 3. Create Java Program
mkdir -p /home/app  
cd /home/app  
nano Hello.java  

Paste:
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello from Docker container!");
    }
}

Compile & Run:
javac Hello.java  
java Hello  

![java program](/Classwork/2_Container_Persistence/Images/image3.png)

---

## 4. Exit Container
exit  

![exit](/Classwork/2_Container_Persistence/Images/image4.png)

---

## 5. Commit Container → Image
docker commit java_lab myrepo/java-app:1.0  
docker images  

![commit](/Classwork/2_Container_Persistence/Images/image5.png)

---

## 6. Reuse Image
docker run -it myrepo/java-app:1.0 bash  
cd /home/app  
java Hello  

![reuse](/Classwork/2_Container_Persistence/Images/image6.png)

---

## 7. Save & Load Image
docker save -o java-app.tar myrepo/java-app:1.0  
docker load -i java-app.tar  

![save load](/Classwork/2_Container_Persistence/Images/image7.png)

---

## 8. Export vs Save
docker export java_lab > container.tar  
docker save -o image.tar myrepo/java-app:1.0  

![export vs save](/Classwork/2_Container_Persistence/Images/image8.png)

---

## 9. Dockerfile (Best Practice)

FROM ubuntu:22.04  
RUN apt update && apt install -y openjdk-17-jdk  
WORKDIR /home/app  
COPY Hello.java .  
RUN javac Hello.java  
CMD ["java", "Hello"]

Build:
docker build -t java-app:2.0 .  

![dockerfile](/Classwork/2_Container_Persistence/Images/image9.png)

---

## 10. Key Concepts
- Container → Running environment  
- Image → Snapshot of container  
- docker commit → Container → Image  
- docker save/load → Image ↔ File  
- docker export → Filesystem only (not recommended)