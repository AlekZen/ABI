import streamlit as st
import cv2
import os
import numpy as np


mensaje= st.empty()
mensaje.header('Entrenando...')

dataPath = 'datos'
listaPersonas= os.listdir(dataPath)
lista=st.empty()

st.write('Lista de personas: ', listaPersonas)

labels =[]
facesData =[]
label = 0


for nameDir in listaPersonas:
    personPath = dataPath + '/' + nameDir
    print('Leyendo imagenes')
    
    for fileName in os.listdir(personPath):
        #print('Rostros: ', nameDir + '/' + fileName)
        labels.append(label)
        facesData.append(cv2.imread(personPath+'/'+fileName,0))
        image = cv2.imread(personPath+'/'+fileName,0)
        cv2.imshow('image', image)
        cv2.waitKey(10)
    label=label+1

#print('Etiquetas= ', labels)
st.write('Numero de 0s: ' , np.count_nonzero(np.array(labels)==0))
st.write('Numero de 1s: ' , np.count_nonzero(np.array(labels)==1))
st.write('Numero de 2s: ' , np.count_nonzero(np.array(labels)==2))



cv2.destroyAllWindows()
        

face_recognizer= cv2.face.LBPHFaceRecognizer_create()

face_recognizer.train(facesData, np.array(labels))
face_recognizer.write('modeloLBPH.xml')
mensaje.header('Modelo entrenado, ve la opcion reconocer')
