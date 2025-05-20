
from flasgger import Swagger
from flask import Flask, request, jsonify
from application.libs.train import train_model
from application.libs.predict import predict_model
from flask import Flask, render_template, request


app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.yaml')

@app.route("/", methods=['GET'])
def index():
    return {
        "mensagem": "API de Previsão está rodando! Use /predict para fazer previsões."}


@app.route("/predict", methods=['POST'])
def predict():
    print("/predict - called")
    data = request.get_json()
    result = predict_model(data)

    return jsonify(result)



@app.route("/predict-painel", methods=['GET'])
def predict_painel_get():
    return render_template("formulario.html")


@app.route("/predict-painel", methods=['POST'])
def predict_painel_post():
    try:
        data = request.form.to_dict()
        result = predict_model(data)  # Certifique-se de que isso retorna um dict, str ou algo serializável
    except Exception as ex:
        result = {"error": str(ex)}

    return jsonify(result)



@app.route("/train", methods=['GET'])
def train():

    result = train_model()
    return jsonify(result)


if __name__ == "__main__": 
    app.run(debug=True, port=8000)