from tkinter import * 
import tkinter
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from datetime import datetime, timedelta 
import locale
locale.setlocale(locale.LC_ALL, '') 



#funciones

conexion=sqlite3.connect('clientes.db')
cursor=conexion.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS consolidado (id INTEGER PRIMARY KEY AUTOINCREMENT , fecha TEXT, nombre TEXT, apellido TEXT, saldo NUMERIC, telefono TEXT, dias TEXT)')
conexion.close()

def iniciar_consolidado():
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute('INSERT INTO consolidado VALUES(?,?,?,?,?)', (id_busqueda3.get(), fecha_var.get(), cliente_consulta.get(), apellido_consulta.get(), saldo_acumulado.get()))
	conexion.commit()
	conexion.close()


def borrar():
	
	mensaje.config(text="")

	n1.set('')
	a1.set('')
	t1.set('')
	d1.set("")
def nuevo():
	if len (n1.get())==0 or len (a1.get())==0 or len (t1.get())==0 or len(d1.get())==0:
		messagebox.showerror("Error", "No puede haber campos vacios")
	else:
		dt=datetime.now()
		dt_format=("{}/{}/{}".format(dt.day, dt.month, dt.year))
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute( "INSERT INTO clientes VALUES (null,?,?,?,?)", (n1.get(), a1.get(), t1.get(), d1.get()) )
		conexion.commit()
		conexion.close()

		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("INSERT INTO consolidado VALUES (null,?,?,?,?,?,?)",(dt_format, n1.get(), a1.get(), '0',t1.get(),'0'))
		conexion.commit()
		conexion.close()
		
		mensaje.config (text="Cliente creado con éxito")
		n1.set('')
		a1.set('')
		t1.set('')
		d1.set("")
	
def consulta ():
	verconsulta.delete(*verconsulta.get_children())
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute("SELECT id, apellido, nombre, telefono, DNI FROM clientes WHERE apellido LIKE ?",(a1.get()+'%',))
	usuarios=cursor.fetchall()
	for u in usuarios:

		verconsulta.insert("", "end", values=(u))
	conexion.close()



def editar():
	editar.config(state="disable")
	def eliminar():
		respuesta=messagebox.askquestion("Eliminar", "El registro será elminado")
		if respuesta == "yes":
			conexion=sqlite3.connect('clientes.db')
			cursor=conexion.cursor()
			cursor.execute("DELETE FROM clientes WHERE id=?", (id_busqueda.get(),) )
			cursor.execute("DELETE FROM consolidado WHERE id=?", (id_busqueda.get(),) )

			conexion.commit()
			conexion.close()
			ventana_edicion.destroy()
			editar.config(state="normal")
	def buscar():
		nomeeditar.set("")
		apelidoeditar.set("")
		phoneeditar.set("")
		DNIeditar.set("")
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("SELECT nombre, apellido, telefono, DNI FROM clientes WHERE id=?", (id_busqueda.get(),))
		cambio=cursor.fetchone()
		try:
			lista=list(cambio)
			nome.set(lista[0])
			apelido.set(lista[1])
			phone.set(lista[2])
			DNI.set(lista[3])
			gris_nombre_fijo.config(textvariable=nome)
			gris_apellido_fijo.config(textvariable=apelido)
			gris_tel_fijo.config(textvariable=phone)
			gris_DNI_fijo.config(textvariable=DNI)
			conexion.close()
		except TypeError:
			messagebox.showerror("Error", "El id que está busando no existe o ha sido eliminado")
	def modificar_tabla():
		if len(nomeeditar.get()) != 0:

			conexion=sqlite3.connect('clientes.db')
			cursor=conexion.cursor()
			cursor.execute ("UPDATE clientes SET nombre= ? WHERE id=?", (nomeeditar.get(), id_busqueda.get())) 
			cambio=cursor.fetchone()
			conexion.commit()
			conexion.close() 
		if len(apelidoeditar.get()) != 0:

			conexion=sqlite3.connect('clientes.db')
			cursor=conexion.cursor()
			cursor.execute ("UPDATE clientes SET apellido= ? WHERE id=?", (apelidoeditar.get(), id_busqueda.get())) 
			cambio=cursor.fetchone()
			conexion.commit()
			conexion.close() 
		if len(phoneeditar.get()) != 0:

			conexion=sqlite3.connect('clientes.db')
			cursor=conexion.cursor()
			cursor.execute ("UPDATE clientes SET telefono= ? WHERE id=?", (phoneeditar.get(), id_busqueda.get())) 
			cambio=cursor.fetchone()
			conexion.commit()
			conexion.close() 

		if len(DNIeditar.get())!=0:
			conexion=sqlite3.connect('clientes.db')
			cursor=conexion.cursor()
			cursor.execute ("UPDATE clientes SET DNI= ? WHERE id=?", (DNIeditar.get(), id_busqueda.get())) 
			cambio=cursor.fetchone()
			conexion.commit()
			conexion.close() 

		if len(phoneeditar.get())!=0 or len(nomeeditar.get())!=0 or len(apelidoeditar.get())!=0 or len (DNIeditar.get()) !=0:
			messagebox.showinfo("Editar", "El cliente ha sido editado")
			ventana_edicion.destroy()
			editar.config(state="normal")
		
		if len(nomeeditar.get()) ==0 and len(apelidoeditar.get()) ==0 and len(phoneeditar.get())==0 and len (DNIeditar.get())==0:
			messagebox.showinfo("Error", "No ha editado ningún campo")
		
	def cruz():
		ventana_edicion.destroy()
		editar.config(state="normal")
		

	id_busqueda=StringVar()
	ventana_edicion=Toplevel(width=450, height=500)
	ventana_edicion.title("Editar Cliente")
	ventana_edicion.attributes('-topmost', 'true')
	label_id=Label(ventana_edicion, text="Id")
	label_id.grid(row=0, column=0, padx=3, pady=3)
	entry_id=Entry(ventana_edicion, textvariable=id_busqueda)
	entry_id.grid(row=0, column=1, padx=3, pady=3)
	buscar_id=Button(ventana_edicion, text="Buscar", command=buscar)
	buscar_id.grid(row=0, column=3)
	nombre_fijo=Label(ventana_edicion, text="Nombre").grid(row=1, column=0, padx=3, pady=3)
	nome=StringVar()
	gris_nombre_fijo=Entry(ventana_edicion, state="disabled")
	gris_nombre_fijo.grid(row=1, column=1, padx=3, pady=3)
	nombre_fijo=Label(ventana_edicion, text="Nombre").grid(row=1, column=0, padx=3, pady=3)
	apelido=StringVar()
	apellido_fijo=Label(ventana_edicion, text="Apellido").grid(row=3, column=0, padx=3, pady=3)
	gris_apellido_fijo=Entry(ventana_edicion, bg="blue", state="disabled")
	gris_apellido_fijo.grid(row=3, column=1, padx=3, pady=3)
	phone=StringVar()
	tel_fijo=Label(ventana_edicion, text="Telefono").grid(row=5, column=0, padx=3, pady=3)
	gris_tel_fijo=Entry(ventana_edicion, bg="blue", state="disabled")
	gris_tel_fijo.grid(row=5, column=1, padx=3, pady=3)
	DNI=StringVar()
	DNI_fijo=Label(ventana_edicion, text="DNI").grid(row=7, column=0, padx=3, pady=3)
	gris_DNI_fijo=Entry(ventana_edicion, bg="blue", state="disabled")
	gris_DNI_fijo.grid(row=7, column=1, padx=3, pady=3)
	#Label y Entry para toplevel edicion
	nombre_editar=Label(ventana_edicion, text="Editar Nombre").grid(row=2, column=0, padx=3, pady=3)
	nomeeditar=StringVar()
	editar_nombre_fijo=Entry(ventana_edicion, textvariable=nomeeditar)
	editar_nombre_fijo.grid(row=2, column=1, padx=3, pady=3)
	apellido_editar=Label(ventana_edicion, text="Editar Apellido").grid(row=4, column=0, padx=3, pady=3)
	apelidoeditar=StringVar()
	editar_apellido_fijo=Entry(ventana_edicion, textvariable=apelidoeditar)
	editar_apellido_fijo.grid(row=4, column=1, padx=3, pady=3)
	tel_editar=Label(ventana_edicion, text="Editar Telefono").grid(row=6, column=0, padx=3, pady=3)
	phoneeditar=StringVar()
	editar_tel_fijo=Entry(ventana_edicion, textvariable=phoneeditar)
	editar_tel_fijo.grid(row=6, column=1, padx=3, pady=3)
	DNI_editar=Label(ventana_edicion, text="Editar DNI").grid(row=8, column=0, padx=3, pady=3)
	DNIeditar=StringVar()
	editar_DNI=Entry(ventana_edicion, textvariable=DNIeditar)
	editar_DNI.grid(row=8, column=1, padx=3, pady=3)
	Boton_editar_toplevel=Button(ventana_edicion, text="Editar", command=modificar_tabla).grid(row=7, column=2, padx=3, pady=3)
	Boton_eliminar_toplevel=Button(ventana_edicion, text="Eliminar", command=eliminar).grid(row=7, column=3, padx=3, pady=3)
	ventana_edicion.protocol("WM_DELETE_WINDOW", cruz)

	
	
	
#variables para las funciones


root = Tk()
root.title("Gestor")

def cerrar():
	presentacion.destroy()
presentacion=Toplevel()
presentacion.attributes('-topmost', 'true')
saludo=Label(presentacion, text='Bienvenido a GESTOR 1.0.20', font=('verdana', 25, 'bold')).pack()
aceptar=Button(presentacion,text='Aceptar', command=cerrar, font=('time new roman', 16)).pack()

entrada=Frame(root)
entrada.pack()
hola=Label(entrada, text='Gestor 1.0.20', font=('time new roman',20))
hola.pack()


#Creando la pestaña cliente

pestaña=ttk.Notebook(root)
pestaña.pack(fill="both", expand=1)


n1=StringVar () 
a1=StringVar () 
t1=StringVar ()
d1=StringVar ()
	

	#Contenedor
frame=Frame(pestaña)
frame.pack(fill="both", expand=1)

#Incorporo el frame a la pestaña
pestaña.add(frame, text="Clientes    ")

#Label monitor carga
mensaje=Label(frame,  bg="white", font=("time new roman", 15))
mensaje.grid(row=1, column=2, columnspan=2)

#Label monitor de consulta

verconsulta=ttk.Treeview(frame) 
verconsulta ["columns"]= ("cuatro","uno", "dos", "tres", "cinco")
verconsulta.column ("cuatro", width=60, minwidth=60)
verconsulta.column ("#0", width=0, minwidth=0)
verconsulta.heading ("cuatro", text="Id")
verconsulta.heading ("uno", text="Nombre")
verconsulta.heading ("dos", text="Apellido")
verconsulta.heading ("tres",text="Telefono")
verconsulta.heading("cinco", text="DNI")
verconsulta.grid(row=5, column=0, columnspan=4)


	#Canmpo de nombres
labelNombre=Label(frame, text="Nombre")
labelNombre.config(font=("time new roman", 18))
labelNombre.grid(row=0, column=0,padx=5, pady=5)
entryNombre=Entry(frame, textvariable=n1)
entryNombre.grid(row=0, column=1,padx=5, pady=5)

	#Campo de Apellido
labelApellido=Label(frame, text="Apellido")
labelApellido.config(font=("time new roman", 18))
labelApellido.grid(row=1, column=0, padx=5, pady=5)
entryApellido=Entry(frame, textvariable=a1)
entryApellido.grid(row=1, column=1, padx=5, pady=5)

	#Campo telefono
