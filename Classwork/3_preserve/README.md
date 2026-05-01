# 🐳 Experiment: How to Preserve Changes Made Inside a Container

## 📌 Objective
Learn how to preserve changes made inside a Docker container by installing software, creating an application, and converting the container into a reusable image.

## 📖 Scenario Overview
In this experiment, you will:
- Start an Ubuntu container
- Install Java (JDK)
- Create a Java program in /home/app
- Convert the modified container into an image
- Reuse and share that image

## 🚀 Step 1: Run Base Ubuntu Container
docker run -it --name java_lab ubuntu:22.04 bash
You are now inside the container.

## ⚙️ Step 2: Install Java Compiler (Inside Container)
apt update
apt install -y openjdk-17-jdk

Verify installation:
javac --version

## 💻 Step 3: Create Java App in /home/app
mkdir -p /home/app
cd /home/app
nano Hello.java

Paste the following code:
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello from Docker container!");
    }
}

Compile and run:
javac Hello.java
java Hello

✔ Now the container has:
- Java installed
- Source file and compiled class in /home/app

## 🔚 Step 4: Exit Container
exit
Container stops, but changes are preserved in the stopped container.

## 📦 Step 5: Convert Container → Image (docker commit)
docker commit java_lab myrepo/java-app:1.0

✔ What happens:
- Container filesystem snapshot is taken
- New reusable image is created

Verify:
docker images

## 🔁 Step 6: Reuse the Exported Image (Locally)
docker run -it myrepo/java-app:1.0 bash

Test:
cd /home/app
java Hello

✔ Java and program already exist.

## 💾 Step 7: Save / Load (Offline Transfer)

Save image to file:
docker save -o java-app.tar myrepo/java-app:1.0

Transfer java-app.tar via USB / SCP.

Load image:
docker load -i java-app.tar

Verify:
docker images

## ⚠️ Important: Export vs Save (Common Confusion)

docker export:
docker export java_lab > container.tar
- Exports filesystem only
- Loses: image name, layers, metadata (CMD, ENTRYPOINT)

docker save (Recommended):
docker save -o image.tar myrepo/java-app:1.0

## 📊 Command Summary
docker commit  → Container → Image
docker save    → Image → File
docker load    → File → Image
docker push/pull → Registry sharing
docker export/import → Raw filesystem only (rare)

## 🧠 Best Practice Note
For real projects, prefer Dockerfile instead of docker commit.

Example:
FROM ubuntu:22.04
RUN apt update && apt install -y openjdk-17-jdk
WORKDIR /home/app
COPY Hello.java .
RUN javac Hello.java
CMD ["java", "Hello"]

Build:
docker build -t java-app:2.0 .

## ✅ One-Line Summary
Modified container → docker commit
Reuse locally → docker run
Share online → docker push/pull
Share offline → docker save/load