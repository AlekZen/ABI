import cv2
import os
import streamlit as st
import imutils
import datetime
import pyodbc
import time

encabezado = st.empty()
encabezado.header('Reconocimiento de rostros')
run = st.sidebar.checkbox('Reconocer')
sql = st.sidebar.checkbox('Grabar en SQL')
if sql:
    verSQL= st.sidebar.checkbox('Ver SQL' )


ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Hour, Minute, Second = timeStamp.split(":")

# st.write('Fecha: ',Date)
# st.write('Tiempo estampa: ' ,timeStamp)
# st.write('El tiempo:',Time)
# st.write('La hora: ',Hour)
# st.write('Minuto: ',Minute)
# st.write("Segundo: ", Second)

server = 'AI\ALEK' # for a named instance
database='asistencia'
user= 'sa'
pswd='Alek.Zen'
cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+ pswd)
cursor = cnxn.cursor()


def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        ####Creatting csv of attendance

        ##Create table for Attendance
        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        global subb
        subb='Attendance'
        global DB_table_name
        DB_table_name = str(subb + "_" + Date + "_Time_" + Hour + "_")

        
        ###Connect to the database
        try:
            if verSQL:
                cursor.execute("SELECT @@version;") 
                row = cursor.fetchone() 
                while row: 
                    st.sidebar.write(row[0])
                    row = cursor.fetchone()
                
            

        except Exception as e:
            st.write(e)
            
            

        sql ="USE ["+database +"] if not exists (select * from sysobjects where name='"+DB_table_name +"' and xtype='U') CREATE TABLE [dbo].["+DB_table_name+"]([ID] int not null identity(1,1) primary key,[Nombre] [nvarchar](150) NULL,[Fecha] [date] NULL,[Hora] [time](7) NULL) "
        

        try:
            cursor.execute(sql)
            cnxn.commit()
            if verSQL:
                st.sidebar.write('Trabajando en la tabla: '+DB_table_name)

        except Exception as ex:
            print(ex)  #
            st.sidebar.write('No existe enlace con SQL: ')




if sql:
    #Sample select query
    fill_attendance()
    def enter_data_DB(name):
        ts = time.time()
        fecha=str(datetime.datetime.now())
        Date = datetime.datetime.fromtimestamp(ts).strftime('%d/%Y/%m')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
        Hour, Minute, Second = timeStamp.split(":")
        Insert_data = "USE ["+database +"]  INSERT INTO [dbo].["+DB_table_name+"] VALUES ( '"+str(name)+"','"+fecha+"','"+str(Time)+"')"
        print(Insert_data)
        VALUES = ( str(name), str(Date), str(Time))
        print('Fecha: '+ fecha)       
        try:
           cursor.execute(Insert_data)
           cnxn.commit()
           print('Grabando a : '+name + 'en '+DB_table_name)
           
        except Exception as e:
           st.sidebar.write(e)
           





FRAME_WINDOW = st.image([])

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
indexCam= st.sidebar.selectbox('Elegir otra camara', returnCameraIndexes())
seleccionada.write('Camara seleccionada : '+str(indexCam))
st.sidebar.write('Camaras disponibles: '+str(returnCameraIndexes()))




dataPath = 'datos'
imagePaths = os.listdir(dataPath)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()


face_recognizer.read('modeloLBPH.xml')
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)



camera = cv2.VideoCapture(indexCam,cv2.CAP_DSHOW)
#camera = cv2.VideoCapture(indexCam ,cv2.CAP_DSHOW)


faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')



dataPath = 'datos'
listaPersonas= os.listdir(dataPath)

margen= st.sidebar.slider('Margen', min_value=0, max_value=1000,value=80)

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime('%d/%m/%Y')
            timeString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString},{timeString}')



#Camarilla
while run:
    ret, frame = camera.read()   
    if ret==False: break
    frame = imutils.resize(frame,width=640)
    gray   = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()
    
    faces = faceClassif.detectMultiScale(gray,1.3,5)
    
    for(x,y,w,h) in faces:
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)
        cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
        if result[1]<margen:
            cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            name=imagePaths[result[0]]
            markAttendance(name)
            if sql:
                enter_data_DB(name)
            
        else:
            cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        
        
        
        
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
  
else:
    st.write('Activa el boton de reconocer para comenzar la rutina')
  
    

st.write('Personas existentes: ', imagePaths)







