import cv2
import os
import streamlit as st
import imutils
import datetime
import pyodbc
import time

sql = st.checkbox('SQL')




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
                st.sidebar.write('Trabajando en la tabla: '+DB_table_name)

        except Exception as ex:
            print(ex)  #


ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Hour, Minute, Second = timeStamp.split(":")




if sql:
    try:
        verSQL= st.sidebar.checkbox('Ver SQL' )
        server = 'AI\ALEK' # for a named instance
        database='asistencia'
        user= 'sa'
        pswd='Alek.Zen'
        cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+ pswd)
        cursor = cnxn.cursor()
    except:
        st.sidebar.write('No hay enlace con SQL')


if sql:
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
           
