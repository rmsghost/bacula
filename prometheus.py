from flask import Flask, jsonify, request
from flask.wrappers import Response
from traccingX import tracing, opentracing_tracer
import opentracing
import requests
from prometheus_client import make_wsgi_app, Counter, Histogram, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time
import os
from flask_opentracing import FlaskTracer
import logging


app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
REQUEST_COUNT = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Application Request Latency',
    ['method', 'endpoint']
)
REQUEST_LATENCY_G = Gauge(
    'app_response_time',
    'App response Time',
    ['method','endpoint']
)
CALLS_EXTERNAL_API = Counter(
    'call_external_count',
    'Application external call',
    ['method','endpoint','request']
)



@app.route('/')
@tracing.trace()
def hello():
    span = tracing.get_span()
    start_time = time.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    response = jsonify(message='Hello, world!')
    REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    REQUEST_LATENCY_G.labels('GET','/').set(time.time() - start_time)
    return response

@app.route('/teste/<segundos>', methods=['GET'])
@tracing.trace()
def teste(segundos):
    span = tracing.get_span()
    start_time = time.time()
    REQUEST_COUNT.labels('GET', '/teste', 200).inc()
    time.sleep(int(segundos))
    REQUEST_LATENCY.labels('GET','/teste').observe(time.time() - start_time)
    REQUEST_LATENCY_G.labels('GET','/teste').set(time.time() - start_time)
    return {
        'msg':'Ola'        
    }

@app.route('/rick', methods=['GET'])
@tracing.trace()
def rick():

    span = tracing.get_span()
    text_carrier = {}
    opentracing_tracer.inject(span, opentracing.Format.TEXT_MAP, text_carrier)

    response = requests.get('https://rickandmortyapi.com/api', headers=text_carrier)
    REQUEST_COUNT.labels('GET', '/rick', 200).inc() 
    #response = requests.get('http://172.21.0.7:8689/pokemon')
    #response = requests.get('http://172.21.0.7:8689/')
    #print(response)
    span.log_kv({'event': 'Consultando API externa'})
    data = response.json()
    print(data)
    CALLS_EXTERNAL_API.labels('GET','/getapi','https://rickandmortyapi.com/api').inc()
    logging.warning('HAHAHA HIHIHI')
    return jsonify(data) 


@app.route('/getapi', methods=['GET'])
@tracing.trace()
def get_api():
    span = tracing.get_span()
    text_carrier = {}
    opentracing_tracer.inject(span, opentracing.Format.TEXT_MAP, text_carrier)
    response = requests.get('http://172.23.0.7:8689/api', headers=text_carrier)
    time.sleep(5)
    REQUEST_COUNT.labels('GET', '/getapi', 200).inc() 
    span.log_kv({'event': 'Consultando API amiga'})
    data = response.json()
    print(data)
    CALLS_EXTERNAL_API.labels('GET','/getapi','http://172.21.0.7:8689/api').inc()
    return jsonify(data) 

@app.route('/cocanan', methods=['GET'])
@tracing.trace()
def cocanan():
    print(f'teste')
    url = "https://rickandmortyapi.com/api"
    parent_span = tracing.get_span()
    
    with opentracing.tracer.start_span('Chamada API externa', child_of=parent_span) as span:
        span.set_tag('http_url',url)
        r = requests.get(url)
        span.set_tag("http.status_code", r.status_code)
    
    with opentracing.tracer.start_span('parse-json', child_of=parent_span) as span:
        json = r.json()
        span.set_tag('resultados', json)

    return jsonify(json)



# @app.route('/rick', methods=['GET'])
# @tracing.trace()
# def get_api():
#     span = tracing.get_span()

#     REQUEST_COUNT.labels('GET', '/getapi', 200).inc()    

#     text_carrier = {}
#     opentracing_tracer.inject(span, opentracing.Format.TEXT_MAP, text_carrier)
#     response = requests.get('http://172.21.0.7:8689/rick', headers=text_carrier)
#     data = response.json()
#     CALLS_EXTERNAL_API.labels('GET','/getapi','http://172.21.0.7:8689/rick').inc()

#     span.log_kv({'event': 'Consultando INTERNA'})

#    # logging.warning('Consultando API externa')


#     return jsonify(data) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
