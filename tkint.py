import tkinter


ventana = tkinter.Tk()
ventana.geometry("600x600")
etiqueta=tkinter.Label(ventana)
etiqueta.pack(side= tkinter.BOTTOM,fill= tkinter.Y)
#etiqueta.pack(fill= tkinter.X)
persona = tkinter.Entry(ventana)
persona.pack()


def saludo():
    etiqueta["text"]= persona.get()





boton1 = tkinter.Button(ventana,text='Capturar', padx=40,pady=50, command= saludo)
boton1.pack(side= tkinter.TOP)

ventana.mainloop()