labelTel=Label(frame, text="Telefono")
labelTel.config(font=("time new roman", 18))
labelTel.grid(row=2, column=0, padx=5, pady=5)
entryTel=Entry(frame, textvariable=t1)
entryTel.grid(row=2, column=1, padx=5, pady=5)

#Campo de DNI

labelDNI=Label(frame, text="DNI")
labelDNI.config(font=("time new roman", 18))
labelDNI.grid(row=3, column=0, padx=5, pady=5)
entryDNI=Entry(frame, textvariable=d1)
entryDNI.grid(row=3, column=1, padx=5, pady=5)

#Variables
nombre=n1.get()
apellido=a1.get()
tel=t1.get()
dni=d1.get()

	#Botones ((

nuevo=Button(frame, text="Nuevo", command=nuevo, width=11, height=1)
nuevo.grid(row=4, column=0)
nuevo.config(font=("time new roman", 15), padx=4, pady=4,relief="ridge")

editar=Button(frame, text="Editar", command=editar,width=11, height=1)
editar.grid(row=4, column=1)
editar.config(font=("time new roman", 15), padx=4, pady=4,relief="ridge")

borrar=Button(frame, text="Borrar", command=borrar, width=11, height=1)
borrar.grid(row=4, column=2)
borrar.config(font=("time new roman", 15), padx=4, pady=4,relief="ridge")

consultar=Button(frame, text="Consultar", command=consulta,width=11, height=1)
consultar.grid(row=4, column=3)
consultar.config(font=("time new roman", 15), padx=4, pady=4,relief="ridge")

#top level para edición


#Base  datos clientes (tabla)
conexion=sqlite3.connect('clientes.db')
cursor=conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS clientes"\
	"( id INTEGER PRIMARY KEY AUTOINCREMENT, nombre VARCHAR (100) NOT NULL, apellido VARCHAR (100) NOT NULL, telefono INTEGER(30) NOT NULL, DNI INTEGER(12)  NOT NULL)")
conexion.commit()
conexion.close()

#Base de datos productos (tabla)
conexion=sqlite3.connect('clientes.db')
cursor=conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS productos"\
	"( id INTEGER PRIMARY KEY AUTOINCREMENT, producto VARCHAR (100) NOT NULL, precio INTEGER (100) NOT NULL)")
conexion.commit()
conexion.close()

#Funciones para la pestaña producto

def borrar_pto():
	
	mensaje2.config(text="")

	pto.set('')
	pr.set('')
	
def nuevo_pto():
	if len (pto.get())==0 or len (pr.get())==0 :
		messagebox.showerror("Error", "No puede haber campos vacios")
	else:
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute( "INSERT INTO productos VALUES (null,?,?)", (pto.get(), pr.get()) )
		
		
		conexion.commit()
		conexion.close()
		mensaje2.config(text="Producto creado con éxito")
		pto.set('')
		pr.set('')
def consulta_pto ():
	verconsulta2.delete(*verconsulta2.get_children())
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute("SELECT id, producto, precio FROM productos WHERE producto LIKE ?",(pto.get()+'%',))
	mercaderia=cursor.fetchall()
	for m in mercaderia:

		verconsulta2.insert("", "end", values=(m))
	conexion.close()



def editar_pto():
	editar.config(state="disable")
	def eliminar_pto():
		respuesta=messagebox.askquestion("Eliminar", "El registro será elminado")
		if respuesta == "yes":
			conexion=sqlite3.connect('clientes.db')
			cursor=conexion.cursor()
			cursor.execute("DELETE FROM productos WHERE id=?", (id_busqueda2.get(),) )
			conexion.commit()
			conexion.close()
			ventana_edicion2.destroy()
			editar.config(state="normal")
	def buscar_pto():
		mercaeditar.set("")
		precioeditar.set("")
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("SELECT producto, precio FROM productos WHERE id=?", (id_busqueda2.get(),))
		cambio=cursor.fetchone()
		try:
			lista=list(cambio)
			merca.set(lista[0])
			valor.set(lista[1])
			gris_producto_fijo.config(textvariable=merca)
			gris_precio_fijo.config(textvariable=valor)
			conexion.close()
		except TypeError:
			messagebox.showerror("Error", "El id que está busando no existe o ha sido eliminado")
	def modificar_tabla_pto():
		if len(mercaeditar.get()) != 0:

			conexion=sqlite3.connect('clientes.db')
			cursor=conexion.cursor()
			cursor.execute ("UPDATE productos SET producto= ? WHERE id=?", (mercaeditar.get(), id_busqueda2.get())) 
			cambio=cursor.fetchone()
			conexion.commit()
			conexion.close() 
		if len(precioeditar.get()) != 0:

			conexion=sqlite3.connect('clientes.db')
			cursor=conexion.cursor()
			cursor.execute ("UPDATE productos SET precio= ? WHERE id=?", (precioeditar.get(), id_busqueda2.get())) 
			cambio=cursor.fetchone()
			conexion.commit()
			conexion.close() 
		
		if len(merca.get())!=0 or len(precioeditar.get())!=0 :
			messagebox.showinfo("Editar", "El producto ha sido editado")
			ventana_edicion2.destroy()
			editar.config(state="normal")
		
		if len(mercaeditar.get()) ==0 and len(precioeditar.get()) ==0:
			messagebox.showinfo("Error", "No ha editado ningún campo")
		
	def cruz_pto():
		ventana_edicion2.destroy()
		editar.config(state="normal")
		

	id_busqueda2=StringVar()
	ventana_edicion2=Toplevel(width=450, height=500)
	ventana_edicion2.title("Producto")
	ventana_edicion2.attributes('-topmost', 'true')
	label_id=Label(ventana_edicion2, text="Id")
	label_id.grid(row=0, column=0, padx=3, pady=3)
	entry_id=Entry(ventana_edicion2, textvariable=id_busqueda2)
	entry_id.grid(row=0, column=1, padx=3, pady=3)
	buscar_id=Button(ventana_edicion2, text="Buscar", command=buscar_pto)
	buscar_id.grid(row=0, column=3)
	producto_fijo=Label(ventana_edicion2, text="Producto").grid(row=1, column=0, padx=3, pady=3)
	merca=StringVar()
	gris_producto_fijo=Entry(ventana_edicion2, state="disabled")
	gris_producto_fijo.grid(row=1, column=1, padx=3, pady=3)
	producto_fijo=Label(ventana_edicion2, text="Producto").grid(row=1, column=0, padx=3, pady=3)
	valor=StringVar()
	precio_fijo=Label(ventana_edicion2, text="Precio").grid(row=3, column=0, padx=3, pady=3)
	gris_precio_fijo=Entry(ventana_edicion2, bg="blue", state="disabled")
	gris_precio_fijo.grid(row=3, column=1, padx=3, pady=3)
	
	#Label y Entry para toplevel edicion productos
	producto_editar=Label(ventana_edicion2, text="Editar Producto").grid(row=2, column=0, padx=3, pady=3)
	mercaeditar=StringVar()
	editar_producto_fijo=Entry(ventana_edicion2, textvariable=mercaeditar)
	editar_producto_fijo.grid(row=2, column=1, padx=3, pady=3)
	precio_editar=Label(ventana_edicion2, text="Editar Precio").grid(row=4, column=0, padx=3, pady=3)
	precioeditar=StringVar()
	editar_precio_fijo=Entry(ventana_edicion2, textvariable=precioeditar)
	editar_precio_fijo.grid(row=4, column=1, padx=3, pady=3)
	
	Boton_editar_toplevel=Button(ventana_edicion2, text="Editar", command=modificar_tabla_pto).grid(row=7, column=2, padx=3, pady=3)
	Boton_eliminar_toplevel=Button(ventana_edicion2, text="Eliminar", command=eliminar_pto).grid(row=7, column=3, padx=3, pady=3)
	ventana_edicion2.protocol("WM_DELETE_WINDOW", cruz_pto)



#Ventana de productos #########


frame2=Frame(pestaña)
frame2.pack(fill="both", expand=1)

#Variables
pr=StringVar()
pto=StringVar()
#Incorporo el frame a la pestaña
pestaña.add(frame2, text="Productos    ")

#Label monitor carga Producto
mensaje2=Label(frame2,  bg="white", font=("time new roman", 15))
mensaje2.grid(row=1, column=2, columnspan=2)

	#Canmpo de Poducto
labelProducto=Label(frame2, text="Producto")
labelProducto.config(font=("time new roman", 18))
labelProducto.grid(row=0, column=0,padx=5, pady=5)
entryProducto=Entry(frame2, textvariable=pto, width=50)
entryProducto.grid(row=0, column=1,padx=5, pady=5, columnspan=2)

	#Campo de Precio
labelPrecio=Label(frame2, text="Precio")
labelPrecio.config(font=("time new roman", 18))
labelPrecio.grid(row=1, column=0, padx=5, pady=5)
entryPrecio=Entry(frame2, textvariable=pr)
entryPrecio.grid(row=1, column=1, padx=5, pady=5, sticky="w")


#Botones pestaña productos

nuevo=Button(frame2, text="Nuevo", command=nuevo_pto, width=11, height=1)
nuevo.grid(row=4, column=0)
nuevo.config(font=("time new roman", 15), padx=4, pady=4,relief="ridge")

editar=Button(frame2, text="Editar", command=editar_pto,width=11, height=1)
editar.grid(row=4, column=1)
editar.config(font=("time new roman", 15), padx=4, pady=4,relief="ridge")

borrar=Button(frame2, text="Borrar", command=borrar_pto, width=11, height=1)
borrar.grid(row=4, column=2)
borrar.config(font=("time new roman", 15), padx=4, pady=4,relief="ridge")

consultar=Button(frame2, text="Consultar", command=consulta_pto, width=11, height=1)
consultar.grid(row=4, column=3)
consultar.config(font=("time new roman", 15), padx=4, pady=4,relief="ridge")



#Label monitor de consulta Producto

verconsulta2=ttk.Treeview(frame2) 
verconsulta2 ["columns"]= ("cuatro","uno", "dos")

verconsulta2.column ("#0", width=0, minwidth=0)
verconsulta2.column ("cuatro",width=30, minwidth=30)
verconsulta2.column ("uno",width=400, minwidth=400)
verconsulta2.column ("dos",width=95, minwidth=95)
verconsulta2.heading ("cuatro", text="Id")
verconsulta2.heading ("uno", text="Producto")
verconsulta2.heading ("dos", text="Precio")

verconsulta2.grid(row=5, column=0, columnspan=4)


#Pestaña de ventas...

#Botones plantilla de ventas




#funciones de la pestaña ventas
def blanquear():
	entry_buscar_prod_id.config(state='disable')
	entry_buscar_prod_ventas.config(state='disable')
	venta_computar.set(0)
	num_venta.set(0)
	id_var.set(0)
	id_var2.set(0)
	id_var3.set(0)
	id_var4.set(0)
	id_var5.set(0)
	prod_var.set('')
	prod_var2.set('')
	prod_var3.set('')
	prod_var4.set('')
	prod_var5.set('')
	cant_var.set(0)
	cant_var2.set(0)
	cant_var3.set(0)
	cant_var4.set(0)
	cant_var5.set(0)
	pre_var.set(0)
	pre_var2.set(0)
	pre_var3.set(0)
	pre_var4.set(0)
	pre_var5.set(0)
	total_uni_var.set(0)
	total_uni_var2.set(0)
	total_uni_var3.set(0)
	total_uni_var4.set(0)
	total_uni_var5.set(0)
	total_var.set(0)
	desc.set(0)
	saldo.set(0)
	saldo.set(0)
	cliente_consulta.set('')
	id_busqueda3.set('')
	apellido_consulta.set('')
	DNI_consulta.set('')
	tel_consulta.set('')
	buscar_prod_venta.set('')
