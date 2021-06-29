#%%
import pyodbc
import datetime
import time

from FireBase import escribe

#%%
server = 'AI\ALEK' # for a named instance
database='asistencia'
user= 'sa'
pswd='Alek.Zen'
cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+ pswd)
cursor = cnxn.cursor()


#%%

#Sample select query
cursor.execute("SELECT @@version;") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()






#%%





# DB_table_name='Probando4'




# sql ='USE ['+database +'] CREATE TABLE [dbo].['+DB_table_name+']([Nombre] [nvarchar](150) NULL,	[Fecha] [date] NULL,	[Hora] [time](7) NULL) ON [PRIMARY] '
# cursor.execute(sql)
# cnxn.commit()
# print(sqlCreate)



#%%


cursor.execute("SELECT  [Nombre]      ,[Fecha]      ,[Hora]  FROM [asistencia].[dbo].["+DB_table_name+"]") 
row = cursor.fetchone() 
while row: 
    print(row[0:])
    row = cursor.fetchone()



#%%
sql = "CREATE TABLE [" + DB_table_name + """]
                        (	ID INT NOT NULL identity(1,1) primary key,	[Nombre] [nvarchar](150) not NULL,	[Fecha] [date] not NULL,	[Hora] [time](7) not NULL)
                        """
print(sql)

cursor.execute(sql)
print('Tabla creeada')

#%%
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
            cursor.execute("SELECT @@version;") 
            row = cursor.fetchone() 
            while row: 
                print(row[0])
                row = cursor.fetchone()
                
            

        except Exception as e:
            print(e)
            
            

        sql ="USE ["+database +"] if not exists (select * from sysobjects where name='"+DB_table_name +"' and xtype='U') CREATE TABLE [dbo].["+DB_table_name+"]([ID] int not null identity(1,1) primary key,[Nombre] [nvarchar](150) NULL,[Fecha] [date] NULL,[Hora] [time](7) NULL) "
        

        try:
            cursor.execute(sql)
            cnxn.commit()
            print('jala'+sql)

        except Exception as ex:
            print(ex)  #
            print('Falla: '+sql)


#%%


fill_attendance()




#%%


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
           print('Exitoso en: '+DB_table_name)
           
        except Exception as e:
           print(e)
           print(DB_table_name)
           print(Insert_data)
         
                


#%%

escribe('Sidd')

enter_data_DB('Sidd')