# 📘 Experiment 9: Ansible

## 🧩 Problem Statement
Managing infrastructure manually across multiple servers leads to configuration drift, inconsistent environments, and repetitive tasks. Scaling becomes difficult with manual SSH-based administration.

---

## 🚀 What is Ansible?
Ansible is an open-source automation tool used for configuration management, application deployment, and orchestration.

Features:
- Agentless (uses SSH)
- YAML-based playbooks
- Idempotent (safe to run multiple times)
- Push-based architecture

---

## ⚙️ Key Concepts

Component        Description
Control Node     Machine with Ansible installed
Managed Nodes    Target servers
Inventory        List of servers
Playbooks        YAML automation files
Tasks            Individual actions
Modules          Built-in functionalities
Roles            Reusable scripts

---

## 🔄 How Ansible Works
- Control node connects to managed nodes via SSH
- Executes modules through tasks
- Tasks grouped into playbooks
- Inventory defines servers

---

## ✅ Benefits
- Free & open source
- Easy to use
- No agents required
- Scalable
- Strong community support

---

# 🧪 Part A: Installation

## Install via pip
```bash
pip install ansible
```
![Install](./1.png)

```bash
ansible --version
```
![Version](./2.png)

## Install via apt
```bash
sudo apt update -y
```
![Version](./3.png)

```bash
sudo apt install ansible -y
```
![Version](./4.png)

## Test Installation
```bash
ansible localhost -m ping
```
![Version](./5.png)

Expected Output:
"ping": "pong"

---

# 🐳 Docker + SSH Setup

## Generate SSH Key
```bash
ssh-keygen -t rsa -b 4096
```
![Version](./6.png)

```bash
cp ~/.ssh/id_rsa.pub .
cp ~/.ssh/id_rsa .
```
![Version](./7.png)

---

## Create Dockerfile
```bash
FROM ubuntu

RUN apt update -y
RUN apt install -y python3 python3-pip openssh-server
RUN mkdir -p /var/run/sshd

RUN mkdir -p /run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

COPY id_rsa /root/.ssh/id_rsa
COPY id_rsa.pub /root/.ssh/authorized_keys

RUN chmod 600 /root/.ssh/id_rsa && chmod 644 /root/.ssh/authorized_keys

RUN sed -i 's@session\\s*required\\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
```
![Version](./8.png)
![Version](./9.png)

---

## Build Image
```bash
docker build -t ubuntu-server .
```
![Version](./10.png)

## Run Container
```bash
docker run -d -p 2222:22 --name ssh-test-server ubuntu-server
```
![Version](./12.png)

## Get Container IP
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ssh-test-server
```
![Version](./13.png)

---

## Test SSH

```bash
Password:
ssh root@localhost -p 2222
```
![Version](./14.png)

```bash
Key-based:
ssh -i ~/.ssh/id_rsa root@localhost -p 2222
```
![Version](./15.png)

---

# ⚡ Ansible with Docker

## Run Multiple Servers
```bash
for i in {1..4}; do
  docker run -d -p 220${i}:22 --name server${i} ubuntu-server
done
```
![Version](./16.png)

---

## Create Inventory
```bash
echo "[servers]" > inventory.ini
```
![Version](./19.png)

```bash
for i in {1..4}; do
  docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server${i} >> inventory.ini
done
```
![Version](./17.png)
```bash
cat << EOF >> inventory.ini
 
[servers:vars]
ansible_user=root
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
EOF
```
![Version](./20.png)

---

## Test Connectivity
```bash
ansible all -i inventory.ini -m ping
```
![Version](./19.png)

---

## Create Playbook (playbook1.yml)
```bash
---
- name: Update and configure servers
  hosts: all
  become: yes

  tasks:
    - name: Update apt packages
      apt:
        update_cache: yes
        upgrade: dist

    - name: Install packages
      apt:
        name: ["vim", "htop", "wget"]
        state: present

    - name: Create test file
      copy:
        dest: /root/ansible_test.txt
        content: "Configured by Ansible on {{ inventory_hostname }}"
```
![Version](./20.png)

---

## Run Playbook
```bash
ansible-playbook -i inventory.ini playbook1.yml
```
![Version](./21.png)

---

## Verify Output
```bash
ansible all -i inventory.ini -m command -a "cat /root/ansible_test.txt"
```
![Version](./22.png)

---

## Cleanup
```bash
for i in {1..4}; do docker rm -f server${i}; done
```
![Version](./23.png)

---

# 📊 Need for Ansible
- Scalability
- Consistency
- Efficiency
- Idempotency
- Infrastructure as Code

---

# ⭐ Key Features
- Agentless
- Idempotent
- YAML-based
- Large module library
- Push-based

---

# 🎯 Conclusion
Ansible simplifies server management by automating repetitive tasks, ensuring consistency, and enabling scalable infrastructure management.
