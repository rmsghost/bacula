import time
from flask import Flask,  jsonify, request, render_template
import bd
from traccing import tracing, opentracing_tracer
import opentracing
from flask.wrappers import Response
import os
import requests
import logging

app = Flask(__name__)


#Inciando as rotas
@app.route("/", methods=['GET'])
@tracing.trace()
def index():
    span = tracing.get_span()
    name = request.args.get('name')
    return jsonify({
        'httpCode': 200,
        'body': 'Welcome to API',
        'arg': name
    })


@app.route("/login", methods=['GET'])
@tracing.trace()
def login():
    print(f'Login sendo efetuado')

    return render_template('./html/login.html')


#Lista todos os pokemon
@app.route("/pokemon", methods=['GET'])
@tracing.trace()
def consultaPokemon():
    parent_span = tracing.get_span()

    with opentracing.tracer.start_span('Call BD', child_of=parent_span) as span:
        resultado = bd.allPokemon()
        span.set_tag('Chamada', resultado[0])
    
    return jsonify(resultado[1]) 



#Lista um pokemon específico pelo ID da pokedex
@app.route("/consulta/<id>", methods=['GET'])
@tracing.trace()
def exibe(id):
    span = tracing.get_span()
    resultado = bd.consultPokemon(id)
    return jsonify(resultado) 

@app.route("/api", methods=['GET'])
@tracing.trace()
def api():
    span = tracing.get_span()
    text_carrier = {}
    opentracing_tracer.inject(span, opentracing.Format.TEXT_MAP, text_carrier)
    response = requests.get('https://rickandmortyapi.com/api', headers=text_carrier)
    span.log_kv({'event': 'Consultando API externa'})
    data = response.json()
    logging.warning('HAHAHA HIHIHI')
    
    return jsonify(data)



#Inicializando a aplicação
app.run(host='0.0.0.0',port='8689',debug=False)