def habilitar_ventas():
	nueva_venta.config(state='disable')
	fin_venta.config(state='disable')
	Editar_venta.config(state='normal')
	Eliminar_venta.config(state='normal')
	entry_buscar_prod_ventas.config(state='normal')
	entry_buscar_prod_id.config(state='normal')
	#boton_pagos.config(state='disable')
	fin_venta.config(state='disable')
	id_var.set(0)
	id_var2.set(0)
	id_var3.set(0)
	id_var4.set(0)
	id_var5.set(0)
	prod_var.set('')
	prod_var2.set('')
	prod_var3.set('')
	prod_var4.set('')
	prod_var5.set('')
	cant_var.set(0)
	cant_var2.set(0)
	cant_var3.set(0)
	cant_var4.set(0)
	cant_var5.set(0)
	pre_var.set(0)
	pre_var2.set(0)
	pre_var3.set(0)
	pre_var4.set(0)
	pre_var5.set(0)
	total_uni_var.set(0)
	total_uni_var2.set(0)
	total_uni_var3.set(0)
	total_uni_var4.set(0)
	total_uni_var5.set(0)
	total_var.set(0)
	desc.set(0)
	saldo.set(0)
	saldo.set(0)
	entry_num_venta.config(state="normal")
def consultar_ventas(event):
	
	conexion=sqlite3.connect('clientes.db')
	cursor1=conexion.cursor()
	cursor1.execute("SELECT * FROM ventas WHERE numero = ?", (num_venta.get(),))
	cursor2=conexion.cursor()
	cursor2.execute("SELECT * FROM asociados WHERE numero=?", (num_venta.get(),))
	datos1=cursor1.fetchall()
	datos2=cursor2.fetchall()
	conexion.close()

	try:
		venta_computar.set(datos2[0][9])
		fecha_var.set(datos1[0][1])
		id_var.set(datos1[0][2])
		id_var2.set(datos1[1][2])
		id_var3.set(datos1[2][2])
		id_var4.set(datos1[3][2])
		id_var5.set(datos1[4][2])
		prod_var.set(datos1[0][3])
		prod_var2.set(datos1[1][3])
		prod_var3.set(datos1[2][3])
		prod_var4.set(datos1[3][3])
		prod_var5.set(datos1[4][3])
		cant_var.set(datos1[0][4])
		cant_var2.set(datos1[1][4])
		cant_var3.set(datos1[2][4])
		cant_var4.set(datos1[3][4])
		cant_var5.set(datos1[4][4])
		pre_var.set(datos1[0][5])
		pre_var2.set(datos1[1][5])
		pre_var3.set(datos1[2][5])
		pre_var4.set(datos1[3][5])
		pre_var5.set(datos1[4][5])
		total_uni_var.set(datos1[0][6])
		total_uni_var2.set(datos1[1][6])
		total_uni_var3.set(datos1[2][6])
		total_uni_var4.set(datos1[3][6])
		total_uni_var5.set(datos1[4][6])
		total_var.set(datos1[0][7])
		desc.set(datos1[0][8])
		saldo.set(datos1[0][9])
		id_busqueda3.set(datos2[0][1])
		cliente_consulta.set(datos2[0][3])
		apellido_consulta.set(datos2[0][4])
		DNI_consulta.set(datos2[0][5])
		tel_consulta.set(datos2[0][6]) 
	except IndexError:
		messagebox.showinfo('', 'La venta no existe o ha sido eliminada')
		blanquear()
		#boton_pagos.config(state='disable')
		fin_venta.config(state='disable')
		Editar_venta.config(state='disable')
		Eliminar_venta.config(state='disable')
		#nueva_venta.config(state='normal')



def editar_venta_cargada():
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute('SELECT descuento FROM asociados  WHERE numero=?', (num_venta.get(),))
	consulta_descuento=cursor.fetchone()
	conexion.close()
	string_consulta=list(consulta_descuento)
	st_consulta2=str(string_consulta[0])
	print(st_consulta2)
	if st_consulta2=='SI':
		messagebox.showinfo('','La venta posee descuento. Genera una venta nueva')
	else: 
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("DELETE FROM ventas WHERE numero = ? ", (num_venta.get(),))
		lista_carga_venta=[(num_venta.get(),fecha_var.get(), id_var.get(), prod_var.get(), cant_var.get(), pre_var.get(), total_uni_var.get(), total_var.get(), desc.get(), saldo.get()),
			(num_venta.get(), fecha_var.get(), id_var2.get(), prod_var2.get(), cant_var2.get(), pre_var2.get(), total_uni_var2.get(), total_var.get(), desc.get(), saldo.get()),
			(num_venta.get(),fecha_var.get(), id_var3.get(), prod_var3.get(), cant_var3.get(), pre_var3.get(), total_uni_var3.get(), total_var.get(), desc.get(), saldo.get()),
			(num_venta.get(),fecha_var.get(), id_var4.get(), prod_var4.get(), cant_var4.get(), pre_var4.get(), total_uni_var4.get(), total_var.get(), desc.get(), saldo.get()),
			(num_venta.get(),fecha_var.get(), id_var5.get(), prod_var5.get(), cant_var5.get(), pre_var5.get(), total_uni_var5.get(), total_var.get(), desc.get(), saldo.get())]
		detalle.set(prod_var.get()+ prod_var2.get()+ prod_var3.get()+ prod_var4.get()+ prod_var5.get()) 
		cursor.executemany("INSERT INTO ventas VALUES(?,?,?,?,?,?,?,?,?,?)",lista_carga_venta )
		cursor.execute("UPDATE asociados SET saldo = ? WHERE numero=?", (saldo.get(),num_venta.get(),))
		cursor.execute("UPDATE ventas SET saldo =? WHERE numero=?", (saldo.get(),num_venta.get(),))
		cursor.execute("UPDATE asociados SET venta_total = ? WHERE numero=?", (venta_computar.get(),num_venta.get(),))
		cursor.execute("UPDATE asociados SET detalle = ? WHERE numero=?", (detalle.get(),num_venta.get(),))
		conexion.commit()
		conexion.close()
		messagebox.showinfo("Edicion", "Venta nº {} editada correctamente".format(num_venta.get()))
		acumular_saldo2(id_busqueda3.get())
		comenzar_venta()

		venta_computar.set(0)
		num_venta.set(0)
		entry_num_venta.config(state="disable")
		id_var.set(0)
		id_var2.set(0)
		id_var3.set(0)
		id_var4.set(0)
		id_var5.set(0)
		prod_var.set('')
		prod_var2.set('')
		prod_var3.set('')
		prod_var4.set('')
		prod_var5.set('')
		cant_var.set(0)
		cant_var2.set(0)
		cant_var3.set(0)
		cant_var4.set(0)
		cant_var5.set(0)
		pre_var.set(0)
		pre_var2.set(0)
		pre_var3.set(0)
		pre_var4.set(0)
		pre_var5.set(0)
		total_uni_var.set(0)
		total_uni_var2.set(0)
		total_uni_var3.set(0)
		total_uni_var4.set(0)
		total_uni_var5.set(0)
		total_var.set(0)
		desc.set(0)
		saldo.set(0)
		saldo.set(0)
		cliente_consulta.set('')
		id_busqueda3.set('')
		apellido_consulta.set('')
		DNI_consulta.set('')
		tel_consulta.set('')
		fin_venta.config(state='disable')
		Editar_venta.config(state='disable')
		Eliminar_venta.config(state='disable')
	
def eliminar_venta_cargada():
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute("DELETE FROM ventas WHERE numero = ? ", (num_venta.get(),))
	cursor.execute("DELETE FROM asociados WHERE numero = ? ", (num_venta.get(),))
	conexion.commit()
	conexion.close()
	messagebox.showinfo("Eliminar", "La venta nº {} ha sido eliminada correctamente".format(num_venta.get()))

	entry_num_venta.config(state="disable")
	num_venta.set(0)
	id_var.set(0)
	id_var2.set(0)
	id_var3.set(0)
	id_var4.set(0)
	id_var5.set(0)
	prod_var.set('')
	prod_var2.set('')
	prod_var3.set('')
	prod_var4.set('')
	prod_var5.set('')
	cant_var.set(0)
	cant_var2.set(0)
	cant_var3.set(0)
	cant_var4.set(0)
	cant_var5.set(0)
	pre_var.set(0)
	pre_var2.set(0)
	pre_var3.set(0)
	pre_var4.set(0)
	pre_var5.set(0)
	total_uni_var.set(0)
	total_uni_var2.set(0)
	total_uni_var3.set(0)
	total_uni_var4.set(0)
	total_uni_var5.set(0)
	total_var.set(0)
	desc.set(0)
	saldo.set(0)
	saldo.set(0)
	cliente_consulta.set('')
	id_busqueda3.set('')
	apellido_consulta.set('')
	DNI_consulta.set('')
	tel_consulta.set('')
	Editar_venta.config(state='disable')
	Eliminar_venta.config(state='disable')
	nueva_venta.config(state='normal')
	venta_computar.set(0)
def limpiar_planilla ():
	blanquear()
	Editar_venta.config(state='disable')
	Eliminar_venta.config(state='disable')
	nueva_venta.config(state='normal')
	Consultar_venta.config(state='normal')



