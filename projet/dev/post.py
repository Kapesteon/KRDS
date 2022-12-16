import requests

url = 'http://192.168.0.174:8888/RequestDesktop'
#url = 'http://127.0.0.1:8888/RequestDesktop'
x = requests.post(url, json = {"status": 201, "message": "Request Desktop", "username" :"alex"})

print(x.text)




url = 'http://192.168.0.174:8888/GetUserId'
json = {"status": 201, "message": "Is user in db?", "username" :"Alice", "passwordHash" :"62cefe04ea3ed48f7941e7e02915adf23a4490d6396ebab88eee605fbb1ac96c"}

y = requests.post(url, json = json)
print(y.text)