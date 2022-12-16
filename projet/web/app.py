import hashlib, json, requests
from flask import Flask, render_template, request, redirect, make_response

try : 
    isloged = False
    #Nom de l'application
    app = Flask(__name__)
    app.config.update(
    )

except Exception as e:
    print("Error : ", e)

try :
    #Fonction d'affichage de la page index
    @app.route('/')
    def index():
        try:
            if(request.cookies.get("auth") == None):
                print("cookie = none")
                isloged = "false"

            else :
                isloged=request.cookies.get("auth")
                
            if(isloged != "True"):
                return redirect('/login')

            else : 
                print("try to render index")
                return render_template('index.html')

        except Exception as e:
            print("Error : ", e)

    @app.route('/login')
    def login():
        try:
            return render_template('login.html')
        except Exception as e:
            print("Error : ", e)    
    
    @app.route('/index')
    def renderIndex():
        try:
            if(request.cookies.get("auth") == None):
                print("cookie = none")
                isloged = "false"

            else :
                isloged=request.cookies.get("auth")

            if (isloged == "True"):
                return render_template('index.html')
            else :
                return redirect('/')
        except Exception as e:
            print("Error : ", e)   

    #Fonction d'affichage de la page update
    @app.route('/login/submit', methods=['GET', 'POST'])
    def loginSubmit():
        if request.method == "POST":
            try:
                data = request.form
                passwd = hashlib.sha256(str(data["password"]).encode()).hexdigest()
                url = 'http://192.168.0.174:8888/GetUserId'
                jsonData = {"status": 201, "message": "Is user in db?", "username" : data["username"], "passwordHash" : passwd}

                y = requests.post(url, json = jsonData)
                responseStatus = json.loads(y.text)["status"]
                print("loginSubmit response  : "+ str(responseStatus))
                dataResponse = json.loads(y.text)

                if (responseStatus == 201):
                    global userID
                    userID = dataResponse["userID"]
                    response = {"status": "ok"}
                    return response

                else :
                    print("hello too bad response")
                    response = {"status": "Error"}
                    return response

            except Exception as e:
                print("Error : ", e)
        else:
            return redirect('/login')
    
    @app.route('/login/disconnect')
    def loginDisconnect():
        try :
            resp = make_response()
            resp.delete_cookie('auth', path="/", domain="192.168.0.153")
            resp.delete_cookie('username', path="/", domain="192.168.0.153")
            return resp
        except Exception as e:
            print("Error : ", e)

    @app.route('/index/getDekstop', methods=["GET", "POST"])
    def indexGetDekstop():
        try :
            data = request.form
            
            url = 'http://192.168.0.174:8888/RequestDesktop'

            global userID
            x = requests.post(url, json = {"status": 201, "message": "Request Desktop", "username": data["username"].lower(), "userID":userID})      
            responseStatus = json.loads(x.text)["status"]
            
            print("indexGetDekstop response : " + str(responseStatus))

            response = json.loads(x.text)

            if (responseStatus == 201):
                return response
            else :
                return redirect("/")
        except Exception as e:
            print("Error : ", e)


    #Lancement de l'application web
    if __name__ == '__main__':
        app.run()

except Exception as e: 
    print('Error : ', e)