def cargar_venta ():
	if len (cliente_consulta.get())!=0:
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute('''CREATE TABLE IF NOT EXISTS ventas(numero INTEGER (10000) ,fecha TEXT , Codigo INTEGER(100000),
			productos VARCHAR(100), cantidad INTEGER(10000), precio INTEGER(10000), unitario INTEGER, total INTEGER,
			descuento INTEGER, saldo INTEGER) ''')
		conexion.close()
		nueva_venta2()
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		lista_carga_venta=[(num_venta.get(),fecha_var.get(), id_var.get(), prod_var.get(), cant_var.get(), pre_var.get(), total_uni_var.get(), total_var.get(), desc.get(), saldo.get()),
			(num_venta.get(),fecha_var.get(), id_var2.get(), prod_var2.get(), cant_var2.get(), pre_var2.get(), total_uni_var2.get(), total_var.get(), desc.get(), saldo.get()),
			(num_venta.get(),fecha_var.get(), id_var3.get(), prod_var3.get(), cant_var3.get(), pre_var3.get(), total_uni_var3.get(), total_var.get(), desc.get(), saldo.get()),
			(num_venta.get(),fecha_var.get(), id_var4.get(), prod_var4.get(), cant_var4.get(), pre_var4.get(), total_uni_var4.get(), total_var.get(), desc.get(), saldo.get()),
			(num_venta.get(),fecha_var.get(), id_var5.get(), prod_var5.get(), cant_var5.get(), pre_var5.get(), total_uni_var5.get(), total_var.get(), desc.get(), saldo.get())]
		detalle.set(prod_var.get() + prod_var2.get() + prod_var3.get() + prod_var4.get() + prod_var5.get())
		cursor.executemany("INSERT INTO ventas VALUES(?,?,?,?,?,?,?,?,?,?)",lista_carga_venta )
		cursor.execute("UPDATE asociados SET saldo = ? WHERE numero=?", (saldo.get(),num_venta.get(),))
		cursor.execute("UPDATE ventas SET saldo =? WHERE numero=?", (saldo.get(),num_venta.get(),))
		cursor.execute("UPDATE asociados SET venta_total = ?, efectivo=0, tarjeta=0, debito=0, credito=0, descuento='' WHERE numero=?", (venta_computar.get(),num_venta.get(),))
		cursor.execute("UPDATE asociados SET detalle = ? WHERE numero=?", (detalle.get(),num_venta.get(),))
		if desc.get()==0:
			cursor.execute("UPDATE asociados SET descuento = 'NO' WHERE numero=?", (num_venta.get(),))
		else:
			cursor.execute("UPDATE asociados SET descuento = 'SI' WHERE numero=?", (num_venta.get(),))

		conexion.commit()
		conexion.close()

		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("UPDATE consolidado SET fecha =? WHERE ID=?", (fecha_var.get(), id_busqueda3.get()))
		conexion.commit()
		conexion.close()

		messagebox.showinfo("Venta", "Venta nº {} cargada con éxito".format(num_venta.get()))
		fin_venta.config(state='disable')
		#num_venta.set(0)
		entry_num_venta.config(state="disable")
		preguntar=messagebox.askquestion('Pagos', 'Desea aplicar pago')
		if preguntar =='yes':
			aplicar_pago()
		else:
			acumular_saldo2(id_busqueda3.get())
			blanquear()
			num_venta.set(0)
			id_var.set(0)
			id_var2.set(0)
			id_var3.set(0)
			id_var4.set(0)
			id_var5.set(0)
			prod_var.set('')
			prod_var2.set('')
			prod_var3.set('')
			prod_var4.set('')
			prod_var5.set('')
			cant_var.set(0)
			cant_var2.set(0)
			cant_var3.set(0)
			cant_var4.set(0)
			cant_var5.set(0)
			pre_var.set(0)
			pre_var2.set(0)
			pre_var3.set(0)
			pre_var4.set(0)
			pre_var5.set(0)
			total_uni_var.set(0)
			total_uni_var2.set(0)
			total_uni_var3.set(0)
			total_uni_var4.set(0)
			total_uni_var5.set(0)
			total_var.set(0)
			desc.set(0)
			saldo.set(0)
			saldo.set(0)
			cliente_consulta.set('')
			id_busqueda3.set('')
			apellido_consulta.set('')
			DNI_consulta.set('')
			tel_consulta.set('')
			entry_buscar_prod_ventas.config(state="disable")
			entry_buscar_prod_id.config(state="disable")
			dt=datetime.now()
			fecha_var.set('{}/{}/{}'.format(dt.day, dt.month, dt.year))
		
	else:
		messagebox.showinfo("", "Debe asociar un cliente a la venta") 

		





def aplicar_pago():

	def imputar_pago_efcetivo(event):
		x=saldo.get()-efectivo.get()
		saldo.set(x)
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("SELECT MAX (numero) FROM asociados")
		numero=cursor.fetchone()
		num_venta2.set(numero[0])
		cursor.execute("UPDATE asociados SET efectivo =?,  debito=0,credito=0  WHERE numero =?", (efectivo.get(), num_venta2.get(),))
		cursor.execute('UPDATE asociados SET saldo =? WHERE numero= ?', (saldo.get(), num_venta.get()))
		conexion.commit()
		conexion.close()
		cuadro_pago.destroy()
		messagebox.showinfo('','El pago fue apicado a la venta nº {}'.format(num_venta.get()))
		preguntar=messagebox.askquestion('Pagos', '¿Desea aplicar pago con Tarjeta?')
		if preguntar =='yes':
			aplicar_pago2()
		else:
			acumular_saldo2(id_busqueda3.get())
			blanquear()

	num_venta2=StringVar()
	efectivo=IntVar()
	TC=IntVar()
	cuadro_pago=Toplevel()
	#Label_num_venta2=Label(cuadro_pago, text="Venta nº").grid(row=0, column=0)
	#entry_num_venta2=Entry(cuadro_pago, textvariable=num_venta2)
	##entry_num_venta2.grid(row=0, column=1)
	#entry_num_venta2.config(state="disable")
	cuadro_pago.config(width=250, height=200, padx=10, pady=15)
	label_efectivo=Label(cuadro_pago, text='Efectivo', width=35, padx=5, pady=5)
	label_efectivo.grid(row=1, column=0)
	entry_efectivo=Entry(cuadro_pago, textvariable=efectivo, justify="right")
	entry_efectivo.grid(row=2, column=0)
	entry_efectivo.bind('<Return>', imputar_pago_efcetivo)
	entry_efectivo.config(font=('time new roman', 18))
	#label_TC=Label(cuadro_pago, text='Tarjea', width=35, padx=5, pady=5)
	#label_TC.grid(row=3, column=0)
	#entry_TC=Entry(cuadro_pago,textvariable=TC, justify="right")
	#entry_TC.grid(row=4, column=0)
	#entry_TC.bind('<Return>', imputar_pago_TC)
	

def aplicar_pago2():
	def imputar_pago_TC(event):
		saldo.set(saldo.get()-TC.get())
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("SELECT MAX (numero) FROM asociados")
		numero=cursor.fetchone()
		num_venta2.set(numero[0])
		cursor.execute("UPDATE asociados SET tarjeta =?, debito=0, credito=0  WHERE numero =?", (TC.get(), num_venta2.get(),))
		cursor.execute('UPDATE asociados SET saldo =? WHERE numero= ?', (saldo.get(), num_venta.get()))
		conexion.commit()
		conexion.close()
		cuadro_pago.destroy()
		messagebox.showinfo('','El pago fue apicado a la venta nº {}'.format(num_venta.get()))
		acumular_saldo2(id_busqueda3.get()) 
		blanquear()
		
	num_venta2=StringVar()
	efectivo=IntVar()
	TC=IntVar()
	cuadro_pago=Toplevel()
	#Label_num_venta2=Label(cuadro_pago, text="Venta nº").grid(row=0, column=0)
	#entry_num_venta2=Entry(cuadro_pago, textvariable=num_venta2)
	##entry_num_venta2.grid(row=0, column=1)
	#entry_num_venta2.config(state="disable")
	cuadro_pago.config(width=250, height=200, padx=10, pady=15)
	#label_efectivo=Label(cuadro_pago, text='Efectivo', width=35, padx=5, pady=5)
	#label_efectivo.grid(row=1, column=0)
	#entry_efectivo=Entry(cuadro_pago, textvariable=efectivo, justify="right")
	#entry_efectivo.grid(row=2, column=0)
	#entry_efectivo.bind('<Return>', imputar_pago_TC)
	label_TC=Label(cuadro_pago, text='Tarjeta', width=35, padx=5, pady=5)
	label_TC.grid(row=3, column=0)
	entry_TC=Entry(cuadro_pago,textvariable=TC, justify="right")
	entry_TC.grid(row=4, column=0)
	entry_TC.config(font=('time new roman', 18))
	entry_TC.bind('<Return>', imputar_pago_TC)

def abrir_precio():
	if id_var.get()==1:
		entry_pre.config(state='normal')


def abrir_productos_con_id(event):
	def asignar_prod2(event):
		x=verconsulta_ventas.set(verconsulta_ventas.selection())
		if len(prod_var.get()) ==0:
			prod_var.set(x.get('uno')), id_var.set(x.get('cuatro')), pre_var.set(x.get('dos')), total_uni_var.set(0)
		elif len (prod_var.get())!=0 and len (prod_var2.get())==0 :
			prod_var2.set(x.get('uno')), id_var2.set(x.get('cuatro')), pre_var2.set(x.get('dos')), total_uni_var2.set(0)
		elif len (prod_var2.get())!=0 and len (prod_var3.get())==0:
			prod_var3.set(x.get('uno')), id_var3.set(x.get('cuatro')), pre_var3.set(x.get('dos')), total_uni_var3.set(0)
		elif len (prod_var3.get())!=0 and len (prod_var4.get())==0:
			prod_var4.set(x.get('uno')), id_var4.set(x.get('cuatro')), pre_var4.set(x.get('dos')), total_uni_var4.set(0)
		elif len (prod_var4.get())!=0 and len (prod_var5.get())==0:
			prod_var5.set(x.get('uno')), id_var5.set(x.get('cuatro')), pre_var5.set(x.get('dos')), total_uni_var5.set(0)
			
		buscando_ptos.destroy()
		buscar_prod_id.set('')
		abrir_precio()

	buscando_ptos=Toplevel(width=250, height=300)
	buscando_ptos.attributes('-topmost', 'true')

	verconsulta_ventas=ttk.Treeview(buscando_ptos) 
	verconsulta_ventas ["columns"]= ("cuatro","uno", "dos")
	verconsulta_ventas.column ("#0", width=0, minwidth=0)
	verconsulta_ventas.column ("cuatro",width=20, minwidth=20)
	verconsulta_ventas.column ("uno",width=400, minwidth=400)
	verconsulta_ventas.column ("dos",width=95, minwidth=95)
	verconsulta_ventas.heading ("cuatro", text="Id")
	verconsulta_ventas.heading ("uno", text="Producto")
	verconsulta_ventas.heading ("dos", text="Precio")
	verconsulta_ventas.grid(row=0, column=0)
	verconsulta_ventas.bind('<Double-Button-1>', asignar_prod2)

	verconsulta_ventas.delete(*verconsulta_ventas.get_children())
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute("SELECT id, producto, precio FROM productos WHERE id LIKE ?",(buscar_prod_id.get(),))
	mercaderia=cursor.fetchall() 
	for m in mercaderia:

		verconsulta_ventas.insert("", "end", values=(m))
	conexion.close()
	abrir_precio()



def aplicar_descuento ():
	x=total_var.get()
	y=desc.get()
	r=x-x*(y/100)
	saldo.set(r)
	venta_computar.set(r)




def abrir_productos(event):

	def asignar_prod(event):
		x=verconsulta_ventas.set(verconsulta_ventas.selection())
		if len(prod_var.get()) ==0:
			prod_var.set(x.get('uno')), id_var.set(x.get('cuatro')), pre_var.set(x.get('dos')), total_uni_var.set(0)
		elif len (prod_var.get())!=0 and len (prod_var2.get())==0 :
			prod_var2.set(x.get('uno')), id_var2.set(x.get('cuatro')), pre_var2.set(x.get('dos')), total_uni_var2.set(0)
		elif len (prod_var2.get())!=0 and len (prod_var3.get())==0:
			prod_var3.set(x.get('uno')), id_var3.set(x.get('cuatro')), pre_var3.set(x.get('dos')), total_uni_var3.set(0) 
		elif len (prod_var3.get())!=0 and len (prod_var4.get())==0:
			prod_var4.set(x.get('uno')), id_var4.set(x.get('cuatro')), pre_var4.set(x.get('dos')), total_uni_var4.set(0) 
		elif len (prod_var4.get())!=0 and len (prod_var5.get())==0:
			prod_var5.set(x.get('uno')), id_var5.set(x.get('cuatro')), pre_var5.set(x.get('dos')), total_uni_var5.set(0) 
		buscando_ptos.destroy()
		buscar_prod_venta.set('')









	buscando_ptos=Toplevel(width=250, height=300)
	buscando_ptos.attributes('-topmost', 'true')

	verconsulta_ventas=ttk.Treeview(buscando_ptos) 
	verconsulta_ventas ["columns"]= ("cuatro","uno", "dos")
	verconsulta_ventas.column ("#0", width=0, minwidth=0)
	verconsulta_ventas.column ("cuatro",width=20, minwidth=20)
	verconsulta_ventas.column ("uno",width=400, minwidth=400)
	verconsulta_ventas.column ("dos",width=95, minwidth=95)
	verconsulta_ventas.heading ("cuatro", text="Id")
	verconsulta_ventas.heading ("uno", text="Producto")
	verconsulta_ventas.heading ("dos", text="Precio")
	verconsulta_ventas.grid(row=0, column=0)
	verconsulta_ventas.bind('<Double-Button-1>', asignar_prod)

	verconsulta_ventas.delete(*verconsulta_ventas.get_children())
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute("SELECT id, producto, precio FROM productos WHERE producto LIKE ?",(buscar_prod_venta.get()+'%',))
	mercaderia=cursor.fetchall() 
	for m in mercaderia:

		verconsulta_ventas.insert("", "end", values=(m))
	conexion.close()
	

