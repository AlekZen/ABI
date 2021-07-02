import streamlit as st
import cv2
import imutils
import os
import time
import numpy as np
import datetime



try:
    import pyodbc
    from FireBase import escribe
except:
    st.write('Firebase error')

global indexCam
indexCam=0
indexCamRtsp= 'rtsp://192.168.5.23:5554'

#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr
#%%
run = st.checkbox('Run') 

#Camaras y Broncas

def testDevice(source):
   cap = cv2.VideoCapture(source) 
   if cap is None or not cap.isOpened():
       st.sidebar.write('Esta camara no funciona: ', source)
   else: 
       st.sidebar.write('Esta camara funciona: ', source)



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










if st.sidebar.checkbox('Ajustes de camara'):
    seleccionada=st.sidebar.empty()
    indexCam= st.sidebar.selectbox('Elegir otra camara', returnCameraIndexes())
    seleccionada.write('Camara seleccionada : '+str(indexCam))
    st.sidebar.write('Camaras disponibles: '+str(returnCameraIndexes()))
    st.write('Index '+ indexCamRtsp)
      





    st.sidebar.write('Probando camaras')
    testDevice(0) 
    testDevice(1) 
    testDevice(2) 
    testDevice(3) 


ruta = dataPath = 'datos'
st.title("Reconocimiento Facial")
dataPath = 'datos'
imagePaths = os.listdir(dataPath)
#camara = st.sidebar.checkbox("Camara")
#st.sidebar.button('Entrenar')

FRAME_WINDOW = st.image([])
FRAME_WINDOW2 = st.image([])
ejecuta= st.sidebar.radio('¿Elige una funcion?', ['Reconocer','Capturar'])

camiIP= st.sidebar.checkbox('Camara IP')
if camiIP:
    seleccionada=st.sidebar.empty()
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    rtsp = st.sidebar.text_input(label='Camara IP')
    indexCam=('rtsp://192.168.5.23:5554/onvif1')
    if not rtsp:
        seleccionada.write('Indice Camara IP actual : '+str(indexCam))
    if rtsp:    
        st.sidebar.success(('URL '+ rtsp ))
        indexCam=rtsp
        st.write('Indice camara '+indexCam)
        seleccionada.write('Indice Camara IP seleccionada : '+str(indexCam))

st.sidebar.write(indexCam)

def entrenar():
    mensaje= st.empty()
    st.warning('Espera un poco, Entrenando...')

    dataPath = 'datos'
    listaPersonas= os.listdir(dataPath)
    lista=st.empty()

    st.write('Lista de personas: ', listaPersonas)

    labels =[]
    facesData =[]
    label = 0


    for nameDir in listaPersonas:
        personPath = dataPath + '/' + nameDir
        st.write('Codificando imagenes de...'+ nameDir)
    
        for fileName in os.listdir(personPath):
            #print('Rostros: ', nameDir + '/' + fileName)
            labels.append(label)
            facesData.append(cv2.imread(personPath+'/'+fileName,0))
            image = cv2.imread(personPath+'/'+fileName,0)
            cv2.imshow('image', image)
            cv2.waitKey(10)
        label=label+1

    cv2.destroyAllWindows()
        

    face_recognizer= cv2.face.LBPHFaceRecognizer_create()

    face_recognizer.train(facesData, np.array(labels))
    face_recognizer.write('modeloLBPH.xml')
    st.info('El entrenamiento del modelo se ha completado con exito')
    st.sidebar.write('Modelo entrenado, ve la opcion reconocer')
    return st.write('Modelo entrenado')

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




if st.sidebar.button('Entrenar'):
     entrenar()


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
        subb='Asistencia'
        global DB_table_name
        DB_table_name = str(subb + "_Dia_" + Date + "_Hora_" + Hour + "_")

        
        ###Connect to the database
        try:
            if verSQL:
                try:
                    cursor.execute("SELECT @@version;") 
                    row = cursor.fetchone() 
                    while row: 
                        st.sidebar.write(row[0])
                        row = cursor.fetchone()
                except:
                    print('No hay SQL')
            

        except Exception as e:
            print(e)
            
            

        sql ="USE ["+database +"] if not exists (select * from sysobjects where name='"+DB_table_name +"' and xtype='U') CREATE TABLE [dbo].["+DB_table_name+"]([ID] int not null identity(1,1) primary key,[Nombre] [nvarchar](150) NULL,[Fecha] [date] NULL,[Hora] [time](7) NULL) "
        

        try:
            cursor.execute(sql)
            cnxn.commit()
            if verSQL:
                st.write('SQL grabando en la tabla: '+DB_table_name)

        except Exception as ex:
            print(ex)  #

ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Hour, Minute, Second = timeStamp.split(":")

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




