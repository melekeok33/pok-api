#<==============Documentación interna===============>
#Autor: Manuel Lima
#Fecha de creación: 21 noviembre de  2025
#Procesos pendientes: N/A

from tkinter import Tk, Entry, Label, Text, Button #ventana, objetos
import requests #API
from PIL import Image, ImageTk #imagen
from io import BytesIO #apoyo

class pokeapi(Tk):
    def __init__(self):
        super().__init__() #preguntar a richi

        self.title("Pokéapi"); self.config(bg="skyblue") #config de ventana
        self.url="https://pokeapi.co/api/v2/pokemon/" #url de la API

        #objetos
        Label(self, text="¿Qué pokémon buscas?").pack()
        self.p=Entry(self); self.p.pack()
        Button(self, text="Buscar pokémon", command=self.buscar).pack()
        self.rp=Label(self, text="");self.rp.pack()

        Label(self, text="¿Qué propiedad buscas?").pack()
        self.h=Entry(self); self.h.pack()
        Button(self, text="Buscar propiedad", command=self.propiedad).pack()
        self.rh=Text(self, width=40, height=20);self.rh.pack()



    def buscar(self):
        p=self.p.get()
        if not p:
            return False #validación de que p no esté vacío
        
        try:
            respuesta=requests.get(self.url+p) #encontrar el pokémon en la web
            if respuesta.status_code!=200: #maneja los errores HTTP
                self.rp['text']=f"{respuesta.status_code} \n :("
            self.data=respuesta.json() #pasa al formato json
            self.rp['text']=f"Pokemon disponible"
            return self.data
        except:
            self.rp['text']="Pokemon no disponible"
            return 
            
    def propiedad(self):
        self.rh.delete(1.0, END) #comienza vaciando el objeto texto
        acu="" #acumulador para algunos atributos
        atrib=["height", "weight", "base"] #vector de atributos
        clave = self.h.get() #clave 

        if not clave:
            self.rp['text']="No se proporcionó información"
            return
        
        RUTAS = {"abilities": "ability","types": "type", "moves": "move"} #algunas rutas para encontrar información del pokemon
        try:
            lista = self.data[clave]#indica en donde posicionarse

            ruta = RUTAS.get(clave)#nos da la clave para encontrarlo en el texto

            #atributos
            height=self.data["height"]
            weight = self.data["weight"]
            base = self.data["base_experience"]

            for i in range(len(atrib)): #recorrer el vector y en cada iteración al cambiar de string, imprime el atributo correspondiente
                #traté de usar match case, pero no me salió
                '''match atrib[i]:
                    case 0:
                        print (height)
                        self.rh.insert("end", f"---HEIGHT---\n{height}\n")
                    case 1:
                        self.rh.insert("end", f"---WEIGHT---\n{weight}\n")
                    case 2:
                        self.rh.insert("end", f"---BASE---\n{base}\n")'''
                
                if atrib[i]=="height":
                    self.rh.insert(1.0, f"---HEIGHT---\n{height}\n")
                elif atrib[i]=="weight":
                    self.rh.insert(1.0, f"---WEIGHT---\n{weight}\n")
                elif atrib[i]=="base":
                    self.rh.insert(1.0, f"---BASE---\n{base}\n")

            #en cada iteración se asigna a acu el valor requerido
            for item in lista:
                    acu+=(item[ruta]["name"])
                    acu+="\n"
            self.rh.insert(1.0, acu)

            self.mostrar_sprite()
        except:
            self.rp["text"] = "Propiedad no disponible"

    def mostrar_sprite(self): 
        try:
            url_img = self.data["sprites"]["front_default"] 
            if not url_img:
                self.rp["text"] = "Sprite no disponible"
                return

            # descargar imagen
            img_bytes = requests.get(url_img).content
            img = Image.open(BytesIO(img_bytes))

            # opcional: redimensionar
            img = img.resize((200, 200))

            # convertir a formato Tkinter
            self.sprite = ImageTk.PhotoImage(img)

            # crear o actualizar label
            if hasattr(self, "sprite_label"):
                self.sprite_label.config(image=self.sprite)
            else:
                self.sprite_label = Label(self, image=self.sprite)
                self.sprite_label.pack()

            self.rp["text"] = "Sprite cargado"
        except:
            self.rp["text"] = "Error al cargar sprite"


pokeapi().mainloop()