def comenzar_venta ():
	if len (cliente_consulta.get())==0:
		messagebox.showinfo('','Recuerda asociar un cliente')
	else:
		id_var.set(0)
		id_var2.set(0)
		id_var3.set(0)
		id_var4.set(0)
		id_var5.set(0)
		prod_var.set('')
		prod_var2.set('')
		prod_var3.set('')
		prod_var4.set('')
		prod_var5.set('')
		cant_var.set(0)
		cant_var2.set(0)
		cant_var3.set(0)
		cant_var4.set(0)
		cant_var5.set(0)
		pre_var.set(0)
		pre_var2.set(0)
		pre_var3.set(0)
		pre_var4.set(0)
		pre_var5.set(0)
		total_uni_var.set(0)
		total_uni_var2.set(0)
		total_uni_var3.set(0)
		total_uni_var4.set(0)
		total_uni_var5.set(0)
		total_var.set(0)
		desc.set(0)
		saldo.set(0)
		saldo.set(0)
		fin_venta.config(state='normal')
		entry_buscar_prod_ventas.config(state='normal')
		entry_buscar_prod_id.config(state='normal')
		nueva_venta.config(state='normal')

	

def nueva_venta2 ():
	entry_num_venta.config(state='disable')
	
	fin_venta.config(state='normal')
	entry_buscar_prod_ventas.config(state="normal")
	entry_buscar_prod_id.config(state="normal")
	
	if len (cliente_consulta.get())!=0:
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute('''CREATE TABLE IF NOT EXISTS asociados (numero INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER (10000), fecha TEXT, nombre VARCHAR (100) NOT NULL, apellido VARCHAR (100) NOT NULL, 
			dni VARCHAR(100), telefono VARCHAR(100), saldo INTEGER (10000), detalle VARCHAR, venta_total NUMERIC, tarjeta NUMERIC, debito NUMERIC, credito NUMERIC, efectivo NUMERIC, descuento TEXT )''')
		conexion.commit()
		conexion.close()

		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("INSERT INTO asociados VALUES (null, ?,?,?,?,?,?,?,null, null, null,null,null,null,null)", (id_busqueda3.get(),fecha_var.get(), cliente_consulta.get(), apellido_consulta.get(),DNI_consulta.get(), tel_consulta.get(), saldo.get(),))
		conexion.commit()
		conexion.close()

		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("SELECT MAX (numero) FROM asociados" )
		numero_imprimir=cursor.fetchone()
		conexion.close()
		numero_imprimir2=list(numero_imprimir)
		num_venta.set(numero_imprimir2[0])
	else:
		messagebox.showinfo("Error", "Debes introducir un cliente")


def precio_x_cantidad(event):
	try:
		total_uni_var.set (float(cant_var.get()) * float(pre_var.get()))
		total_uni_var2.set (float(cant_var2.get()) * float(pre_var2.get()))
		total_uni_var3.set(float(cant_var3.get()) * float(pre_var3.get()))
		total_uni_var4.set(float(cant_var4.get()) * float(pre_var4.get()))
		total_uni_var5.set(float(cant_var5.get()) * float(pre_var5.get()))
		x=(float(total_uni_var.get())+float(total_uni_var2.get())+float(total_uni_var3.get())+float(total_uni_var4.get())+float(total_uni_var5.get()))
		total_var.set(x)
		venta_computar.set(x)
		saldo.set(x)
	except TclError:
		messagebox.showinfo('Error','Introduce solamente valores numéricos')


	

	

def consulta_cliente_ventas():
	def captar_id (event):
		x=verconsulta3.set(verconsulta3.selection())
		id_busqueda3.set(x.get("cuatro"))
		cliente_consulta.set(x.get("dos"))
		apellido_consulta.set(x.get("uno"))
		tel_consulta.set(x.get("tres"))
		DNI_consulta.set(x.get("cinco"))
		ventana_buscar_id_ventas.destroy()

	def buscando_id_ventas():
		verconsulta3.delete(*verconsulta3.get_children())
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("SELECT id, apellido, nombre, telefono, DNI FROM clientes WHERE apellido LIKE ?",(apellido_ventas.get()+'%',))
		usuarios=cursor.fetchall()
		for u in usuarios:

			verconsulta3.insert("", "end", values=(u))
		conexion.close()


	apellido_ventas=StringVar()
	ventana_buscar_id_ventas=Toplevel(width=450, height=500)
	ventana_buscar_id_ventas.title("Buscar Id Cliente")
	ventana_buscar_id_ventas.attributes('-topmost', 'true')
	label_apellido_ventas=Label(ventana_buscar_id_ventas, text="Apellido")
	label_apellido_ventas.grid(row=0, column=0, padx=3, pady=3)
	entry_apellido_ventas=Entry(ventana_buscar_id_ventas, textvariable=apellido_ventas)
	entry_apellido_ventas.grid(row=0, column=1, padx=3, pady=3)
	boton_cons_ventas=Button(ventana_buscar_id_ventas, text='Cosultar', command = buscando_id_ventas).grid(row=0, column=3)

	#treeview de la busqueda de cliente
	verconsulta3=ttk.Treeview(ventana_buscar_id_ventas) 
	verconsulta3 ["columns"]= ("cuatro","uno", "dos", "tres", "cinco")
	verconsulta3.column ("cuatro", width=60, minwidth=60)
	verconsulta3.column ("#0", width=0, minwidth=0)
	verconsulta3.heading ("cuatro", text="Id")
	verconsulta3.heading ("uno", text="Nombre")
	verconsulta3.heading ("dos", text="Apellido")
	verconsulta3.heading ("tres",text="Telefono")
	verconsulta3.heading("cinco", text="DNI")
	verconsulta3.grid(row=2, column=0, columnspan=4)
	ventana_buscar_id_ventas.bind('<Double-Button-1>', captar_id)


frame3=Frame(pestaña)
frame3.pack(fill="both", expand=1)
pestaña.add(frame3, text="Venta    ")

id_busqueda3=StringVar()
Label_id_venta=Label(frame3, text='Id Cliente',font=('time new roman', 10, 'bold')).grid(row=1, column=0)
entry_id_venta=Entry(frame3, textvariable=id_busqueda3)
entry_id_venta.grid(row=1, column=1, sticky='w')
entry_id_venta.config(state='disable')
boton_consultar_venta=Button(frame3, text="Consultar Cliente", command=consulta_cliente_ventas).grid(row=1, column=2, sticky='w')

#Presentación del cliente

cliente_consulta=StringVar()
label_cliente_venta=Label(frame3, text='Nombre',font=('time new roman', 10, 'bold')).grid(row=2, column=0)
entry_cliente_venta=Entry(frame3, textvariable=cliente_consulta)
entry_cliente_venta.grid(row=2, column=1, sticky='w')
entry_cliente_venta.config(state='disable')

apellido_consulta=StringVar()
label_apellido_venta=Label(frame3, text='Apellido',font=('time new roman', 10, 'bold')).grid(row=2, column=2)
entry_apellido_venta=Entry(frame3, textvariable=apellido_consulta)
entry_apellido_venta.grid(row=2, column=3, sticky='w')
entry_apellido_venta.config(state='disable')

DNI_consulta=StringVar()
label_DNI_venta=Label(frame3, text='DNI',font=('time new roman', 10, 'bold')).grid(row=2, column=4, sticky='w')
entry_DNI_venta=Entry(frame3, textvariable=DNI_consulta)
entry_DNI_venta.grid(row=2, column=5, sticky='w')
entry_DNI_venta.config(state='disable')

tel_consulta=StringVar()
label_tel_venta=Label(frame3, text='Telefono',font=('time new roman', 10, 'bold')).grid(row=2, column=6, sticky='w')
entry_tel_venta=Entry(frame3, textvariable=tel_consulta)
entry_tel_venta.grid(row=2, column=7, sticky='w')
entry_tel_venta.config(state='disable')

#label separador
label_separador=Label(frame3, bg='white', width=200).grid(row=3, column=0, columnspan=9, sticky='we')

#label planilla de venta

label_planilla=Label(frame3, text='Planilla de Ventas', font=("time new roman", 30), fg='black').grid(row=4, column=0, columnspan=8)

#Construcción de la planilla de venta....
num_venta=IntVar(0)
Label_num_venta=Label(frame3, text= "Número de Venta", font= ("time new roman", 13, 'bold'), padx=9, pady=15).grid(row=5, column=0, sticky='w')
entry_num_venta=Entry(frame3, textvariable=num_venta, font=('time new roman', 12), width=10)
entry_num_venta.grid(row=5, column=1,  sticky='w')
entry_num_venta.config(state="disable")
entry_num_venta.bind('<Return>', consultar_ventas)

#Buscar por nombre e ID

buscar_prod_venta=StringVar()
label_buscar_prod_ventas=Label(frame3, text="Consultar producto", font=('time new roman', 12))
label_buscar_prod_ventas.grid(row=5, column=4, sticky='w')
entry_buscar_prod_ventas=Entry(frame3, textvariable=buscar_prod_venta, font=('time new roman', 12))
entry_buscar_prod_ventas.grid(row=5, column=5, sticky='w')
entry_buscar_prod_ventas.bind('<Return>', abrir_productos)
entry_buscar_prod_ventas.config(state="disable")

buscar_prod_id=StringVar()
label_buscar_prod_id=Label(frame3, text="Consultar por Codigo", font=('time new roman', 12))
label_buscar_prod_id.grid(row=5, column=2, sticky='w')
entry_buscar_prod_id=Entry(frame3, textvariable=buscar_prod_id, font=('time new roman', 12))
entry_buscar_prod_id.grid(row=5, column=3, sticky='w')
entry_buscar_prod_id.bind('<Return>', abrir_productos_con_id)
entry_buscar_prod_id.config(state="disable")

fecha_var=StringVar()
fecha=Label(frame3, text='Fecha', font=('time new roman', 12)).grid(row=6, column=0)
entry_fecha=Entry(frame3, textvariable=fecha_var, font=('time new roman', 12))
entry_fecha.grid(row=7, column=0)
entry_fecha.config(state='disable', justify="center")
dt=datetime.now()
fecha_var.set("{}/{}/{}".format(dt.day, dt.month, dt.year))

def trocar_fecha():
	if otra_fecha.get()==1:
		entry_fecha.config(state='normal')
	else:entry_fecha.config(state='disable')

otra_fecha=IntVar()
cambiar_fecha=Checkbutton(frame3, text='Cambiar Fecha', variable=otra_fecha, onvalue=1, offvalue=0, command=trocar_fecha).grid(row=14, column=0)



