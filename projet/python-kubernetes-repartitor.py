import sys      
import time

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from kubernetes import client, config #for kubernetes API calls
from kubernetes.stream import stream #For launching command in pod 

import ast  #for byte-data conversion
import os   #for file management
import fileinput
import yaml
import json
import traceback 

from db.server.getUserID import getUserID #File to verify if user exists in databse, made by Alexis


"""_____________________________________________________________"""
"""                         Constants                           """
"""_____________________________________________________________"""
USER_RELATED_FOLDER = "./users/"

TEMPLATE_K8S_SERVICE_CLIENT = "./users/TEMPLATE_SERVICE.yaml"       #File path to the kubernetes service template that will be duplicated when a new user want to connect
TEMPLATE_K8S_DEPLOYMENT_CLIENT = "./users/TEMPLATE_DEPLOYMENT.yaml" #File path to the kubernetes deployment template that will be duplicated when a new user want to connect


SERVICE_CLIENT_NAME_CONVENTION = "alpha-service-user-"         #Name convention for service files, add the username after the last -
DEPLOYMENT_CLIENT_NAME_CONVENTION = "alpha-deployment-user-"   #Name convention for deployment files add the username after the last -

DEPLOYMENT_IMAGE_DEFAULT_LOCATION = "localhost:32000/"          #Where kubernetes should look the image for the deployment
DEPLOYMENT_IMAGE_DEFAULT_NAME="alpha"                           #Default name of the image deployment that kubernetes will use

DEPLOYMENT_DEFAULT_TOKEN="vncpassword"

HOST_DB_IP = "192.168.0.174"
HOST_DB_PORT = 65432

image = DEPLOYMENT_IMAGE_DEFAULT_LOCATION+DEPLOYMENT_IMAGE_DEFAULT_NAME



"""_____________________________________________________________"""
"""                     Web functions                           """
"""_____________________________________________________________"""

def setup(sock):
    try : 
        sock.bind((sys.argv[1], int(sys.argv[2])))
        print("Server launched !")
    except Exception as e:
        print(e)

def listen(sock):
    try : 
        (bytestr,adress) = sock.recvfrom(4096)
        print('Msg received : ',bytestr)
        dict_str = bytestr.decode("UTF-8")
        data = ast.literal_eval(dict_str) #data is a dict

        #DEBUG:
        data = {"name" : "jean", "pwd" :"test"}

        userDeploymentFilePath  = createNewUserDeployment(data["name"],image)
        userServiceFilePath     = createNewUserService(data["name"])
        port = str(createPodForUser(data["name"],image,userDeploymentFilePath,userServiceFilePath))
        ipv4 = getNodeIp()


        m ='{"ipv4": "'+ipv4+'", "port": '+port+'}'
        jsonObj = json.dumps(m)

        dataToSend = jsonObj
        sock.sendto(bytes(dataToSend,encoding="utf-8"), adress)

    except Exception as e:
        print(e)
    finally:
        sock.close

"""_____________________________________________________________"""
"""            Kubernetes related functions                     """
"""_____________________________________________________________"""

def find_file(filename, search_path):
    result = ""

    #Wlaking top-down from the root
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result = os.path.join(root, filename)
            break
        
    return result

#TODO
def initGUISessionInPod(podname):
    return
    #https://stackoverflow.com/questions/73210551/execute-commands-within-kubernetes-pod-in-python

# ***createNewUserService***
# param     :   [string] username                   (client's username requesting a pod)
# return    :   [string] userFileNameLocation       (The file path of the service-user.yaml)
#
#
def createNewUserService(username):

    #check if the service is not already created for this user:
    userFileName = "service-user-"+username+".yaml"
    userFileNameLocation = USER_RELATED_FOLDER+userFileName
    userFile = find_file(userFileName, USER_RELATED_FOLDER)

    #If the file was found, return
    if userFile != "":
        return userFileNameLocation
    
    else: #Else, create it
    
        cpCommand = 'cp '+TEMPLATE_K8S_SERVICE_CLIENT+" "+userFileNameLocation
        print(cpCommand)
        for i in range(5):
            try:

                os.popen(cpCommand) 
                break
            except Exception as e:
                print("Error when trying to copy templateServce, happened on attempt %d " % (i))
    

    time.sleep(3) #Wait for the file to be created

    with fileinput.FileInput("./users/"+userFileName, inplace=True,backup='') as file:
        for line in file:
            print(line.replace("%USER%", username), end='')
    
    return userFileNameLocation


