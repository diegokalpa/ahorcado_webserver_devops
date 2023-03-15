from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)
@app.route('/')  # se crea inicialmente esta linea para conectar con index.html
def home():
    return render_template('index.html')

@app.route('/palabra_aleatoria', methods=['POST']) 
def palabra_aleatoria():

    palabras = []
  
    with open("archivos/data.txt", "r",encoding = "utf-8") as f:
    # with open("venv/archivos/data.txt", "r",encoding = "utf-8") as f:
        palabras = [c for c in f]
    global aleatoria   # Esta global me permite usar la variable en cualquier parte
    aleatoria = random.choice(palabras)
    aleatoria = aleatoria.rstrip('\n,')
    # aleatoria = "sol"
    global longitud_aleatoria
    longitud_aleatoria = len(aleatoria)
    # print(longitud_aleatoria)
    global tablero
    tablero = longitud_aleatoria*["-"]
    print("tablero es:",tablero)
    global letras_incorrectas
    letras_incorrectas = []
    global intentos
    try:
        # intentos = int(input("Escriba el numero de intentos para jugar: "))
        intentos = int(request.form.get("intentos"))
    except ValueError:  
        print("Debes ingresar un numero")
        intentos = int(request.form.get("intentos"))
        # intentos = int(input("Escriba el numero de intentos para jugar: "))
    return render_template('index.html', intentos = intentos, tablero = tablero, longitud_aleatoria = longitud_aleatoria), aleatoria#,[],tablero
#return aleatoria, tablero, intentos, [], 


@app.route('/pedir_letra', methods=['POST'])
def pedir_letra():
    global letra
    global tablero
    palabra_completa = " ".join(tablero)

    while palabra_completa != aleatoria:
        print("palabra completa: ", palabra_completa)
        # letra = input("Ingrese una letra:")
        letra = (request.form.get("letra"))
        if letra.isalpha() == False:
            print("Debes ingresar una letra, no otro caracter")
            letra = str(input("Ingrese una letra:"))
        else:
            os.system ("clear")
        procesar_letra(letra,aleatoria)
        actualizar_tablero(aleatoria, tablero, letra,letras_incorrectas)
        print("Tu Palabra", tablero)
        print("Tus letras falladas \n", letras_incorrectas)
        palabra_completa = "".join(tablero)
        return render_template('index.html', tablero = tablero, letra = letra, palabra_completa = palabra_completa, letras_incorrectas=letras_incorrectas, intentos=intentos)
        
    fin_juego()
    return letra


@app.route('/procesar_letra', methods=['POST'])
def procesar_letra(letra,aleatoria):
    if letra in aleatoria:
        print("la letra existe")
        print("Te quedan, ", intentos, "intentos")
        actualizar_tablero(aleatoria, tablero, letra, letras_incorrectas)
        return render_template('index.html', intentos = intentos, tablero = tablero)
    else:
        print('¡Oh! Has fallado.')
        numero_intentos()
        actualizar_tablero(aleatoria, tablero,letra, letras_incorrectas)
        letras_incorrectas.append(letra)
        return render_template('index.html', intentos = intentos, tablero = tablero, letras_incorrectas = letras_incorrectas)

        
def actualizar_tablero(aleatoria, tablero, letra,letras_incorrectas): 
        for indice, letra_palabra in enumerate(aleatoria):
            if letra == letra_palabra:
                tablero[indice] = letra
                return render_template('index.html', tablero = tablero)

@app.route('/numero_intentos', methods=['POST'])   
def numero_intentos():
    global intentos
    intentos = intentos - 1
    if intentos == 0:
        print("PERDISTE, EL JUEGO HA TERMINADO")
        perdiste = 'PERDISTE, EL JUEGO HA TERMINADO'
        print(tablero)
        print("La palabra era:", aleatoria )
        # exit()
        return render_template('index.html', perdiste = perdiste, aleatoria=aleatoria)
    else:
        print("Te quedan, ", intentos, "intentos")

@app.route('/fin_juego', methods=['POST'])       
def fin_juego():
    print("FELICIDADES GANASTE EL JUEGO")
    ganaste = "GANASTE, EL JUEGO HA TERMINADO"
    print("La palabra era:", aleatoria )
    return render_template('index.html', ganaste = "GANASTE  EL JUEGO!!!", aleatoria=aleatoria)
    exit()


def run():
    palabra_aleatoria()
    pedir_letra()


if __name__ == '__main__':
    app.run(port = 5100, debug=True)
    # run()