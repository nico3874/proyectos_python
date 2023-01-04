import random

def tablas ():
	a=random.randrange (10)
	b=random.randrange (10) 
	r=a*b
	
	return (print(r))




puntos=0
chances=0

def puntuacion ():
	
	if chances ==10:
			print("\n>>>>Has obtenido {} puntos".format(puntos))
	if puntos >= 7:
			print ("\n>>>>Muy bien, realmente conoces las tablas!!!")
	else:
			print ("\n>>>>Debes practicar un poco más, no te desanimes; si continuas lo conseguirás")
			



nombre= input("¿Cuál es tu nombre?: ")

print ("Hola {}, sabes cuánto es {} x {}". format(nombre,a,b))
while True:
	
	
	try:
		
		
		frases1=["Ahora intenta con esta {} x {}".format(a,b), "A ver cómo te va con esta {} x {}".format (a,b), "Muy bien!!...Continuemos {} x {}".format(a,b)]
		respuesta= int(input())
		if respuesta ==a*b:
			puntos+=1
			chances+=1
			print("Correcto!!! Vas muy bien")
			a=random.randrange (10)
			b=random.randrange (10) 
			
			print (random.choice(frases1))
			
			print ("Puntaje {}".format(puntos))

			
				

		else:
			chances+=1
			print ("Intentalo de nuevo")
			
			print ("Puntaje {}".format(puntos))
			
			

	except ValueError:
		print ("Solo puedes introducir números enteros")


	if chances ==10:
		puntuacion()
		print("\n Adios...Sigue estudiando!!!>>>")
		break





		









