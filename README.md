# Zero Trust Network

## Description:
The Zero Trust Network project aims to implement a robust security architecture where no entity, internal or external, is trusted by default. This README provides an overview of the project structure and how to navigate through its components.

## Network Diagram
![alt text](<ZTN Basic Design.png>)

## Sub-repositories:
This Project has 4 main repositorys

1. [TrustEngine](TrustEngine/README.md)
2. [EdgeNode](EdgeNode/README.md)
3. [AdminGUI](AdminGUI/README.md)
4. [PythonAPI](PythonAPI/README.md)

This repository exists to cleanly package all of the repositorys in to one place for development purposes.

## Installation:
Pre-requisites:
- Python 3.10 or higher
- Git (for cloning the repository)
- Windows or Linux OS (Windows is easier for development purposes!)

To clone this repository, run the following command:
```bash
git clone --recursive https://github.com/ZeroTrustNetworkWWU/FlaskPythonZTA
```

Once the repository is cloned, navigate to the root directory and run the following command, It will initialze the python virtual environments, install the dependencys for each and finally start the servers.
```bash
 ./StartServers.bat
 ```
You can use this same script to start the servers after the initial setup.

At this point you should be able to access the EdgeNode at `http://localhost:5005` and login with the default credentials `user1:password1`.

If you want to run the servers individually please refer to the README.md files in each of the sub-repositories.

## Configuration and Setup:
Configuring the network is done by modifying the 
configuration files in the directories of each of the sub-repositories. Specifically the `clientAPIConfig.json` file in the `PythonAPI` directory and the `edgeNodeConfig.json` file in the `EdgeNode` directory. For more information on how to configure the network, please refer to the README.md files in each of the sub-repositories.

## Contributing / Next steps:

-- Convert the StartServers.bat script to a bash script for Linux development

-- Improve the Edge nodes to be able to handle multiple backends
instead of the current single backend. 

-- Remove the ip of the backend from the edge node and instead use the trust engine to determine the backend to use.

-- Convert everything to https. This will require the flask server be run with a certificate and key file. The Admin GUI will also need to be updated to use https.

-- Improve the GUI role selection in the user tab to be more user friendly. Specifically, make a dropdown menu for selecting roles as you must select a valid role for that user.

-- Add a display for logging in the Admin GUI. visualize the traffic in the network.

-- Improve the FetchAPI.kt file in the AdminGUI so it sends more trust data to the trust engine. Potentially split it up and make it a Kotlin API for connecting to the trust engine (much like the PythonAPI).
