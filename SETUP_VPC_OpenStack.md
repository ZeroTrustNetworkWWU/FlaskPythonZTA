# Setting Up a VPC in OpenStack for the Zero Trust Network

## Overview

This manual provides step-by-step instructions for setting up a Virtual Private Cloud (VPC) in OpenStack with two Virtual Machines (VMs): an Edge Node with internet access and a web UI, and a Trust Engine with exclusive connectivity to the Edge Node.

## Prerequisites

- An active OpenStack account.
- Basic understanding of OpenStack services, including Neutron, Nova, and Horizon.
- SSH client installed for accessing VMs.

## 1. Create a Virtual Private Cloud (VPC)

### Step 1.1: Access Horizon Dashboard
- Log in to the OpenStack Horizon Dashboard.

### Step 1.2: Create a Project (if not already created)
- Navigate to "Project" -> "Compute" -> "Instances".
- Create a new project if needed.

### Step 1.3: Create VPC (Network)
- Go to "Project" -> "Network" -> "Networks".
- Click "Create Network".
- Name your network (e.g., ZeroTrust-VPC) and configure the subnet:
    - Network Address (e.g., 10.0.0.0/16).
    - Enable DHCP.
- Click "Create".

## 2. Set Up Subnets

### Step 2.1: Create Subnets
- Go to "Project" -> "Network" -> "Subnets".
- Click "Create Subnet".
- Name your subnet, select the created network, and enter a CIDR block for the Edge Node (e.g., 10.0.1.0/24).
- Repeat to create a second subnet for the Trust Engine (e.g., 10.0.2.0/24).

## 3. Establish Internet Connectivity

### Step 3.1: Create a Router
- Go to "Project" -> "Network" -> "Routers".
- Click "Create Router".
- Name your router (e.g., ZeroTrust-Router).
- Set the external network to your public network and create the router.

### Step 3.2: Configure Router Interfaces
- Click on the router name.
- Under "Interfaces", add interfaces for both subnets (Edge Node and Trust Engine).

## 4. Launch Instances (VMs)

### Step 4.1: Navigate to Instances Dashboard
- Go to "Project" -> "Compute" -> "Instances".

### Step 4.2: Launch Instances
- Click "Launch Instance".
- Choose an image (AMI equivalent) and instance type (flavor).
- Configure instance details, selecting your VPC and the respective subnets.
- Add storage as needed.
- Configure security groups:
    - Edge Node: Allow HTTP, HTTPS, and SSH.
    - Trust Engine: Allow internal traffic from the Edge Node.
- Review and launch the instances with a key pair.

## 5. Assign Floating IP to Edge Node

### Step 5.1: Allocate and Associate Floating IP
- Go to "Project" -> "Network" -> "Floating IPs".
- Allocate a new floating IP.
- Associate the new address with the Edge Node.

## 6. Configure Edge Node for Web Access
- SSH into the Edge Node using its floating IP.
- Configure the server to host your web UI.

## 7. Verify Configuration

### Step 7.1: Test Internet Access
- Access the Edge Node's web UI from an external browser.

### Step 7.2: Validate Internal Connectivity
- SSH into the Edge Node, then from there to the Trust Engine, ensuring connectivity.

## Conclusion

Following these steps, you should have a VPC with an internet-accessible Edge Node hosting a web UI and a Trust Engine that communicates solely with the Edge Node.