#***createNewUserDeployment***
# param     :   [string] username                   (client's username requesting a pod)
#               [string] imageName                      (the name of the docker image to write in the yaml file)
# return    :   [string] userFileNameLocation       (The file path of the service-user.yaml)
def createNewUserDeployment(username,imageName,userID):

    #check if the service is not already created for this user:
    userFileName = "deployment-user-"+username+".yaml"
    userFileNameLocation = USER_RELATED_FOLDER+userFileName
    userFile = find_file(userFileName, USER_RELATED_FOLDER)

    #If the file was found, return
    if userFile != "":
        return userFileNameLocation
    
    else: #Else, create it
    
        cpCommand = 'cp '+TEMPLATE_K8S_DEPLOYMENT_CLIENT+" "+userFileNameLocation
        print(cpCommand)
        for i in range(5):
            try:

                os.popen(cpCommand) 
                break
            except Exception as e:
                print("Error when trying to copy templateServce, happened on attempt %d " % (i))
    

    time.sleep(3) #Wait for the file to be created

    with fileinput.FileInput("./users/"+userFileName, inplace=True,backup='') as file:
        for line in file:
            print(line.replace("%USER%", username), end='')

    with fileinput.FileInput("./users/"+userFileName, inplace=True,backup='') as file:
        for line in file:
            print(line.replace("%IMAGE%", imageName), end='')

    with fileinput.FileInput("./users/"+userFileName, inplace=True,backup='') as file:
        for line in file:
            print(line.replace("%SECRET_TOKEN%", DEPLOYMENT_DEFAULT_TOKEN), end='')

    with fileinput.FileInput("./users/"+userFileName, inplace=True,backup='') as file:
        for line in file:
            print(line.replace("%USERID%", "\""+userID+"\""), end='')

    return userFileNameLocation






#***createPodForUser***
# param     :   [string] username                   (client's username requesting a pod)
#               [string] deploymentFilePath         (File path of the deployment.yaml)
#               [string] serviceFilePath            (File path of the service.yaml)
# return    :   [int] port       (The node's port forwarded for the user to connect)
def createPodForUser(username,imageName,deploymentFilePath,serviceFilePath):
    
    appv1 = client.AppsV1Api()
    corev1 = client.CoreV1Api()
    
    metadataNameDeployment = DEPLOYMENT_CLIENT_NAME_CONVENTION + username

    deploymentList = appv1.list_namespaced_deployment(namespace="default")

    isUserDeploymentAlreadyCreated = False

    #Check if the deployment is already created or not
    for item in deploymentList.items:
        if (item.metadata.name == metadataNameDeployment):
            isUserDeploymentAlreadyCreated = True

    if(not isUserDeploymentAlreadyCreated):
        with open(deploymentFilePath) as f:
            dep = yaml.safe_load(f)
            resp = appv1.create_namespaced_deployment(
                body=dep, namespace="default")
            print("Deployment created. status='%s'" % resp.metadata.name)
    



    metadataNameService = SERVICE_CLIENT_NAME_CONVENTION + username

    #Check if the service is already created or not
    serviceList = corev1.list_namespaced_service(namespace="default")
    isUserServiceAlreadyCreated = False
    for item in serviceList.items:
        if (item.metadata.name == metadataNameService):
            isUserServiceAlreadyCreated = True
            userService = item

    #If the deployment and services are not yet created
    if(not isUserDeploymentAlreadyCreated):
        with open(serviceFilePath) as f:
            dep = yaml.safe_load(f)
            service = corev1.create_namespaced_service(
                body=dep, namespace="default")
            print("Service created. status='%s'" % service.metadata.name)

        userService = service




    vncport = userService.spec.ports[0].node_port
    novncport = userService.spec.ports[1].node_port
    port = novncport 

    return port


