import tkinter as tk
from tkinter import filedialog, messagebox

# Funciones para análisis léxico y sintáctico

def analizar_codigo(codigo):
    # Definir palabras clave y tokens
    palabras_clave = {
        'CrearBD': 'CREATE_DB',
        'EliminarBD': 'DELETE_DB',
        'CrearColeccion': 'CREATE_COLLECTION',
        'EliminarColeccion': 'DELETE_COLLECTION',
        'InsertarUnico': 'INSERT_ONE',
        'ActualizarUnico': 'UPDATE_ONE',
        'EliminarUnico': 'DELETE_ONE',
        'BuscarTodo': 'FIND_ALL',
        'BuscarUnico': 'FIND_ONE'
    }
    
    tokens = []
    errores = []

    

    # Dividir el código en líneas
    lineas = codigo.split('\n')

    # Analizar cada línea
    for numero_linea, linea in enumerate(lineas, start=1):
        # Ignorar líneas en blanco o comentarios
        if not linea.strip() or linea.strip().startswith('//') or linea.strip().startswith('/*'):
            continue
        
        # Dividir la línea en palabras
        palabras = linea.split()

        # Analizar la primera palabra para identificar comandos
        comando = palabras[0]

        if comando in palabras_clave:
            token = palabras_clave[comando]
            if token == 'CREATE_DB' or token == 'DELETE_DB':
                # Verificar si hay argumentos adicionales
                if len(palabras) != 2:
                    errores.append((numero_linea, 'Error sintáctico: Falta el nombre de la base de datos.'))
                else:
                    tokens.append((token, palabras[1]))
            elif token == 'CREATE_COLLECTION' or token == 'DELETE_COLLECTION':
                if len(palabras) != 2:
                    errores.append((numero_linea, 'Error sintáctico: Falta el nombre de la colección.'))
                else:
                    tokens.append((token, palabras[1]))
            else:
                tokens.append((token,))
        else:
            errores.append((numero_linea, 'Error léxico: Comando desconocido.'))
            

    return tokens, errores


def generar_sentencias():
    global tokens, sentencias_mongodb
    
    if 'tokens' in globals():
        sentencias_mongodb = []
        
        for token in tokens:
            if token[0] == 'CREATE_DB':
                sentencias_mongodb.append(f"use('{token[1]}');")
            elif token[0] == 'DELETE_DB':
                sentencias_mongodb.append('db.dropDatabase();')
            elif token[0] == 'CREATE_COLLECTION':
                sentencias_mongodb.append(f"db.createCollection('{token[1]}');")
            elif token[0] == 'DELETE_COLLECTION':
                sentencias_mongodb.append(f"db.{token[1]}.drop();")
            elif token[0] == 'INSERT_ONE':
                sentencias_mongodb.append(f"db.{token[1]}.insertOne(ARCHIVOJSON);")
            elif token[0] == 'UPDATE_ONE':
                sentencias_mongodb.append(f"db.{token[1]}.updateOne(ARCHIVOJSON);")
            elif token[0] == 'DELETE_ONE':
                sentencias_mongodb.append(f"db.{token[1]}.deleteOne(ARCHIVOJSON);")
            elif token[0] == 'FIND_ALL':
                sentencias_mongodb.append(f"db.{token[1]}.find();")
            elif token[0] == 'FIND_ONE':
                sentencias_mongodb.append(f"db.{token[1]}.findOne();")
        
        messagebox.showinfo("Información", "Sentencias MongoDB generadas correctamente.")
    else:
        messagebox.showerror("Error", "No se ha analizado ningún código.")


# Funciones para la interfaz de usuario

def cargar_archivo():
    ruta_archivo = filedialog.askopenfilename()
    if ruta_archivo:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
        entrada_texto.delete(1.0, tk.END)
        entrada_texto.insert(1.0, contenido)
        messagebox.showinfo("Información", "Archivo cargado correctamente.")


def guardar_archivo():
    contenido = entrada_texto.get(1.0, tk.END)
    if contenido:
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".txt")
        with open(ruta_guardado, 'w') as archivo:
            archivo.write(contenido)
        messagebox.showinfo("Información", f"El archivo se ha guardado correctamente en '{ruta_guardado}'.")
    else:
        messagebox.showerror("Error", "No hay contenido para guardar.")


def mostrar_errores():
    global errores
    if 'errores' in globals() and errores:
        messagebox.showinfo("Errores", "\n".join([f"Línea {linea}: {descripcion}" for linea, descripcion in errores]))
    else:
        messagebox.showinfo("Errores", "No hay errores que mostrar.")



def mostrar_sentencias():
    if 'sentencias_mongodb' in globals():
        messagebox.showinfo("Sentencias MongoDB", "\n".join(sentencias_mongodb))
    else:
        messagebox.showinfo("Sentencias MongoDB", "No hay sentencias MongoDB que mostrar.")


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Interfaz de Usuario")

# Crear área de texto para entrada de código
entrada_texto = tk.Text(ventana, height=20, width=50)
entrada_texto.pack()

# Crear botones para las opciones
tk.Button(ventana, text="Cargar Archivo", command=cargar_archivo).pack(fill=tk.X)
tk.Button(ventana, text="Analizar Código", command=analizar_codigo).pack(fill=tk.X)
tk.Button(ventana, text="Mostrar Errores", command=mostrar_errores).pack(fill=tk.X)
tk.Button(ventana, text="Generar Sentencias MongoDB", command=generar_sentencias).pack(fill=tk.X)
tk.Button(ventana, text="Mostrar Sentencias MongoDB", command=mostrar_sentencias).pack(fill=tk.X)
tk.Button(ventana, text="Guardar Archivo", command=guardar_archivo).pack(fill=tk.X)
tk.Button(ventana, text="Salir", command=ventana.quit).pack(fill=tk.X)

# Ejecutar bucle de eventos
ventana.mainloop()
