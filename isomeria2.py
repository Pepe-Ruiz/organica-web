from flask import Flask, request, render_template_string, Blueprint,redirect
from rdkit import Chem
from rdkit.Chem import Draw
import base64
from io import BytesIO
import json

app = Flask(__name__)
pagina_isomeria = Blueprint('pagina_isomeria', __name__)
# Cargar archivo JSON con todos los tipos de isomería
with open("isomeria2.json", "r", encoding="utf-8") as f:
    DATOS_ISOMERIA = json.load(f)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Visualizar Isomería Orgánica</title>
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
    <h1 style="text-align:center;">Formulación Orgánica: Isomería</h1><br>
    <h2>El término isómeros se utiliza en química orgánica para designar dos compuestos que tienen la misma fórmula molecular pero que presentan distintas propiedades químicas.</h2>
    <div class="container">
        <div class="formulario">
            <form method="POST">
                {% for tipo in ['funcional', 'posicion', 'cadena', 'cis_trans', 'optica'] %}
                    <label><strong>Isómeros de {{ tipo.replace('_', '-') }}:</strong></label><br>
                    <label>
                        <input type="checkbox" id="{{ tipo }}" name="{{ tipo }}_activa" onclick="toggleLista('{{ tipo }}')"> Mostrar
                    </label>
                    <div id="lista_{{ tipo }}" style="display:none; margin-top:10px;">
                        <label for="compuesto_{{ tipo }}">Selecciona un compuesto:</label>
                        <select name="compuesto_{{ tipo }}">
                            {% for clave, datos in datos_isomeria[tipo].items() %}
                                <option value="{{ clave }}">{{ datos['nombre'] }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <br>
                {% endfor %}
                <button type="submit">Ver resultado</button>
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

#@app.route("/", methods=["GET", "POST"])
@pagina_isomeria.route("/hola6", methods=["GET", "POST"])
def index():
    resultados = []
    error = None

    if request.method == "POST":
        for tipo in ['funcional', 'posicion', 'cadena', 'cis_trans', 'optica']:
            activa = request.form.get(f"{tipo}_activa")
            seleccionado = request.form.get(f"compuesto_{tipo}")

            if activa and seleccionado in DATOS_ISOMERIA[tipo]:
                info = DATOS_ISOMERIA[tipo][seleccionado]
                smiles = [i["smiles"] for i in info["isomeros"]]
                nombres = [i["nombre"] for i in info["isomeros"]]
                mols = [Chem.MolFromSmiles(s) for s in smiles]

                img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(250, 250), legends=nombres)
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                img_html = f'<img src="data:image/png;base64,{img_base64}"/>'

                resultados.append({
                    "titulo": f"Isomería de {tipo.replace('_', '-')} - {info['nombre']}",
                    "imagen": img_html
                })

        if not resultados:
            error = "Debes seleccionar al menos una isomería y un compuesto válido."

    return render_template_string(
        HTML_TEMPLATE,
        datos_isomeria=DATOS_ISOMERIA,
        resultados=resultados,
        error=error
    )

app.register_blueprint(pagina_isomeria)


if __name__ == "__main__":
    app.run(debug=True)
