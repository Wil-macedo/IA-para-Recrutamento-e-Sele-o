
from flask import Flask, request, jsonify
from application.libs.train import train_model
from application.libs.predict import predict_model


app = Flask(__name__)

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


@app.route("/predict-painel", methods=['POST'])
def predict_painel():

    try:
        data = request.get_json()
        result = predict_model(data)
    except Exception as ex:
        result = str(ex)
        
    return jsonify(result)


@app.route("/train", methods=['GET'])
def train():

    result = train_model()
    return jsonify(result)


if __name__ == "__main__": 
    app.run(debug=True, port=8000)