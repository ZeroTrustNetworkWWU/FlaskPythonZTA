# Instructions Manual: Setting Up a VPC in AWS with for the Zero Trust Network

## Overview

This manual provides step-by-step instructions for setting up a Virtual Private Cloud (VPC) in AWS with two Virtual Machines (VMs): an Edge Node with internet access and a web UI, and a Trust Engine with exclusive connectivity to the Edge Node.

## Prerequisites

- An active AWS account.
- Basic understanding of AWS services, including VPC, EC2, and IAM.
- SSH client installed for accessing VMs.

## 1. Create a Virtual Private Cloud (VPC)

### Step 1.1: Access VPC Dashboard
- Log in to the AWS Management Console.
- Navigate to the "VPC" service.

### Step 1.2: Create VPC
- Click on "Your VPCs" in the navigation pane.
- Select "Create VPC".
- Name your VPC and specify a CIDR block (e.g., 10.0.0.0/16).
- Click "Create".

## 2. Set Up Subnets

### Step 2.1: Create Subnets
- Go to "Subnets" in the VPC dashboard.
- Click "Create subnet".
- Name your subnet, select the created VPC, and enter a CIDR block for the Edge Node (e.g., 10.0.1.0/24).
- Repeat to create a second subnet for the Trust Engine (e.g., 10.0.2.0/24).

## 3. Establish Internet Connectivity

### Step 3.1: Create Internet Gateway
- Select "Internet Gateways" on the VPC dashboard.
- Click "Create internet gateway", name it, and create.
- Attach it to your VPC.

### Step 3.2: Configure Route Tables
- Create a route table for your VPC, associate it with the Edge Node's subnet.
- Add a route (0.0.0.0/0) directed to the internet gateway.

## 4. Launch EC2 Instances (VMs)

### Step 4.1: Navigate to EC2 Dashboard
- Open the "EC2" service from the AWS Management Console.

### Step 4.2: Launch Instances
- Click "Launch Instance".
- Choose an AMI and instance type.
- Configure instance details, selecting your VPC and the respective subnets.
- Add storage as needed.
- Configure security groups:
    - Edge Node: Allow HTTP, HTTPS, and SSH.
    - Trust Engine: Allow internal traffic from the Edge Node.
- Review and launch the instances with a key pair.

## 5. Assign Elastic IP to Edge Node

### Step 5.1: Allocate and Associate Elastic IP
- In the EC2 dashboard, select "Elastic IPs" -> "Allocate new address".
- Associate the new address with the Edge Node.

## 6. Configure Edge Node for Web Access
- SSH into the Edge Node using its Elastic IP.
- Configure the server to host your web UI.

## 7. Verify Configuration

### Step 7.1: Test Internet Access
- Access the Edge Node's web UI from an external browser.

### Step 7.2: Validate Internal Connectivity
- SSH into the Edge Node, then from there to the Trust Engine, ensuring connectivity.

## Conclusion

Following these steps, you should have a VPC with an internet-accessible Edge Node hosting a web UI and a Trust Engine that communicates solely with the Edge Node.

## Troubleshooting

### Issue: Unable to connect to the Trust Engine from the Edge Node.
- Solution: Verify the security group for the Trust Engine allows inbound connections from the Edge Node.

