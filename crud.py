"""
Pasos para conectar con BBDD

1- Abrir-Crear conexión
2- Crear Puntero
3- Ejecutar query (consulta) SQL
4- Manejar los resultados de la query (consulta)
   4.1- Insertar, Leer, Actualizar, Borrar  ==> (Create, Read, Update, Delete)
5- Cerrar puntero
6- Cerrar conexión

"""

from tkinter import *
from tkinter import messagebox
import sqlite3

root = Tk()


#######################################  Funciones   #############################################


def exit():
   valor = messagebox.askyesno("Salir", "¿Desea salir de la aplicación?")

   if valor:
      root.destroy()


def connect():
   try:
      miConexion = sqlite3.connect("CRUD")
      miCursor = miConexion.cursor()

      miCursor.execute('''
            CREATE TABLE USERDATA(
               ID INTEGER PRIMARY KEY AUTOINCREMENT,  
               NOMBRE_USUARIO VARCHAR(50),
               PASSWORD VARCHAR(50),
               DIRECCION VARCHAR(50),
               APELLIDO VARCHAR(50),
               COMENTARIOS VARCHAR(100)
            )
      ''')

      messagebox.showinfo("Conectado", "BBDD creada con éxito!")

   except:
      messagebox.showerror("Mala suerte!", "La BBDD ya ha sido creada")


def limpiarCampos():
   miID.set("")
   miNombre.set("")
   miPass.set("")
   miApellido.set("")
   miDireccion.set("")
   textoComentario.delete("1.0", "end")


############################     CRUD -- Funciones   ###########################################

def create(): 
      miConexion = sqlite3.connect("CRUD")
      miCursor = miConexion.cursor()

      datos = miNombre.get(), miPass.get(), miDireccion.get(), miApellido.get(), textoComentario.get("1.0", "end")
      miCursor.execute("INSERT INTO USERDATA VALUES(NULL, ?,?,?,?,?)", datos)

      miConexion.commit()

      messagebox.showinfo("Create", "Los datos han sido agregados a la base de datos")

      limpiarCampos()


def read():
   try:
      miConexion = sqlite3.connect("CRUD")
      miCursor = miConexion.cursor()

      miCursor.execute("SELECT * FROM USERDATA WHERE ID = " + miID.get())

      data = miCursor.fetchall() #guarda en un array, una tupla con todos los datos

      for dato in data: #dato es la tupla y data el array
         #print(data[0][1]) ==> seria lo mismo
         miNombre.set(dato[1])
         miPass.set(dato[2])
         miApellido.set(dato[3])
         miDireccion.set(dato[4])
         textoComentario.insert(1.0, dato[5])

      miConexion.commit()

   except:
      messagebox.showwarning("BBDD", "Debe insertar un ID")


def update():
   miConexion = sqlite3.connect("CRUD")
   miCursor = miConexion.cursor()

   data = miNombre.get(), miPass.get(), miApellido.get(), miDireccion.get(), textoComentario.get("1.0", "end")

   miCursor.execute("UPDATE USERDATA SET NOMBRE_USUARIO=?, PASSWORD=?, APELLIDO=?, DIRECCION=?, COMENTARIOS=? WHERE ID = " + miID.get(), data)

   messagebox.showinfo("Update", "Datos actualizados con éxito")

   miConexion.commit()


def delete():
   miConexion = sqlite3.connect("CRUD")
   miCursor = miConexion.cursor()

   miCursor.execute("DELETE FROM USERDATA WHERE ID = " + miID.get())

   limpiarCampos()

   messagebox.showinfo("Delete", "Datos eliminados con éxito")

   miConexion.commit()





############################     Menú      ###########################################

#Creas el menú principal
barraMenu = Menu(root)
root.config(menu=barraMenu, width=400, height=400, cursor="heart")

#Opciones principales del menú
BBDDMenu = Menu(barraMenu, tearoff=0)
borrarMenu = Menu(barraMenu, tearoff=0)
CRUDMenu = Menu(barraMenu, tearoff=0)
ayudaMenu = Menu(barraMenu, tearoff=0)

#Se agregan al menú principal
barraMenu.add_cascade(label="BBDD", menu=BBDDMenu)
barraMenu.add_cascade(label="Borrar", menu=borrarMenu)
barraMenu.add_cascade(label="CRUD", menu=CRUDMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

#Agregas las opciones de cada menú
BBDDMenu.add_cascade(label="Conectar", command=connect)
BBDDMenu.add_cascade(label="Salir", command=exit)

CRUDMenu.add_cascade(label="Crear", command=create)
CRUDMenu.add_cascade(label="Leer", command=read)
CRUDMenu.add_cascade(label="Actualizar", command=update)
CRUDMenu.add_cascade(label="Eliminar", command=delete)

ayudaMenu.add_cascade(label="Licencia")
ayudaMenu.add_cascade(label="Acerca de...")

borrarMenu.add_command(label="Borrar campos", command=limpiarCampos)


#------------------------------------Campos----------------------------------------

miFrame = Frame(root)
miFrame.pack()
miFrame.config(bg="#33FF42")

miID = StringVar()
miNombre = StringVar()
miPass = StringVar()
miApellido = StringVar()
miDireccion = StringVar()


cuadroID = Entry(miFrame, textvariable=miID)
cuadroID.grid(row=0, column=1, padx=10, pady=10)

cuadroNombre = Entry(miFrame, textvariable=miNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10)
cuadroNombre.config(justify="center")

cuadroPass = Entry(miFrame, textvariable=miPass)
cuadroPass.grid(row=2, column=1, padx=10, pady=10)
cuadroPass.config(show="*", justify="center")

cuadroApellido = Entry(miFrame, textvariable=miApellido)
cuadroApellido.grid(row=3, column=1, padx=10, pady=10)

cuadroDireccion = Entry(miFrame, textvariable=miDireccion)
cuadroDireccion.grid(row=4, column=1, padx=10, pady=10)


textoComentario = Text(miFrame, width=16, height=5)
textoComentario.grid(row=5, column=1)
scrollVert = Scrollbar(miFrame, command=textoComentario.yview)
scrollVert.grid(row=5, column=2, sticky="nsew")

textoComentario.config(yscrollcommand=scrollVert.set)

#################################ETIQUETAS#####################################

IDLabel = Label(miFrame, text="ID: ")
IDLabel.grid(row=0, column=0)

nombreLabel = Label(miFrame, text="Nombre: ")
nombreLabel.grid(row=1, column=0)

passLabel = Label(miFrame, text="Contraseña: ")
passLabel.grid(row=2, column=0)

apellidoLabel = Label(miFrame, text="Apellido: ")
apellidoLabel.grid(row=3, column=0)

direccionLabel = Label(miFrame, text="Dirección: ")
direccionLabel.grid(row=4, column=0)

comentarioLabel = Label(miFrame, text="Comentarios: ")
comentarioLabel.grid(row=5, column=0)

####################################BOTONES####################################

miFrame2 = Frame(root)
miFrame2.pack()
miFrame2.config(bg="#33FF42")

createButton = Button(miFrame2, text="Create", command=create)
createButton.grid(row=0, column=0, sticky="e", pady=10, padx=10)

readButton = Button(miFrame2, text="Read", command=read)
readButton.grid(row=0, column=1, sticky="e", pady=10, padx=10)

updateButton = Button(miFrame2, text="Update", command=update)
updateButton.grid(row=0, column=2, sticky="e", pady=10, padx=10)

deleteButton = Button(miFrame2, text="Delete", command=delete)
deleteButton.grid(row=0, column=3, sticky="e", pady=10, padx=10)


root.mainloop()