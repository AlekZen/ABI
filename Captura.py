import streamlit as st
import cv2
import os
import imutils
#print('Capture el nombre de la persona: ')
st.write='Hola mundo'

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Que quieres hacer?',
    ('Capturar fotos', 'Entrenar el modelo', 'Reconocer rostros')
)

st.write='Hola mundo'


#persona= st.text_input(label='Escribe el nombre de quien quieres capturar fotos')

# Alternative syntax, declare a form and use the returned object
form = st.form(key='my_form')
persona=form.text_input(label='Captura por favor el nombre de la persona que vamos a entrenar')
submit_button = form.form_submit_button(label='Comenzar')

dataPath = 'datos'
datosPersona = dataPath + '/' + persona
st.write=('Ok, Vamos a capturar las fotos de ' + datosPersona)

if not os.path.exists(datosPersona):
        print('Nueva carpeta para:' + datosPersona)
        os.makedirs(datosPersona)
APP_FOLDER = 'A:/BOTSI/Attendance/OpenCV/datos/'+persona+'/'
totalFiles = 0
totalDir = 0
for base, dirs, files in os.walk(APP_FOLDER):
    print('Searching in : ',base)
    for directories in dirs:
        totalDir += 1
    for Files in files:
        totalFiles += 1

conteo = totalDir
print('Total number of files',totalFiles)
print('Total Number of directories',totalDir)
print('Total:',(totalDir + totalFiles))
print('Conteo:',(conteo))


print(totalFiles)


cap = cv2.VideoCapture(0)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
count= totalFiles
while True:
    ret, frame = cap.read()
    if ret==False: break
    frame = imutils.resize(frame,width=640)
    gray   = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()
    faces = faceClassif.detectMultiScale(gray,1.3,5)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,+h),(0,255,0),2)
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(datosPersona +'/rostro_{}.jpg'.format(count),rostro)
        count = count +1
        #print(datosPersona+'/_rostro{}.jpg'.format(count),rostro)
    cv2.imshow('Capturando',frame)

    k = cv2.waitKey(1)
    if k == 27 or count >= totalFiles+300:
        break
cap.release()
cv2.destroyAllWindows()


cap = cv2.VideoCapture(0)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_profileface.xml')
count= totalFiles
while True:
    ret, frame = cap.read()
    if ret==False: break
    frame = imutils.resize(frame,width=640)
    gray   = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()
    faces = faceClassif.detectMultiScale(gray,1.3,5)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,+h),(0,255,0),2)
        fecha = str(datetime.now())
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(datosPersona +'/rostro3_{}.jpg'.format(count),rostro)
        count = count +1
        #print(datosPersona+'/_rostro{}.jpg'.format(count),rostro)
    cv2.imshow('Perfiles',frame)

    k = cv2.waitKey(1)
    if k == 27 or count >= totalFiles+300:
        break
cap.release()
cv2.destroyAllWindows()



print('Terminado')







        
