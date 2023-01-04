from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox

root=Tk()

frame=Frame(root)
frame.pack(fill="both", expand=1)
titulo=Label(frame, text="Dividamos por 2 cifras", font=("time new roman", 18, "bold")).grid(row=0, column=0)
primer=IntVar()
segundo=IntVar()
tercero=IntVar()
cuarto=IntVar()
dividendo=Label(frame, text="Dividendo", font=("time new roman", 15)).grid(row=1, column=0)
entry_dividendo=Entry(frame, textvariable=primer, font=("time new roman", 15),justify="right").grid(row=1, column=1)
divisor=Label(frame, text="Divisor", font=("time new roman", 15)	).grid(row=1, column=2)
entry_divisor=Entry(frame, textvariable=segundo, font=("time new roman", 15), justify="right").grid(row=1, column=3)
control1=Label(frame, text="Cociente", font=("time new roman", 15)).grid(row=12, column=0)
entry_control1=Entry(frame, textvariable=tercero, font=("time new roman", 15), width=7, justify="right" ).grid(row=12, column=1)
control2=Label(frame, text="Resto", font=("time new roman", 15)).grid(row=12, column=3)
entry_control2=Entry(frame, textvariable=cuarto, font=("time new roman", 15), width=7, justify="right" ).grid(row=12, column=4, padx=6, pady=6,  sticky="e")




respuesta=Label(frame, font=("time new roman", 20))
respuesta.grid(row=13, column=0, columnspan=4)

def control():
	a=primer.get()
	b=segundo.get()
	r=a/b
	if tercero.get()==a//b and cuarto.get() ==a%b:
		respuesta.config(text="Muy Bien!!!! Ambas respuesta son correctas", fg="green")
		
		
	elif tercero.get() ==a//b and cuarto.get() !=a%b:
		respuesta.config(text="El cociente es correcto....Debés revisar el resto", fg="yellow")
		
	elif tercero.get() !=a//b and cuarto.get() ==a%b:
		respuesta.config(text="El resto es correcto....Debés revisar el cociente", fg="yellow")
		
	else:
		respuesta.config(text="Ambos valores son incorrectos....Intentalo de nuevo", fg="Red")
		
		

boton_control=Button(frame, text="Controlar", command=control,font=("time new roman", 13), width=15).grid(row=2, column=4, columnspan=2)



dato1=IntVar()
dato2=IntVar()
dato3=IntVar()
dato4=IntVar()
dato5=IntVar()
dato6=IntVar()
dato7=IntVar()
dato8=IntVar()
dato9=IntVar()
dato10=IntVar()

class Enchufar:
	def __init__(self,ubicacion,texto,r,c):
		self.ubicacion=ubicacion
		self.texto=texto
		self.r=r
		self.c=c
		label=Label(self.ubicacion, text=self.texto)
		label.grid(row=self.r, column=self.c)
		label.config(font=("time new roman", 15), padx=4, pady=4)

class Resultado:
	def __init__(self, posicion, variable, r,c):
		self.posicion=posicion
		self.variable=variable
		self.r=r
		self.c=c
		entry=Entry(self.posicion, textvariable=self.variable, font=('time new roman', 12), justify="right", width=7)
		entry.grid(row=self.r, column=self.c)
		entry.config(state="disable")

	


tabla=Enchufar(frame, "x 1 =", 2, 0)
tabla=Enchufar(frame, "x 2 =", 3, 0)
tabla=Enchufar(frame, "x 3 =", 4, 0)
tabla=Enchufar(frame, "x 4 =", 5, 0)
tabla=Enchufar(frame, "x 5 =", 6, 0)
tabla=Enchufar(frame, "x 6 =", 7, 0)
tabla=Enchufar(frame, "x 7 =", 8, 0)
tabla=Enchufar(frame, "x 8 =", 9, 0)
tabla=Enchufar(frame, "x 9 =", 10, 0)
tabla=Enchufar(frame, "x 10 =", 11, 0)


casilla=Resultado(frame, dato1, 2,1)
casilla=Resultado(frame, dato2, 3,1)
casilla=Resultado(frame, dato3, 4,1)
casilla=Resultado(frame, dato4, 5,1)
casilla=Resultado(frame, dato5, 6,1)
casilla=Resultado(frame, dato6, 7,1)
casilla=Resultado(frame, dato7, 8,1)
casilla=Resultado(frame, dato8, 9,1)
casilla=Resultado(frame, dato9, 10,1)
casilla=Resultado(frame, dato10,11,1)



#tabla_lista=[]
def tabla():
	tabla_lista=[]

	for a in range (11):
		r=a*segundo.get()
		tabla_lista.append(r)
	
	for a in tabla_lista:
		
		dato1.set(tabla_lista[1])
		dato2.set(tabla_lista[2])
		dato3.set(tabla_lista[3])
		dato4.set(tabla_lista[4])
		dato5.set(tabla_lista[5])
		dato6.set(tabla_lista[6])
		dato7.set(tabla_lista[7])
		dato8.set(tabla_lista[8])
		dato9.set(tabla_lista[9])
		dato10.set(tabla_lista[10])


boton_tabla=Button(frame, text="Generar tabla", command=tabla, font=("time new roman", 13), width=15).grid(row=1, column=4, columnspan=2)


def borrar ():
	primer.set(0)
	segundo.set(0)
	tercero.set(0)
	cuarto.set(0)
	dato1.set(0)
	dato2.set(0)
	dato3.set(0)
	dato4.set(0)
	dato5.set(0)
	dato6.set(0)
	dato7.set(0)
	dato8.set(0)
	dato9.set(0)
	dato10.set(0)
	respuesta.config(text="")
	

iniciar=Button(frame, text="Borrar", command=borrar, font=("time new roman", 13), width=15).grid(row=3, column=4, columnspan=2 )
	



root.mainloop()