import streamlit as st
import pandas as pd
import numpy as np
import cv2
import os
import imutils
from datetime import datetime




st.title("Capturar rostros")

FRAME_WINDOW = st.image([])


# Forms can be declared using the 'with' syntax
with st.form(key='my_form'):
    persona =text_input = st.text_input(label='Escribe el nombre del que quieres capturar fotos')
    run = st.checkbox('Capturar')
    submit_button = st.form_submit_button(label='Procesar')
    

my_slot1 = st.empty()
# Appends an empty slot to the app. We'll use this later.



dataPath = 'datos'
datosPersona = dataPath + '/' + persona
ruta = st.empty()


if not os.path.exists(datosPersona):
        print('Nueva carpeta para:' + datosPersona)
        os.makedirs(datosPersona)
        
APP_FOLDER = dataPath + '/' + persona+'/'
totalFiles = 0
totalDir = 0

for base, dirs, files in os.walk(APP_FOLDER):
    print('Searching in : ',base)
    for directories in dirs:
        totalDir += 1
    for Files in files:
        totalFiles += 1

conteo = totalDir


def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr





seleccionada=st.sidebar.empty()
indexCam= st.sidebar.selectbox('Probar camaras', returnCameraIndexes())
seleccionada.write('Camara numero : '+str(indexCam))
st.sidebar.write('Camaras disponibles: '+str(returnCameraIndexes()))




if  persona :
    my_slot1.header('Vamos a procesar datos de : '+persona)
    # Replaces the first empty slot with a text string.
    
    ruta.text ('Los datos se van a guardar en: '+ datosPersona)
    st.write('Archivos ya capturados',totalFiles)
    st.write('Carpetas en el directorio',totalDir)
    st.write('Total:',(totalDir + totalFiles))



camera = cv2.VideoCapture(indexCam)


faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
count= totalFiles


dataPath = 'datos'
listaPersonas= os.listdir(dataPath)


#Camarilla
while run:
    ret, frame = camera.read()   
    if ret==False: break
    frame = imutils.resize(frame,width=640)
    gray   = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()
    faces = faceClassif.detectMultiScale(gray,1.3,5)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(datosPersona +'/rostro_{}.jpg'.format(count),rostro)
        count = count +1
        #print(datosPersona+'/_rostro{}.jpg'.format(count),rostro)
    #cv2.imshow('Capturando',frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)
    k = cv2.waitKey(1)
    if k == 27 or count >= totalFiles+300:
        break
      
else:
    st.write('Captura un nombre para capturar su rostro')
    

st.write ('Lista de personas existentes: ', listaPersonas)