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
sudo apt update -y
📸 Add Screenshot Here

sudo apt install ansible -y
📸 Add Screenshot Here

ansible --version
📸 Add Screenshot Here

## Test Installation
ansible localhost -m ping
📸 Add Screenshot Here

Expected Output:
"ping": "pong"

---

# 🐳 Docker + SSH Setup

## Generate SSH Key
ssh-keygen -t rsa -b 4096
📸 Add Screenshot Here

cp ~/.ssh/id_rsa.pub .
cp ~/.ssh/id_rsa .
📸 Add Screenshot Here

---

## Create Dockerfile

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

📸 Add Screenshot Here

---

## Build Image
docker build -t ubuntu-server .
📸 Add Screenshot Here

## Run Container
docker run -d -p 2222:22 --name ssh-test-server ubuntu-server
📸 Add Screenshot Here

## Get Container IP
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ssh-test-server
📸 Add Screenshot Here

---

## Test SSH

Password:
ssh root@localhost -p 2222
📸 Add Screenshot Here

Key-based:
ssh -i ~/.ssh/id_rsa root@localhost -p 2222
📸 Add Screenshot Here

---

# ⚡ Ansible with Docker

## Run Multiple Servers
for i in {1..4}; do
  docker run -d -p 220${i}:22 --name server${i} ubuntu-server
done
📸 Add Screenshot Here

---

## Create Inventory
echo "[servers]" > inventory.ini
📸 Add Screenshot Here

for i in {1..4}; do
  docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server${i} >> inventory.ini
done
📸 Add Screenshot Here

cat << EOF >> inventory.ini

[servers:vars]
ansible_user=root
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
EOF

📸 Add Screenshot Here

---

## Test Connectivity
ansible all -i inventory.ini -m ping
📸 Add Screenshot Here

---

## Create Playbook (playbook1.yml)

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

📸 Add Screenshot Here

---

## Run Playbook
ansible-playbook -i inventory.ini playbook1.yml
📸 Add Screenshot Here

---

## Verify Output
ansible all -i inventory.ini -m command -a "cat /root/ansible_test.txt"
📸 Add Screenshot Here

---

## Cleanup
for i in {1..4}; do docker rm -f server${i}; done
📸 Add Screenshot Here

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
