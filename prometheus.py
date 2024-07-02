from flask import Flask, jsonify, request
from prometheus_client import make_wsgi_app, Counter, Histogram, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time

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

@app.route('/')
def hello():
    start_time = time.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    response = jsonify(message='Hello, world!')
    REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    REQUEST_LATENCY_G.labels('GET','/').set(time.time() - start_time)
    return response

@app.route('/teste/<segundos>', methods=['GET'])
def teste(segundos):
    start_time = time.time()
    REQUEST_COUNT.labels('GET', '/teste', 200).inc()
    time.sleep(int(segundos))
    REQUEST_LATENCY.labels('GET','/teste').observe(time.time() - start_time)
    REQUEST_LATENCY_G.labels('GET','/teste').set(time.time() - start_time)
    return {
        'msg':'Ola'        
    }




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
