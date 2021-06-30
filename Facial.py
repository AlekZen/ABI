import streamlit as st
import cv2
import imutils
import os

st.title("Reconocimiento Facial")
camara = st.sidebar.checkbox("Camara")
capturar = st.sidebar.checkbox("Capturar")

FRAME_WINDOW = st.image([])

camera = cv2.VideoCapture(0)


st.write("Reconocedor")





with st.sidebar.form(key='my_form'):
    persona = st.text_input(label='Escribe el nombre del que quieres capturar fotos')
    submit_button = st.form_submit_button(label='Procesar')
    
ruta = dataPath = 'datos'


def capturacion(ruta, persona):
    global rutaPersona
    rutaPersona= ruta +'/'+ persona
    if not os.path.exists(rutaPersona):
        st.sidebar.write('Creando expediente de: ' + persona)
        os.makedirs(rutaPersona)

    APP_FOLDER = dataPath + '/' + persona+'/'
    global totalFiles
    global count
    totalFiles = 0
    totalDir = 0

    for base, dirs, files in os.walk(APP_FOLDER):
        st.sidebar.write('Buscando en:  ',base)
        for directories in dirs:
            totalDir += 1
        for Files in files:
            totalFiles += 1
        count = totalFiles
        st.sidebar.write('Muestras existentes',totalFiles)


    return "Hola"

if persona:
    capturacion(ruta,persona)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

while camara:
    ret, frame = camera.read() 
    if ret==False: break  
    frame = imutils.resize(frame,width=640)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray   = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()
    faces = faceClassif.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        if capturar:
            cv2.imwrite(rutaPersona +'/rostro_{}.jpg'.format(count),rostro)
            count = count +1
            if count >= totalFiles+300:
                st.write("Capturado 300 muestras")
                persona= st.empty()
            break

    FRAME_WINDOW.image(frame)
    k = cv2.waitKey(1)
    if k == 27 :
        FRAME_WINDOW.image([])
        break