id_var=IntVar()
id_var2=IntVar()
id_var3=IntVar()
id_var4=IntVar()
id_var5=IntVar()


prod2=Label(frame3, text='Código',font=('time new roman', 12)).grid(row=6, column=1, sticky='w')
entry_prod2=Entry(frame3, textvariable=id_var, width=10, state='disable', font=('time new roman', 12))
entry_prod2.grid(row=7, column=1, sticky='w')
entry_prod2=Entry(frame3, textvariable=id_var2, width=10, state='disable', font=('time new roman', 12))
entry_prod2.grid(row=8, column=1, sticky='w')
entry_prod2=Entry(frame3, textvariable=id_var3, width=10, state='disable', font=('time new roman', 12))
entry_prod2.grid(row=9, column=1, sticky='w')
entry_prod2=Entry(frame3, textvariable=id_var4, width=10, state='disable', font=('time new roman', 12))
entry_prod2.grid(row=10, column=1, sticky='w')
entry_prod2=Entry(frame3, textvariable=id_var5, width=10, state='disable', font=('time new roman', 12))
entry_prod2.grid(row=11, column=1, sticky='w')

prod_var=StringVar()
prod_var2=StringVar()
prod_var3=StringVar()
prod_var4=StringVar()
prod_var5=StringVar()
prod=Label(frame3, text='Producto', font=('time new roman', 12)).grid(row=6, column=2)

entry_prod1=Entry(frame3, textvariable=prod_var, width=50, state='disable', font=('time new roman', 12))
entry_prod1.grid(row=7, column=2, columnspan=4, sticky='w')
entry_prod2=Entry(frame3, textvariable=prod_var2, width=50, state='disable', font=('time new roman', 12))
entry_prod2.grid(row=8, column=2, columnspan=4, sticky='w')
entry_prod3=Entry(frame3, textvariable=prod_var3, width=50, state='disable', font=('time new roman', 12))
entry_prod3.grid(row=9, column=2, columnspan=4, sticky='w')
entry_prod4=Entry(frame3, textvariable=prod_var4, width=50, state='disable', font=('time new roman', 12))
entry_prod4.grid(row=10, column=2, columnspan=4, sticky='w')
entry_prod5=Entry(frame3, textvariable=prod_var5, width=50, state='disable', font=('time new roman', 12))
entry_prod5.grid(row=11, column=2, columnspan=4, sticky='w')

	

cant_var=IntVar()
cant_var2=IntVar()
cant_var3=IntVar()
cant_var4=IntVar()
cant_var5=IntVar()


cant=Label(frame3, text='Cantidad',font=('time new roman', 12)).grid(row=6, column=4)
cant_pre=Entry(frame3, textvariable=cant_var, width=10, justify="right", font=('time new roman', 12))
cant_pre.grid(row=7, column=4)
cant_pre.bind('<Return>', precio_x_cantidad)
cant_pre2=Entry(frame3, textvariable=cant_var2, width=10, justify="right", font=('time new roman', 12))
cant_pre2.grid(row=8, column=4)
cant_pre2.bind('<Return>', precio_x_cantidad)
cant_pre3=Entry(frame3, textvariable=cant_var3, width=10, justify="right", font=('time new roman', 12))
cant_pre3.grid(row=9, column=4)
cant_pre3.bind('<Return>', precio_x_cantidad)
cant_pre4=Entry(frame3, textvariable=cant_var4, width=10, justify="right", font=('time new roman', 12))
cant_pre4.grid(row=10, column=4)
cant_pre4.bind('<Return>', precio_x_cantidad)
cant_pre5=Entry(frame3, textvariable=cant_var5, width=10, justify="right", font=('time new roman', 12))
cant_pre5.grid(row=11, column=4)
cant_pre5.bind('<Return>', precio_x_cantidad)


