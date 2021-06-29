import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import time


#Firebase
cred = credentials.Certificate('A:\Develops\AlekZenFirebase.json')
firebase_admin.initialize_app(cred)

db = firestore.client()



#Escribir
def escribe(nombre):
    ts = time.time()
    Date = datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
    timeStamp = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Time = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fecha= datetime.utcnow()
    Docasistente=db.collection(u'Asistentes').document(nombre)
    Asistencias = Docasistente.collection(Date).document(Time)
    doc_ref = db.collection(u'Asistencias').document(nombre).collection(u'Asistencias')
    Asistencias.set({
        u'Fecha': fecha,
        u'Dia': u'16/6/21',
        u'Turno': 1
    })



#escribe('Dulce')

# #leer
# users_ref = db.collection(u'KPIs')
# docs = users_ref.stream()

# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')