if ejecuta == 'Reconocer':
    camera = cv2.VideoCapture(indexCam,cv2.CAP_DSHOW)
    if camiIP:
        camera = cv2.VideoCapture(indexCam)

    sql = st.sidebar.checkbox('Grabar en SQL')
    FB = st.sidebar.checkbox('Grabar en Firebase')
    CSV = st.sidebar.checkbox('Grabar en CSV')
    margen= st.sidebar.slider('Margen', min_value=0, max_value=1000,value=80)
    if sql:
        try:
            verSQL= st.sidebar.checkbox('Ver SQL' )
            server = 'AI\ALEK' # for a named instance
            database='asistencia'
            user= 'sa'
            pswd='Alek.Zen'
            cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+ pswd)
            cursor = cnxn.cursor()
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
                    print('No funciona el enlace con SQL')
        except:
            st.sidebar.write('No hay enlace con SQL')

    












if ejecuta == 'Capturar':
    camera = cv2.VideoCapture(indexCam)
    persona = st.sidebar.text_input(label='Escribe el nombre del que quieres capturar fotos')
    if not persona:
        st.sidebar.warning('Por favor ingresa el nombre de la persona.')
    if persona:    
        st.sidebar.success(('Procesando a '+ persona ))
        capturacion(ruta,persona)
        muestras = st.sidebar.slider('Cuantas muestras quieres?', 50, 300, 100)
    
        Obtener =st.sidebar.button('Obtener')
        if Obtener:
            my_bar = st.progress(0)
            avance = 0 


    
        
        

# with st.sidebar.form(key='my_form'):
#     persona = st.text_input(label='Escribe el nombre del que quieres capturar fotos')
#     submit_button = st.form_submit_button(label='Procesar')
#     if not persona:
#         st.warning('Por favor ingresa el nombre de la persona.')
#         st.stop()
#     st.success('Procesando a ', persona )
my_bar=st.empty() 
    





##El modelo
status = st.empty()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
try:
    face_recognizer.read('modeloLBPH.xml')
except:
    st.write('No Existe un modelo entrenado')


try:
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
except:
    faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
#indexCam= 'rtsp://192.168.5.23:5554/onvif1'
#camera = cv2.VideoCapture(indexCam)

st.write('Camara actual: ' + str(indexCam))
#La camarilla

while True:
    ret, frame = camera.read() 
    if ret==False: break  
    frame = imutils.resize(frame,width=640)
    if ejecuta == 'Capturar':
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray   = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()
        faces = faceClassif.detectMultiScale(gray,1.3,5)
    
        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
            if persona:
                if Obtener:     
                    cv2.imwrite(rutaPersona +'/rostro_{}.jpg'.format(count),rostro)
                    count = count +1
                    avance= avance+1
                    progreso= int(((avance)*100)/(muestras))
                    my_bar.progress(progreso)
                    #st.write('Progreso: '+str (progreso) +' Avance: '+ str(avance) +' Muestras: '+ str(muestras))

                    if count >= totalFiles + muestras:
                        status.info('El proceso de captura ha concluido para '+ persona)
                        avance=0
                        break

    if ejecuta == 'Reconocer':
        gray   = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        faces = faceClassif.detectMultiScale(gray,1.3,5)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        try:
            for(x,y,w,h) in faces:
                rostro = auxFrame[y:y+h,x:x+w]
                rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)
                cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
                if result[1]<margen:
                    cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                    name=imagePaths[result[0]]
                    if CSV:
                        markAttendance(name)
                    if sql:
                        enter_data_DB(name)
                    if FB:
                        escribe(name)
            
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        except:
            st.write("Hay que comenzxar por capturar el modelo")
    
    FRAME_WINDOW.image(frame)
    k = cv2.waitKey(1)
    if k == 27 :
        #FRAME_WINDOW.image([])
        break




st.write('Cam ejecutado')