def getNodeIp():

    # grab the node name from the pod environment vars
    nodeName = os.environ.get('NODE_NAME', None)

    v1 = client.CoreV1Api()

    #DEBUG
    nodeName = 'tuf'

    nodes = v1.list_node(pretty=True)
    for node in nodes.items:
        if node.metadata.name == nodeName:
            addresses = node.status.addresses
            for i in addresses:
                if i.type =="InternalIP":
                    address = i.address

    return address








"""_____________________________________________________________"""
"""                             Main                            """
"""_____________________________________________________________"""
# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Root(Resource):
    #corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
    
        return jsonify({'message': 'hello world'})
    
    # Corresponds to POST request
    def post(self):
    
        data = request.get_json()     # status code
        return jsonify({'data': data}), 201

class RequestDesktop(Resource):

    response = {"status": 400, "message": "Desktop not created", "ipv4" :"0.0.0.0","port":"0000"}
    def post(self):
        try:   
            user_data = request.get_json()
            print(user_data)
            username = user_data["username"]
            userID = user_data["userID"]
            userID = str(userID)
            userDeploymentFilePath  = createNewUserDeployment(username,image,userID)
            userServiceFilePath     = createNewUserService(username)
            port = str(createPodForUser(username,image,userDeploymentFilePath,userServiceFilePath))
            ipv4 = getNodeIp()

            self.response["status"] = 201
            self.response["message"] = "User created successfully"
            self.response["ipv4"] = ipv4
            self.response["port"] = port

            return self.response, 201

        except Exception as e: 
            traceback.print_exc()
            print(e)
            self.response["status"] = 400
            self.response["message"] = "Something went wrong while creating the user's associated files"
            return self.response, 400


class GetUserId(Resource):

    response = {"status": 400, "message": "User not in database", "userID" :-1, "userRole" :""}

    def post(self):
        try:
            
            host = HOST_DB_IP
            port = HOST_DB_PORT 

            user_data = request.get_json()

            username = user_data["username"]
            passwordHash = user_data["passwordHash"]

            dataToSend = getUserID(host, port, username, passwordHash)

            if (dataToSend[0] != -1):
                self.response["status"] = 201
                self.response["message"] = "User in database"
                self.response["userID"] = dataToSend[0]
                self.response["userRole"] = dataToSend[1]
                print(self.response)
                return self.response, 201
            else:
                print(self.response)
                return self.response, 400

        except: 
            self.response["status"] = 400
            self.response["message"] = "Something went wrong while creating the user's associated files"
            return self.response, 400


# adding the defined resources along with their corresponding urls
api.add_resource(Root, '/')
api.add_resource(RequestDesktop, '/RequestDesktop')
api.add_resource(GetUserId, '/GetUserId')

config.load_kube_config()

appv1 = client.AppsV1Api()
corev1 = client.CoreV1Api()

# driver function
if __name__ == '__main__':

    #python3 server.py 127.0.0.1 8888
    host_address = "0.0.0.0"
    host_port = "8888"

    if len(sys.argv) == 1:
        print("No argument given")
        print("Usage :\n python3 python-kubernetes-repartitor.py <IP> <port> ")
        print("Example :\n python3 python-kubernetes-repartitor.py 0.0.0.0 8888")
        print("Using default values, IP="+host_address+" and Port="+host_port+" ")

    if len(sys.argv) == 2:
        print("1 argument given")
        print("Usage :\n python3 python-kubernetes-repartitor.py <IP> <port> ")
        print("Example :\n python3 python-kubernetes-repartitor.py 0.0.0.0 8888")
        print("Using default values for Port="+host_port+" ")
        host_address = sys.argv[1]

    if len(sys.argv) == 3:
        print("2 argument given")
        host_address = sys.argv[1]
        host_port = sys.argv[2]

    if len(sys.argv) > 3:
        print("Usage : ./prog <server> <port> ")
        sys.exit()

    print("app running on "+host_address+":"+host_port)
    app.run(debug = True,host=host_address,port=host_port)










