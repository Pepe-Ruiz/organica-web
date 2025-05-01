from flask import Flask, request, render_template_string, Blueprint,redirect
from rdkit import Chem
from rdkit.Chem import Draw
import base64
from io import BytesIO
import json
from rdkit.Chem import rdMolDescriptors
import re
app = Flask(__name__)
pagina_organica = Blueprint('pagina_organica', __name__)
# Cargar las reacciones del archivo JSON
with open("compuestos3.json", "r", encoding="utf-8") as f:
    DATOS_REACCION = json.load(f)

# Función para convertir SMILES a imagen
def mol_to_img(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return "<p>Error en la molécula</p>"
    img = Draw.MolToImage(mol, size=(300,300), kekulize=True, wedgeBonds=True)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return f'<img src="data:image/png;base64,{img_str}" style="width:150px;">'

# Plantilla HTML con Jinja2
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Reacciones de Orgánica</title>
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
                {% for tipo in ['alcanos', 'alquenos', 'alquinos', 'alcoholes', 'aldehidos', 'eteres', 'cetonas','acidos','sales','esteres', 'aminas','amidas', 'nitrilos', 'nitros'] %}
                    <label><strong>compuesto: {{ tipo.replace('_', '-') }}:</strong></label><br>
                    <label>
                        <input type="checkbox" id="{{ tipo }}" name="{{ tipo }}_activa" onclick="toggleLista('{{ tipo }}')"> Mostrar
                    </label>
                    <div id="lista_{{ tipo }}" style="display:none; margin-top:10px;">
                        <label for="compuesto_{{ tipo }}">Selecciona una función:</label>
                        <select name="compuesto_{{ tipo }}">
                            {% for compuesto in datos_isomeria.get(tipo, []) %}
                                <option value="{{ compuesto['nombre'] }}">{{ compuesto['nombre'] }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <br>
                {% endfor %}
                <button type="submit">Ver resultado</button><br>
            </form>
        </div>
        <div class="resultados">
            {% if resultados %}
                <h2>Resultados:</h2>
                {% for bloque in resultados %}
                    <div style="margin-bottom:20px;">
                        <h3>{{ bloque['titulo'] }}</h3>
                        {{ bloque['imagen']|safe }}
                        <p><strong>Nombre:</strong> {{ bloque['nombre'] }}</p>
                        <p><strong>Fórmula molecular:</strong> {{ bloque['formula'] }}</p>
                    </div>
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





def obtener_formula_molecular(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        return rdMolDescriptors.CalcMolFormula(mol)
    else:
        return "Fórmula no disponible"


def cargar_compuestos():
    with open('compuestos3.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['compuestos3']


@pagina_organica.route("/hola5", methods=["GET", "POST"])
def index():
    resultados = []
    error = None

    if request.method == "POST":
        for tipo in DATOS_REACCION.keys():
            if request.form.get(f"{tipo}_activa"):
                compuesto = request.form.get(f"compuesto_{tipo}")
                if compuesto:
                    compuesto_info = next((c for c in DATOS_REACCION[tipo] if c["nombre"] == compuesto), None)
                    if compuesto_info:
                        smiles = compuesto_info["smiles"]
                        bloque = {"titulo": f"{tipo.capitalize()} - {compuesto_info['nombre']}", "imagen": ""}
                        bloque["imagen"] = mol_to_img(smiles)
                        bloque["formula"]= obtener_formula_molecular(smiles)
                        resultados.append(bloque)
                    else:
                        error = "No se encontró la fórmula."
    return render_template_string(HTML_TEMPLATE, resultados=resultados, error=error, datos_isomeria=DATOS_REACCION)


app.register_blueprint(pagina_organica)




if __name__ == "__main__":
    app.run(debug=True)
