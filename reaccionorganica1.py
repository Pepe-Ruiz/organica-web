from flask import Flask, request, render_template_string, Blueprint,redirect
from rdkit import Chem
from rdkit.Chem import Draw
import base64
from io import BytesIO
import json

app = Flask(__name__)
pagina_reacciones= Blueprint('pagina_reacciones', __name__)
# Cargar las reacciones del archivo JSON
with open("reaccionorganica1.json", "r", encoding="utf-8") as f:
    DATOS_REACCION = json.load(f)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Reacciones de  Orgánica</title>
    <style>
        body { margin: 0; background-color: #D9F2F2; font-family: Arial; }
        .container { display: flex; justify-content: space-between; padding: 20px 40px; }
        .formulario, .resultados {
            width: 48%; background: white; padding: 20px;
            border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
    </style>
    <script>
        function toggleLista(tipo) {
            var div = document.getElementById("lista_" + tipo);
            div.style.display = div.style.display === "block" ? "none" : "block";
        }
    </script>
</head>
<body>
    <h1 style="text-align:center;">Reacciones de Orgánica</h1><br>
    
    <div class="container">
        <div class="formulario">
            
            <form method="POST">
                {% for tipo in ['sustitucion', 'adicion', 'eliminacion', 'adicion_eliminacion', 'oxidacion'] %}
                    <label><strong>Reacción de {{ tipo.replace('_', '-') }}:</strong></label><br>
                    <label>
                        <input type="checkbox" id="{{ tipo }}" name="{{ tipo }}_activa" onclick="toggleLista('{{ tipo }}')"> Mostrar
                    </label>
                    <div id="lista_{{ tipo }}" style="display:none; margin-top:10px;">
                        <label for="reaccion_{{ tipo }}">Selecciona una reacción:</label>
                        
                        <select name="reaccion_{{ tipo }}">
                            {% for clave, datos in datos_isomeria.get(tipo, {}).items() %}
                                <option value="{{ clave }}">{{ clave }}</option>
                            {% endfor %}
                        </select>



                        
                    </div>
                    <br>
                {% endfor %}
                <button type="submit">Ver resultado</button><br>
                <h><FONT color="#0000FF"><U> Alquenos y alquinos</U>: enlaces poco polares. Adición electrófila AE, se produce en la polimerización
                    por adición. <B>Regla de Markownikoff</B>, el fragmento negativo de la molécula que se adiciona se une
                    preferentemente al átomo de carbono del doble enlace que tiene menos átomos de hidrógeno. </FONT></h><br>
                <h><FONT color="#FF0000">El producto principal de la <U>eliminación</U> se obtiene después de aplicar la <B>regla de Saytzeff</b>, por
                    lo que se obtendrá el alqueno más sustituido.</FONT></h>
            </form>
        </div>
        <div class="resultados">
            {% if resultados %}
                <h2>Resultados:</h2>
                {% for bloque in resultados %}
                    <h3>{{ bloque['titulo'] }}</h3>
                    {{ bloque['imagen']|safe }}
                {% endfor %}
            {% elif error %}
                <h2 style="color:red;">Error:</h2>
                <p>{{ error }}</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""
def mol_to_img(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return "<p>Error en la molécula</p>"
    img = Draw.MolToImage(mol)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f'<img src="data:image/png;base64,{img_str}" style="width:150px;">'

#@app.route("/", methods=["GET", "POST"])

@pagina_reacciones.route("/hola7", methods=["GET", "POST"])
def index():
    resultados = []
    error = None

    if request.method == "POST":
        for tipo in DATOS_REACCION.keys():
            if request.form.get(f"{tipo}_activa"):
                reaccion_seleccionada = request.form.get(f"reaccion_{tipo}")
                if reaccion_seleccionada:
                    datos_reaccion = DATOS_REACCION[tipo].get(reaccion_seleccionada)
                    if datos_reaccion:
                        reactivos = datos_reaccion["reactivos"]
                        producto = datos_reaccion["producto"]

                        # Generar imágenes
                        bloque = {"titulo": f"{tipo.capitalize()} - {reaccion_seleccionada}", "imagen": ""}
                        for smi in reactivos:
                            bloque["imagen"] += mol_to_img(smi)
                            bloque["imagen"] += " + "
                        bloque["imagen"] = bloque["imagen"].rstrip(" + ")
                        bloque["imagen"] += " → "
                        bloque["imagen"] += mol_to_img(producto)

                        resultados.append(bloque)
                    else:
                        error = "No se encontró la reacción seleccionada."
    return render_template_string(HTML_TEMPLATE, resultados=resultados, error=error, datos_isomeria=DATOS_REACCION)

app.register_blueprint(pagina_reacciones)
if __name__ == "__main__":
    app.run(debug=True)