pre_var=IntVar()
pre_var2=IntVar()
pre_var3=IntVar()
pre_var4=IntVar()
pre_var5=IntVar()
pre=Label(frame3, text='Precio',font=('time new roman', 12)).grid(row=6, column=5)
entry_pre=Entry(frame3, textvariable=pre_var, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_pre.grid(row=7, column=5)
entry_pre.config(state='disable')
entry_pre2=Entry(frame3, textvariable=pre_var2, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_pre2.grid(row=8, column=5)
entry_pre3=Entry(frame3, textvariable=pre_var3, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_pre3.grid(row=9, column=5)
entry_pre4=Entry(frame3, textvariable=pre_var4, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_pre4.grid(row=10, column=5)
entry_pre5=Entry(frame3, textvariable=pre_var5, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_pre5.grid(row=11, column=5)

total_uni_var=IntVar()
total_uni_var2=IntVar()
total_uni_var3=IntVar()
total_uni_var4=IntVar()
total_uni_var5=IntVar()


prod2=Label(frame3, text='Totales por Producto',font=('time new roman', 12)).grid(row=6, column=6)
entry_total_unid=Entry(frame3, textvariable=total_uni_var, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_total_unid.grid(row=7, column=6)
entry_total_unid=Entry(frame3, textvariable=total_uni_var2, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_total_unid.grid(row=8, column=6)
entry_total_unid=Entry(frame3, textvariable=total_uni_var3, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_total_unid.grid(row=9, column=6)
entry_total_unid=Entry(frame3, textvariable=total_uni_var4, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_total_unid.grid(row=10, column=6)
entry_total_unid=Entry(frame3, textvariable=total_uni_var5, width=10, justify="right", state='disable', font=('time new roman', 12))
entry_total_unid.grid(row=11, column=6)


total_var=IntVar()
total=Label(frame3, text='Total', font=('time new roman', 12)).grid(row=12, column=4)
entry_total=Entry(frame3, textvariable=total_var, justify="right", state='disable', font=('time new roman', 12))
entry_total.grid(row=12, column=5)

#Descuento
desc=IntVar()
entry_desc=Entry(frame3, textvariable=desc, justify="right", font=('time new roman', 12))
entry_desc.grid(row=13, column=5)
label_desc=Label(frame3, text='Desc.%', font=('time new roman', 12)).grid(row=13, column=6)


#Detalle

detalle=StringVar()
#total_final=IntVar()
#entry_total_final=Entry(frame3, textvariable=total_final)
#entry_total_final.grid(row=14, column=5)
#entry_total_final.config(state='disable')
#label_total_final=Label(frame3, text='Total con descuento').grid(row=14, column=6)

#Pagos y entregas
pagos=StringVar()
#entry_pagos=Entry(frame3, textvariable=pagos)
#entry_pagos.grid(row=15, column=5)

# Saldo

saldo=IntVar()
label_saldo=Label(frame3, text='Saldo', font=('time new roman', 16))
label_saldo.grid(row=16, column=4)
entry_saldo=Entry(frame3, textvariable=saldo, justify="right", state='disable', font=('time new roman', 12))
entry_saldo.grid(row=16, column=5)

venta_computar=IntVar()
label_venta_com=Label(frame3, text='Venta Total', font=('time new roman', 12))
label_venta_com.grid(row=15, column=4)
entry_venta_com=Entry(frame3, textvariable=venta_computar, justify="right", state='disable', font=('time new roman', 12))
entry_venta_com.grid(row=15, column=5)

#botones planilla de ventas

nueva_venta=Button(frame3, text='Nueva Venta', command=comenzar_venta)
nueva_venta.grid(row=8, column=0, padx=8, pady=8, sticky='wens')
Consultar_venta=Button(frame3, text='Consultar', command=habilitar_ventas)
Consultar_venta.grid(row=9, column=0, padx=8, pady=8, sticky='wens')
#Nota_credito=Button(frame3, text='Nota de Crédito').grid(row=10, column=0, padx=8, pady=8, sticky='wens')
Editar_venta=Button(frame3, text='Editar', command=editar_venta_cargada)
Editar_venta.grid(row=10, column=0, padx=8, pady=8, sticky='wens')
Editar_venta.config(state='disable')
Eliminar_venta=Button(frame3, text='Eliminar', command=eliminar_venta_cargada)
Eliminar_venta.grid(row=11, column=0, padx=8, pady=8, sticky='wens')
Eliminar_venta.config(state='disable')
fin_venta=Button(frame3, text='Finalizar', command=cargar_venta)
fin_venta.grid(row=12, column=0, padx=8, pady=8, sticky='wens')
fin_venta.config(state='disable')
#boton_pagos=Button(frame3, text='PAGO', command=aplicar_pago)
#boton_pagos.grid(row=17, column=5, padx=8, pady=8, sticky='wens')
#boton_pagos.config(state='disable')
aplicar_descuento_boton=Button(frame3, text='Aplicar desc.', command=aplicar_descuento).grid(row=13, column=7, sticky='w')
limpiar_todo=Button(frame3, text='Limpiar', command=limpiar_planilla)
limpiar_todo.grid(row=13, column=0, padx=8, pady=8, sticky='wens')





#Creación ficha de cliente

def eliminar_linea(event):
	a=messagebox.askquestion('Eliminar', '¿Desea Eliminar el renglon?' )
	if a =='yes':
		x=verconsulta4.set(verconsulta4.selection())
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute('DELETE FROM asociados WHERE numero=?', (x.get("cuatro"),))
		
		
		cursor.execute('UPDATE consolidado SET saldo =? WHERE id=?', (0, ID_consulta2.get()))
		conexion.commit()
		conexion.close()
		consultar_ficha1()

def limpiar_ficha():
	verconsulta4.delete(*verconsulta4.get_children())
	cliente_consulta2.set('')
	apellido_consulta2.set('')
	DNI_consulta2.set('')
	tel_consulta2.set('')
	ID_consulta2.set('')
	entry_ID_venta.config(state="normal")


def consultar_ficha1():
	verconsulta4.delete(*verconsulta4.get_children())
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute("SELECT numero, fecha, detalle, venta_total, efectivo, tarjeta, debito, credito, saldo,descuento FROM asociados WHERE id=?", (ID_consulta2.get(),))
	usuarios=cursor.fetchall()
	for u in usuarios:

		verconsulta4.insert("", "end", values=(u))
	conexion.close()
	acumular_saldo()


def pago_ficha():
	def acreditar_ficha(event):
		
		dt=datetime.now()
		dt_format=("{}/{}/{}".format(dt.day, dt.month, dt.year))
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("INSERT INTO asociados (numero,id, fecha,nombre, apellido, detalle, efectivo, debito, credito, saldo, tarjeta, venta_total) VALUES (null,?,?,?,?,?,?,?,?,?,?,?)", (ID_consulta2.get(),dt_format,'', '','PAGO EN EFECTIVO',efectivo1.get(),0,0,0,0,0))
		conexion.commit()
		conexion.close()
		
		

		level_pago.destroy()
		acumular_saldo2(ID_consulta2.get())
		consultar_ficha1()

	def acreditar_ficha_TC(event):
		dt=datetime.now()
		dt_format=("{}/{}/{}".format(dt.day, dt.month, dt.year))
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("INSERT INTO asociados (numero,id, fecha,nombre, apellido, detalle, efectivo, debito, credito, saldo, tarjeta, venta_total) VALUES (null,?,?,?,?,?,?,?,?,?,?,?)", (ID_consulta2.get(),dt_format,'', '','PAGO EN EFECTIVO',0,0,0,0, TC_ficha.get(),0))
		cursor.execute('UPDATE consolidado SET dias=? WHERE id =? ', ('0', id_busqueda3.get()))
		conexion.commit()
		conexion.close()
		level_pago.destroy()
		acumular_saldo2(ID_consulta2.get())
		consultar_ficha1() 


	TC_ficha=DoubleVar()
	efectivo1=DoubleVar()
	level_pago=Toplevel()
	level_pago.config()
	label1=Label(level_pago, text='Efectivo', font=('time new roman', 16, 'bold'), padx=12, pady=12).grid(row=0, column=0)
	entry1=Entry(level_pago, textvariable=efectivo1, font=('time new roman', 16))
	entry1.grid(row=0, column=1)
	entry1.config(justify='right')
	entry1.bind('<Return>', acreditar_ficha)
	label2=Label(level_pago, text='Tarjeta', font=('time new roman', 16, 'bold'), padx=12, pady=12).grid(row=1, column=0)
	entry2=Entry(level_pago, textvariable=TC_ficha, font=('time new roman', 16))
	entry2.grid(row=1, column=1)
	entry2.config(justify='right')
	entry2.bind('<Return>', acreditar_ficha_TC)

def ND_ficha():
	def debitar_ficha(event):
		dt=datetime.now()
		dt_format=("{}/{}/{}".format(dt.day, dt.month, dt.year))
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("INSERT INTO asociados (numero,id, fecha,nombre, apellido, detalle, debito, saldo, credito, efectivo, tarjeta, venta_total) VALUES (null,?,?,?,?,?,?,?,?,?,?,?)", (ID_consulta2.get(),dt_format,'', '','NOTA DE DEBITO',debito1.get(),0,0,0,0,0))
		conexion.commit()
		conexion.close()
		level_pago.destroy()
		consultar_ficha1()

	debito1=DoubleVar()
	level_pago=Toplevel()
	level_pago.config()
	label1=Label(level_pago, text='Nota de Débito', font=('time new roman', 16, 'bold'), padx=12, pady=12).grid(row=0, column=0)
	entry1=Entry(level_pago, textvariable=debito1, font=('time new roman', 16))
	entry1.grid(row=0, column=1)
	entry1.config(justify='right')
	entry1.bind('<Return>', debitar_ficha)

def NC_ficha():
	def credito_ficha(event):
		dt=datetime.now()
		dt_format=("{}/{}/{}".format(dt.day, dt.month, dt.year))
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("INSERT INTO asociados (numero,id, fecha,nombre, apellido, detalle,saldo,debito, credito,efectivo, tarjeta, venta_total) VALUES (null,?,?,?,?,?,?,?,?,?,?,?)", (ID_consulta2.get(),dt_format,'', '','NOTA DE CREDITO',0,0,credito1.get(),0,0,0))
		cursor.execute('UPDATE consolidado SET dias=? WHERE id =? ', ('0', id_busqueda3.get()))
		conexion.commit()
		conexion.close()
		level_pago.destroy()
		acumular_saldo2(ID_consulta2.get())
		consultar_ficha1()

	credito1=DoubleVar()
	level_pago=Toplevel()
	level_pago.config()
	label1=Label(level_pago, text='Nota de Crédito', font=('time new roman', 16, 'bold'), padx=12, pady=12).grid(row=0, column=0)
	entry1=Entry(level_pago, textvariable=credito1, font=('time new roman', 16))
	entry1.grid(row=0, column=1)
	entry1.config(justify='right')
	entry1.bind('<Return>', credito_ficha)


def consulta_cliente_ficha (event):
	def captar_id (event):
		x=verconsulta3.set(verconsulta3.selection())
		ID_consulta2.set(x.get("cuatro"))
		cliente_consulta2.set(x.get("dos"))
		apellido_consulta2.set(x.get("uno"))
		tel_consulta2.set(x.get("tres"))
		DNI_consulta2.set(x.get("cinco"))
		buscar_cliente_ficha.destroy()

	def buscando_id_ventas():
		verconsulta3.delete(*verconsulta3.get_children())
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute("SELECT id, apellido, nombre, telefono, DNI FROM clientes WHERE apellido LIKE ?",(apellido_ventas.get()+'%',))
		usuarios=cursor.fetchall()
		for u in usuarios:

			verconsulta3.insert("", "end", values=(u))
		conexion.close()



	apellido_ventas=StringVar()
	buscar_cliente_ficha=Toplevel(width=250, height=300)
	buscar_cliente_ficha.attributes('-topmost', 'true')
	buscar_cliente_ficha.title("Cliente")
	label_apellido_ventas=Label(buscar_cliente_ficha, text="Apellido")
	label_apellido_ventas.grid(row=0, column=0, padx=3, pady=3)
	entry_apellido_ventas=Entry(buscar_cliente_ficha, textvariable=apellido_ventas)
	entry_apellido_ventas.grid(row=0, column=1, padx=3, pady=3)
	boton_cons_ventas=Button(buscar_cliente_ficha, text='Cosultar', command = buscando_id_ventas).grid(row=0, column=3)

	#treeview de la busqueda de cliente
	verconsulta3=ttk.Treeview(buscar_cliente_ficha) 
	verconsulta3 ["columns"]= ("cuatro","uno", "dos", "tres", "cinco")
	verconsulta3.column ("cuatro", width=60, minwidth=60)
	verconsulta3.column ("#0", width=0, minwidth=0)
	verconsulta3.heading ("cuatro", text="Id")
	verconsulta3.heading ("uno", text="Nombre")
	verconsulta3.heading ("dos", text="Apellido")
	verconsulta3.heading ("tres",text="Telefono")
	verconsulta3.heading("cinco", text="DNI")
	verconsulta3.grid(row=3, column=0, columnspan=4)
	buscar_cliente_ficha.bind('<Double-Button-1>', captar_id)

	
	entry_ID_venta.config(state="disable")


frame4=Frame(pestaña, bg="sky blue")
frame4.pack(fill="both", expand=1)
pestaña.add(frame4, text="Ficha del Cliente   ")


cliente_consulta2=StringVar()
label_cliente_venta=Label(frame4, text='Nombre', pady=5, font=('time new roman', 11), width=12).grid(row=2, column=0)
entry_cliente_venta=Entry(frame4, textvariable=cliente_consulta2, font=('time new roman', 11))
entry_cliente_venta.grid(row=2, column=1, sticky='w')
entry_cliente_venta.config(state='disable')

apellido_consulta2=StringVar()
label_apellido_venta=Label(frame4, text='Apellido', pady=5, font=('time new roman', 11), width=12).grid(row=2, column=2)
entry_apellido_venta=Entry(frame4, textvariable=apellido_consulta2, font=('time new roman', 11))
entry_apellido_venta.grid(row=2, column=3, sticky='w')
entry_apellido_venta.config(state='disable')

DNI_consulta2=StringVar()
label_DNI_venta=Label(frame4, text='DNI', font=('time new roman', 11), width=12).grid(row=2, column=4)
entry_DNI_venta=Entry(frame4, textvariable=DNI_consulta2,  font=('time new roman', 11))
entry_DNI_venta.grid(row=2, column=5, sticky='w')
entry_DNI_venta.config(state='disable')

tel_consulta2=StringVar()
label_tel_venta=Label(frame4, text='Telefono',  font=('time new roman', 11), width=12).grid(row=2, column=6)
entry_tel_venta=Entry(frame4, textvariable=tel_consulta2, font=('time new roman', 11))
entry_tel_venta.grid(row=2, column=7, sticky= 'w')
entry_tel_venta.config(state='disable')

ID_consulta2=StringVar()
label_ID_venta=Label(frame4, text='ID', width=12).grid(row=2, column=8)
entry_ID_venta=Entry(frame4, textvariable=ID_consulta2)
entry_ID_venta.grid(row=2, column=9, sticky='w')
entry_ID_venta.config(state='normal')
entry_ID_venta.bind("<Return>", consulta_cliente_ficha)
#treeview de la busqueda de cliente
estilo=ttk.Style()
estilo.configure("estilo.Treeview", font=('time new roman', 10))
estilo.configure("estilo.Treeview.Heading", font=('time new roman', 11, 'bold'),fieldbackground='yellow')

verconsulta4=ttk.Treeview(frame4,style="estilo.Treeview", height=25) 

vsb = ttk.Scrollbar(frame4, orient="vertical", command=verconsulta4.yview)
vsb.grid(row=3, column=10, sticky='ns')
verconsulta4.configure(yscrollcommand=vsb.set)


verconsulta4 ["columns"]= ("cuatro","uno", "dos", "tres", "cinco", "seis","siete", "ocho","nueve","diez")
verconsulta4.column ("#0", width=0, minwidth=0)
verconsulta4.heading ("cuatro", text="Nº de Venta")
verconsulta4.column ("cuatro", width=100, minwidth=100)
verconsulta4.heading ("uno", text="Fecha")
verconsulta4.column ("uno", width=70, minwidth=70)
verconsulta4.heading ("dos", text="Detalle")
verconsulta4.column ("dos", width=450, minwidth=450)
verconsulta4.heading ("tres",text="Valor de la Venta")
verconsulta4.column ("tres", width=135, minwidth=120)
verconsulta4.heading("cinco", text="Pago efvo.")
verconsulta4.column ("cinco", width=100, minwidth=100)
verconsulta4.heading("seis", text="Pago TC")
verconsulta4.column ("seis", width=100, minwidth=100)
verconsulta4.heading("siete", text="Nota Débito")
verconsulta4.column ("siete", width=100, minwidth=100)
verconsulta4.heading("ocho", text="Nota Crédito")
verconsulta4.column ("ocho", width=100, minwidth=100)
verconsulta4.heading("nueve", text="Saldo")
verconsulta4.column ("nueve", width=100, minwidth=100)
verconsulta4.heading("diez", text="Descuento")
verconsulta4.column ("diez", width=100, minwidth=100)
verconsulta4.grid(row=3, column=0, columnspan=10, sticky='w')
verconsulta4.bind('<Double-Button-1>', eliminar_linea)

#ventana_buscar_id_ventas.bind('<Double-Button-1>', captar_id)

#Saldo acumulado del cliente
saldo_para_lineas_eliminadas=IntVar()

saldo_acumulado=IntVar()
Label_saldo_acumulado=Label(frame4, text='Saldo cliente', font=('time new roman', 17) ).grid(row=4, column=5)
entry_saldo_acumulado=Entry(frame4, textvariable=saldo_acumulado, font=('time new roman', 17), justify='right')
entry_saldo_acumulado.grid(row=4, column=6, columnspan=4)
#funcion para acumular saldo del cliente

def acumular_saldo():
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute('SELECT SUM (venta_total) FROM asociados WHERE id=?', (ID_consulta2.get(),))
	acumulado=cursor.fetchone()
	cursor1=conexion.cursor()
	cursor1.execute('SELECT SUM (efectivo) FROM asociados WHERE id=?', (ID_consulta2.get(),))
	acumulado1=cursor1.fetchone()
	cursor2=conexion.cursor()
	cursor2.execute('SELECT SUM (credito) FROM asociados WHERE id=?', (ID_consulta2.get(),))
	acumulado2=cursor2.fetchone()
	cursor3=conexion.cursor()
	cursor3.execute('SELECT SUM (debito) FROM asociados WHERE id=?', (ID_consulta2.get(),))
	acumulado3=cursor3.fetchone()

	cursor4=conexion.cursor()
	cursor4.execute('SELECT SUM (tarjeta) FROM asociados WHERE id=?', (ID_consulta2.get(),))
	acumulado4=cursor4.fetchone()
	
	
	
	saldo_lista=list (acumulado)
	saldo_entero=saldo_lista[0]
	
	efectivo_lista=list (acumulado1)
	efectivo_entero=efectivo_lista[0]

	credito_lista=list (acumulado2)
	credito_entero=(credito_lista[0])
	
	debito_lista=list (acumulado3)
	debito_entero=(debito_lista[0])

	tarjeta_lista=list (acumulado4)
	tarjeta_entero=(tarjeta_lista[0])

	

	saldo_cosolidado=saldo_entero-efectivo_entero-credito_entero-tarjeta_entero+debito_entero
	#print(saldo_cosolidado)

	#saldo_acumulado.set(acumulado)
	saldo_acumulado.set(saldo_cosolidado)
	saldo_para_lineas_eliminadas.set(saldo_acumulado)
	saldo_cosolidado=(locale.format_string('%.2f',saldo_cosolidado, grouping=True))
	saldo_acumulado.set('$ {}'.format(saldo_cosolidado)) 
	

	

#Botones ficha cliente
consultar_ficha=Button(frame4, bg="pink",text="Consultar Ficha", command=consultar_ficha1, width=15).grid(row=4, column=0, padx=5, pady=5, sticky="we")
pagar=Button(frame4, bg="pink", text= "Pagar",command=pago_ficha, width=15).grid(row=4, column=1,padx=5, pady=5, sticky="ew")
ND=Button(frame4, bg="pink", text= "Nota de Débito", width=15, command=ND_ficha).grid(row=4, column=2,padx=5, pady=5, sticky="ew")
NC=Button(frame4, bg="pink", text= "Nota de Crédito", width=15, command=NC_ficha).grid(row=4, column=3,padx=5, pady=5, sticky="ew")
limpiar=Button(frame4, bg="pink", text="Limpiar", command=limpiar_ficha, width=15).grid(row=4, column= 4, padx=5, pady=5, sticky="ew")

#Clientes deudores listado automatico

def acumular_saldo2(a):
	#dias_atraso()
	dt=datetime.now()
	dt_format=("{}/{}/{}".format(dt.day, dt.month, dt.year))
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute('SELECT SUM (venta_total) FROM asociados WHERE id=?', (a,))
	acumulado=cursor.fetchone()
	cursor1=conexion.cursor()
	cursor1.execute('SELECT SUM (efectivo) FROM asociados WHERE id=?', (a,))
	acumulado1=cursor1.fetchone()
	cursor2=conexion.cursor()
	cursor2.execute('SELECT SUM (credito) FROM asociados WHERE id=?', (a,))
	acumulado2=cursor2.fetchone()
	cursor3=conexion.cursor()
	cursor3.execute('SELECT SUM (debito) FROM asociados WHERE id=?', (a,))
	acumulado3=cursor3.fetchone()

	cursor4=conexion.cursor()
	cursor4.execute('SELECT SUM (tarjeta) FROM asociados WHERE id=?', (a,))
	acumulado4=cursor4.fetchone()

	saldo_lista=list (acumulado)
	saldo_entero=saldo_lista[0]
	
	efectivo_lista=list (acumulado1)
	efectivo_entero=efectivo_lista[0]

	credito_lista=list (acumulado2)
	credito_entero=(credito_lista[0])
	
	debito_lista=list (acumulado3)
	debito_entero=(debito_lista[0])

	tarjeta_lista=list (acumulado4)
	tarjeta_entero=(tarjeta_lista[0])

	saldo_cosolidado=saldo_entero-efectivo_entero-credito_entero-tarjeta_entero+debito_entero
	cursor.execute('UPDATE consolidado SET saldo =? WHERE id= ?', (saldo_cosolidado, a ))
	cursor.execute('UPDATE consolidado SET  fecha=? WHERE id= ?', (dt_format,a ))
	conexion.commit()
	conexion.close()

def clientes_deudores():
	lista1()
	lista2()
	dias_atraso()
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute('SELECT * FROM consolidado')
	datos=cursor.fetchall()
	conexion.close()

	
				
	pantalla_deudores=Toplevel()
	pantalla_deudores.attributes('-topmost', 'true')
	pantalla_deudores.title('Cuentas por cobrar')
	

	estilo=ttk.Style()
	estilo.configure("estilo.Treeview", font=('time new roman', 10))
	estilo.configure("estilo.Treeview.Heading", font=('time new roman', 11, 'bold'))

	verconsulta5=ttk.Treeview(pantalla_deudores,style="estilo.Treeview",height=30) 

	vsb = ttk.Scrollbar(pantalla_deudores, orient="vertical", command=verconsulta5.yview)
	vsb.grid(row=0, column=1)
	verconsulta5.configure(yscrollcommand=vsb.set)


	dif_fecha=StringVar()
	
	verconsulta5 ["columns"]= ("uno", "dos", "tres", "cuatro", "cinco","siete","seis")
	verconsulta5.column ("#0", width=0, minwidth=0)
	verconsulta5.heading ("uno", text="ID")
	verconsulta5.column ("uno", width=100, minwidth=100)
	verconsulta5.heading ("dos", text="Fecha")
	verconsulta5.column ("dos", width=70, minwidth=70)
	verconsulta5.heading ("tres", text="Nombre")
	verconsulta5.column ("tres", width=150, minwidth=150)
	verconsulta5.heading ("cuatro",text="Apellido")
	verconsulta5.column ("cuatro", width=135, minwidth=120)
	verconsulta5.heading("cinco", text="Saldo")
	verconsulta5.column ("cinco", width=100, minwidth=100)
	verconsulta5.heading("seis", text="Días")
	verconsulta5.column ("seis", width=100, minwidth=100)
	verconsulta5.heading("siete", text="Teléfono")
	verconsulta5.column ("siete", width=100, minwidth=100)

	verconsulta5.grid(row=0, column=0) 

	for d in datos:
		if d[4] >0:
			verconsulta5.insert("",'end', values=d)
	
#clientes_deudores()
lista_resultado=[]
lista_id=[]
pares=[]
def lista1 ():
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute('SELECT * FROM consolidado')
	datos=cursor.fetchall()
	conexion.close()
	hoy=datetime.now()

	for d in datos:
		fecha=str(hoy-datetime.strptime(d[1], '%d/%m/%Y')) 
		lista_resultado.append(fecha)


def lista2 ():
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.execute('SELECT * FROM consolidado')
	datos=cursor.fetchall()
	conexion.close()

	for i in datos:
		lista_id.append(i[0])



def dias_atraso():
	

	
	lista3=zip(lista_resultado, lista_id)
	
	for s in lista3:
		pares.append(s)
	
	
		

	
		
	conexion=sqlite3.connect('clientes.db')
	cursor=conexion.cursor()
	cursor.executemany('UPDATE consolidado SET dias =? WHERE id=? ', (pares))
	conexion.commit()
	conexion.close()

clientes_deudores()
#dias_atraso()
consulta_deuda=Button(frame4, text='Deuda de todos los clientes', command=clientes_deudores, bg='pink').grid(row=5, column= 0, padx=5, pady=5, sticky="ew")

def mostar_ventas_totales():

	def validar(ingreso):
		if len (ingreso)>10:
			return False
		chequeo=[]
		for i, char in enumerate(ingreso):
			if i in  (2,5):
				chequeo.append(char=='/')
			else:
				chequeo.append(char.isdecimal())	

		return all(chequeo)



	visor=Toplevel()
	visor.attributes('-topmost', 'True')
	inicio=StringVar()
	final=StringVar()

	desde=Label(visor, text='Desde', font=('time new roman', 12)).grid(row=0, column=0)
	entry_desde=ttk.Entry(visor, textvariable=inicio, validate='key', validatecommand=(root.register(validar), "%P"))
	entry_desde.grid(row=0, column=1)
	entry_desde.configure(font=('time new roman', 12))
	hasta=Label(visor, text='Hasta', font=('time new roman', 12)).grid(row=0, column=2)
	entry_hasta=Entry(visor, textvariable=final, validate='key', validatecommand=(root.register(validar), "%P"))
	entry_hasta.grid(row=0, column=3)
	entry_hasta.configure(font=('time new roman', 12))



	estilo=ttk.Style()
	estilo.configure("estilo.Treeview", font=('time new roman', 10))
	estilo.configure("estilo.Treeview.Heading", font=('time new roman', 11, 'bold'))

	verconsulta6=ttk.Treeview(visor,style="estilo.Treeview") 

	vsb = ttk.Scrollbar(visor, orient="vertical", command=verconsulta6.yview)
	vsb.grid(row=1, column=5)
	verconsulta6.configure(yscrollcommand=vsb.set)


	
	verconsulta6 ["columns"]= ("uno", "dos", "tres", "cuatro", "cinco")
	verconsulta6.column ("#0", width=0, minwidth=0)
	verconsulta6.heading ("uno", text="Código")
	verconsulta6.column ("uno", width=100, minwidth=100)
	verconsulta6.heading ("dos", text="Producto")
	verconsulta6.column ("dos", width=130, minwidth=130)
	verconsulta6.heading ("tres", text="Precio $")
	verconsulta6.column ("tres", width=70, minwidth=70)
	verconsulta6.heading ("cuatro",text="Cantidad")
	verconsulta6.column ("cuatro", width=70, minwidth=70)
	verconsulta6.heading("cinco", text="Total")
	verconsulta6.column ("cinco", width=100, minwidth=100)
	
	verconsulta6.grid(row=1, column=0, columnspan=5, sticky='we')
	sumatoria=DoubleVar()
	total_total=Label(visor, text='Total', font=('time new roman', 14)).grid(row=3, column=0)
	entry_total_total=Entry(visor, textvariable=sumatoria)
	entry_total_total.grid(row=3, column=1)
	entry_total_total.config(justify='right')



	def ventas_totales():

		verconsulta6.delete(*verconsulta6.get_children())
		conexion=sqlite3.connect('clientes.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM ventas')
		datos=cursor.fetchall()
		conexion.close()
		lista_sumas=[]
		lista_suma2=[]
		finalicima=[]
		finalicima2=[]
		for d in datos:
			if d[2]!=0 and  datetime.strptime(d[1],'%d/%m/%Y')>=datetime.strptime(inicio.get(),'%d/%m/%Y') and  datetime.strptime(d[1],'%d/%m/%Y') <= datetime.strptime(final.get(),'%d/%m/%Y'):
			
				conexion=sqlite3.connect('clientes.db')
				cursor=conexion.cursor()
				cursor.execute('SELECT SUM(cantidad*precio) FROM ventas WHERE Codigo=?', (d[2],))

				a=cursor.fetchall()
				conexion.close()
				

				c=tuple(a[0])
				b=(d[2], d[3], d[5], c[0]/d[5], ('${}'.format(c[0])))
				
				lista_sumas.append(b)
				finalicima.append(c[0])
		for l in lista_sumas:
			if l not in lista_suma2:
				lista_suma2.append(l)

		for l in lista_suma2:
			verconsulta6.insert("",'end', values=l)

		for f in finalicima:
			if f not in finalicima2:
				finalicima2.append(f)

		la_suma=0
		for f in finalicima2:
			la_suma=la_suma + f
			print(la_suma) 
			sumatoria.set('${}'.format(la_suma))
			

		print(la_suma)
	boton_rango_fecha=Button(visor, text='Consultar', command=ventas_totales).grid(row=0, column=4)
		
	
boton_ventas_total=Button(frame2, text='Ventas Totales', command=mostar_ventas_totales, )
boton_ventas_total.grid(row=6, column=0, columnspan=4, sticky='we')
boton_ventas_total.config(font=('time new roman',13))
	

	
		




	
	









root.mainloop()      
