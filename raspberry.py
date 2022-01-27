from time import sleep
import requests
import math
import random
import serial
import os
import socket
import subprocess
import sys
import pyrebase
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import sys
import signal
import firebase
import credentials

#Instalacion de libreria pyrebase
#subprocess.check_call([sys.executable,'-m','pip','install','pyrebase'])

#Variables para almacenar datos recibidos del atmega
ph=""
co2=""
temp=""
luz=""


#ENVIAR DATOS A FIREBASE
def firebase(bomba, foco, ventilador):
    config = {"apiKey": "database-secret",
              "authDomain": "project-id.firebaseapp.com",
              "databaseURL": "https://sistemacic-d1880-default-rtdb.firebaseio.com/",
              "storageBucket": "project-id.appspot.com"}
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    db.child("huerto").child("bomba").set(bomba)
    db.child("huerto").child("foco").set(foco)
    db.child("huerto").child("ventilador").set(ventilador)


#CODIGO INTERRUPCION POR TIMER
def timer_interrupt():
    #RECIBO ORDENES DESDE APP INVENTOR
    servidor()
    threading.Timer(0.1, timer_interrupt).start()

def timer_interrupt2():
    #Enviando informacion a firebase
    firebase(bomba, foco, ventilador)
    threading.Timer(0.1, timer_interrupt2).start()


auto= "0"
def timer_interrupt3():
    #envio ordenes al atmega en modo automatico
    if auto=="1":
        print('ok3')
        autom()
    threading.Timer(2, timer_interrupt3).start()

#Habilito interrupciones por TIMER
threading.Timer(1, timer_interrupt).start()
threading.Timer(1, timer_interrupt2).start()
#threading.Timer(2, timer_interrupt3).start()

def autom():
    if ("18">temp) or (temp>"25"):
        ser.write("2".encode())#enciendo bomba
    else:
        ser.write("5".encode())#apago bomba
    
    if ("200">luz) or (luz>"300"):
        ser.write("3".encode())#enciendo foco
    else:
        ser.write("6".encode())#apago foco
    
    if ("100">co2) or (co2>"400"):
        ser.write("4".encode())#enciendo ventilador
    else:
        ser.write("7".encode())#apago ventilador


#CODIGO PARA COMUNICARNOS CON APP INVECTOR
#Optengo direccion IP
myip = socket.gethostbyname(socket.gethostname())
print (myip)

def servidor():
 Request = None
 class RequestHandler_httpd(BaseHTTPRequestHandler):
   def do_GET(self):    
    global Request
    messagetosend = bytes('Solicitando',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    Request = self.requestline
    Request = Request[5 : int(len(Request)-9)]
    
    #print(Request)
    if Request == 'on1':
      print('Bomba encendida')
      ser.write("2".encode())
      auto= "0"
    if Request == 'on2':
      print('Foco encendido')
      ser.write("3".encode())
      auto= "0"
    if Request == 'on3':
      print('Ventilador encendido')
      ser.write("4".encode())
      auto= "0"
    if Request == 'off1':
      print('Bomba apagada')
      ser.write("5".encode())
      auto= "0"
    if Request == 'off2':
      print('Foco apagado')
      ser.write("6".encode())
      auto= "0"
    if Request == 'off3':
      print('Ventilador apagado')
      ser.write("7".encode())
      auto= "0"
    
    if  Request == 'aut':
      auto= "1"
      print('ok')
    
 server_address_httpd = (myip,8001)
 httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
 print('conectando a servidor')
 print(httpd.fileno())
 httpd.serve_forever()


# CODIGO PARA COMUNICAR CON UBIDOTS
TOKEN = "BBFF-q5N1rTslEYg8YtnIoN1FMVUSzmbhLW"
DEVICE_LABEL = "sistemacic"
VARIABLE_LABEL_1 = "pH"
VARIABLE_LABEL_2 = "CO2"
VARIABLE_LABEL_3 = "Temperatura"
VARIABLE_LABEL_4 = "Luminosidad"

def build_payload(variable_1, variable_2, variable_3, variable_4, value_1, value_2, value_3, value_4):
     print ("CONECTADO...")
     lat = -3.060757
     lng =-79.746451
     payload = {variable_1: value_1,
                variable_2: value_2,
                variable_3: value_3,
                variable_4: {"value": value_4, "context": {"lat": lat, "lng": lng}}}
     return payload

def post_request(payload):
     # Creates the headers for the HTTP requests
     url = "http://industrial.api.ubidots.com"  
     url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
     headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
     
     # Makes the HTTP requests
     status = 400
     attempts = 0
     while status >= 400 and attempts <= 5:
         req = requests.post(url=url, headers=headers, json=payload)
         status = req.status_code
         attempts += 1
         sleep(1)
                
     # Processes results
     if status >= 400:
         print("[ERROR] Could not send data after 5 attempts, please check \
your token credentials and internet connection")
         return False    
     print("[INFO] request made properly, your device is updated")
     return True
    
    
    
    
#Habilito comunicacion serial
ser = serial.Serial('/dev/ttyS1',9600)
ser.flushInput()


#COMUNICACION CON UBIDOTS   
def ubidots():     
    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4,
                           ph, co2, temp, luz)
    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")

while True:
    try: 
        bomba=0
        foco=0
        ventilador=0

        #RECIBO DATOS DESDE EL ATMEGA
        lineBytes = ser.readline()
        line = lineBytes.decode('utf-8').strip()
        if int(line)==2000:
            lineBytes = ser.readline()
            line = lineBytes.decode('utf-8').strip()
            ph=line
            print("ph:"+line)
        elif int(line)==3000:
            lineBytes = ser.readline()
            line = lineBytes.decode('utf-8').strip()
            co2=line
            print("co2:"+line)
        elif int(line)==4000:
            lineBytes = ser.readline()
            line = lineBytes.decode('utf-8').strip()
            temp=line
            print("Temperatura:"+line)
        elif int(line)==5000:
            lineBytes = ser.readline()
            line = lineBytes.decode('utf-8').strip()
            luz=line
            print("Luz:"+line)
            
    except KeyboardInterrupt:
        break
    
    #COMUNICACION CON UBIDOTS        
    ubidots()
