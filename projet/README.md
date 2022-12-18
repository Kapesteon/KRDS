
# Remote Desktop For IT Student on Kubernetes Project
## Description

This is a student project required by UQAC for the course of cloud computing <br>
This project aims to offer a ready-to-install solution easily scalable to allow student to <br>
connect to remote desktop via their browser (So that every student have the same desktop environnement, <br>
software and configs hosted on a stateless Kubernetes pod)

## Installation


You will need a machine that will be hosting the kubernetes client <br>
or subscribe to cloud provider solution (AWS, GKE etc...) <br>
For our case we will go over a local installation using [**microk8s**](https://microk8s.io/) on a linux environnement<br>

### Download

- 1 - Download this repository 


### Microk8s
- 1 - Install microk8s using snap ([**Snap installation**](https://snapcraft.io/docs/installing-snapd))

      sudo snap install microk8s --classic


- 2 - Give the user the permission to run commands

      sudo usermod -a -G microk8s $USER
      sudo chown -f -R $USER ~/.kube
        
        

- 3 - Check if the installation is complete 

      microk8s status --wait-ready
        

- 4 - Create a snap alias 

      sudo snap alias microk8s.kubectl kubectl
        

- 5 - Test if kubectl works

      kubectl get nodes


- 6 - Install microk8s addons (the last is optional)


      microk8s enable dns
      microk8s enable registry
      microk8s enable dashboard


### Docker
- 1 - You will need to use docker in order to build docker image from dockerfile \
Because docker's installation varies per Linux distro and require kernel modules, follow this [**tutorial**](https://docs.docker.com/desktop/install/linux-install/)

- 2 - Once docker is intalled, in a terminal, use `cd` to go to the docker folder of this project

- 3 - Make sure the docker service is up and running

      sudo systemctl start docker.service

- 4 - Use the the following command to build the docker image and push to the local registry \

        ./build_docker_image.sh 

### Python
You will also need to run python on nodes machines and install dependencies

1 - Install python

2 - sudo pip3 install flask-restful 

3 - sudo pip3 install kubernetes 

4 - sudo pip3 install tabulate

5 - sudo pip3 install flask

6 - sudo pip3 install git+https://github.com/rqlite/pyrqlite.git


### Database initialisation
From the project folder. You will need to run the command:

      ./db/server/install_db_server.sh
Then you can start it with your ip address (default is localhost):

      ./db/server/start_db_server.sh <your IP>
You should see a database printed in the terminal with 3 default users created, with credentials:
| Username 	| Password  	|
|----------	|-----------	|
| Alice    	| Merveille 	|
| Bob      	| Chapeau   	|
| Chris    	| Tof       	|

To shutdown the database, run:

      ./db./server/kill_db_server.sh
To reset the database content you can run the start command with **reset** flag:

      ./db/server/start_db_server.sh <your IP> reset

As the owner of the database, you can add or delete users and their files. To do so, run:

      python3 addUser.py <your IP> 4001
      python3 deleteUser.py <your IP> 4001

And to see the current database state, you can run:

      ./python3 printDatabase.py <your IP> 4001
**4001** is the default port of the leader node of the distributed relational database, we letted it as an argument if you wish to edit it yourselves in (in **start_db_server.sh**) because we currently do not offer the possibility to choose it.

---


## Usage
Once the installation and first initialisation are complete 

Open 2 terminals and place yourself at the root of the project, from there run the following commands :

Command to launch the database :

      python3 ./db/server/serverForDatabase.py


Command to launch the REST end-point API (you first need to export the env var locating the client.config file of microk8s :

      KUBECONFIG="/var/snap/microk8s/4221/credentials/client.config"
      export KUBECONFIG
      python3 python-kubernetes-repartitor.py [EXPOSED_IP] [EXPOSED_PORT]


Command to add the web server to kubernetes :

      ./projet/startup.sh

This will create a kubernetes deployment as well as a service to expose web portal, you can see the web portal port exposed using this command :

      kubectl get services

---


## Known issues / FAQ

*I can't run any kubectl command after a machine restart* 
> This happends especially if your machine have a dual boot, use the following commands : \

      microk8s stop
      microk8s start
      sudo microk8s.refresh-certs -e "ca.crt" 

## Contributors

* [Alexis](https://github.com/Tartopomes)
* [Theo.D](https://github.com/lVenol)
* [Kapesteon](https://github.com/Kapesteon)


 
