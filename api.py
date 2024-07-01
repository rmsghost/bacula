import time
from flask import Flask,  jsonify, request
import bd


app = Flask(__name__)


#Inciando as rotas
@app.route("/", methods=['GET'])
def index():
    name = request.args.get('name')
    return jsonify({
        'httpCode': 200,
        'body': 'Welcome to API',
        'arg': name
    })

#Lista todos os pokemon
@app.route("/pokemon", methods=['GET'])
def consultaPokemon():
    resultado = bd.allPokemon()

    return jsonify(resultado) 

#Lista um pokemon específico pelo ID da pokedex
@app.route("/consulta/<id>", methods=['GET'])
def exibe(id):

    resultado = bd.consultPokemon(id)
    return resultado



#Inicializando a aplicação
app.run(host='0.0.0.0',port='8689',debug=False)

