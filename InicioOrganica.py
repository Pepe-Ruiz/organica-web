from flask import Flask, request, render_template_string,render_template

from organica3 import pagina_organica
from isomeria2 import pagina_isomeria
from reaccionorganica1 import pagina_reacciones



app = Flask(__name__)

app.register_blueprint(pagina_organica)
app.register_blueprint(pagina_isomeria)
app.register_blueprint(pagina_reacciones)


HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Orgánica</title>
  <link href="muestrasdeestilos.css" rel="stylesheet" type="text/css">
  <style>
    body { margin: 0; height: 100%; overflow: hidden; }
    div#Superior {
      position: fixed; top: 0; left: 0;
      width: 100%; height: 40px;
      background-color: #BBC7F7;
      z-index: 100;
    }
    div#Izquierda {
      position: fixed; top: 40px; left: 0;
      width: 25%; bottom: 0;
      background-color: #3399FF;
      overflow: auto;
      padding: 10px;
    }
    div#Derecha {
      position: fixed; top: 40px; left: 25%;
      width: 75%; bottom: 0;
      background-color: #D9F2F2;
      overflow: auto;
      padding: 10px;
    }
  </style>
</head>

<body>
  <div id="Superior">
    <marquee direction="Right" scrollamount="4">Orgánica</marquee>
    <div style="text-align: center;">
      <span style="font-family: arial; font-style: italic; color: #000066; font-size: large;">
        Formulación, isomería, reacciones.
      </span>
    </div>
  </div>

  <div id="Izquierda">
  <h2><big>Tema de Orgánica:</big></h2>
  <p><font color="#ff0000">A.- INTRODUCCIÓN</font></p>

  <p><big><a href="/hola5" target="_blank">Formulación.</a></big></p>
  <p><a href="/hola6" target="_blank">Isomería.</a></p>
  <p><a href="/hola7" target="_blank">Reacciones de orgánica.</a></p>

  <p>Autor: José Ruiz Castillo.</p>

  <!-- Contador de visitas en la barra izquierda -->
  <div style="text-align: center; margin-top: 20px;">
    <a href="https://www.freecounterstat.com" title="contador de visitas gratuito">
      <img src="https://counter7.stat.ovh/private/freecounterstat.php?c=j3zccwnewdefsn9dads6jap9xcx388a1" border="0" title="contador de visitas gratuito" alt="contador de visitas gratuito">
    </a>
  </div>
</div>


  <div id="Derecha">
    <h3>Los compuestos orgánicos se nombran y formulan con las siguientes reglas de la IUPAC:</h3>
    <p>• La cadena principal es la más larga que contiene al grupo funcional más importante.</p>
    <p>• El sentido de la numeración será aquel que otorgue el localizador más bajo a dicho grupo funcional.</p>
    <p>• Las cadenas laterales se nombran antes que la cadena principal, precedidas de su correspondiente número de localizador y con la terminación <strong>“il”</strong> o <strong>“ilo”</strong>.</p>
    <p>• Se indicarán los sustituyentes por orden alfabético, incluyendo la terminación característica del grupo funcional más importante a continuación del prefijo del número de carbonos.</p>
    <p>• Cuando haya más de un grupo funcional, el sufijo de la cadena principal corresponde al grupo funcional principal, según este orden:</p>
    <p>Ácidos > ésteres > amidas = sales > nitrilos > aldehídos > cetonas > alcoholes > aminas > éteres > insaturaciones (> ≡) > hidrocarburos saturados.</p>

    <p><strong>met-</strong> Nº de C: uno; <strong>et-</strong> Nº de C: dos; <strong>prop-</strong> Nº de C: tres; <strong>but-</strong> Nº de C: cuatro; <strong>pent-</strong> Nº de C: cinco…</p>

    <p><strong>Alcanos:</strong> [prefijo terminado en <strong>-ano</strong>]</p>
    <p><strong>Alquenos:</strong> [prefijo-localizador(=) terminado en <strong>-eno</strong>]</p>
    <p><strong>Alquinos:</strong> [prefijo-localizador(triple) terminado en <strong>-ino</strong>]</p>
    <p><strong>Alcohol:</strong> nombre-localizador(—OH) terminado en <strong>-ol</strong></p>
    <p><strong>Éteres:</strong> prefijo(n°CP)<strong>oxi</strong>prefijo(n°CP)<strong>ano</strong></p>
    <p><strong>Aldehídos:</strong> nombre(HC)<strong>-al</strong></p>
    <p><strong>Cetonas:</strong> nombre-localizador(—CO—)<strong>-ona</strong></p>
    <p><strong>Ácidos carboxílicos:</strong> ácido nombre(HC)<strong>-oico</strong></p>
    <p><strong>Ésteres:</strong> prefijo(n°C)<strong>-ato</strong> de prefijo(n°C)<strong>-ilo</strong></p>
    <p><strong>Aminas:</strong> nombre-localizador(—NH₂)<strong>-amina</strong> o prefijo(n°CR)<strong>-ilamina</strong></p>
    <p><strong>Amidas:</strong> nombre(HC)<strong>-amida</strong>; N-prefijo(n°CR)il- N-prefijo(n°CR)il-nombre<strong>-amida</strong></p>
    <p><strong>Nitrilos:</strong> nombre(HC)<strong>-nitrilo</strong></p>
    <p><strong>Nitrocompuestos:</strong> localizador(NO₂)-prefijo-nombre(HC)</p>
  </div>
</body>
</html>

"""
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template_string(HTML)

app.route("/hola5", methods=["GET"])
def hola5():
    return "<h2>Formulación Orgánica</h2>"

@app.route("/hola6", methods=["GET"])
def hola6():
    return "<h2>Isomería</h2>"

@app.route("/hola7", methods=["GET"])
def hola7():
    return "<h2>Reacciones Orgánicas</h2>"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)



