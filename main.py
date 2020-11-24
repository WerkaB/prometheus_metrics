from flask import Flask, send_file, request, Response
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
import datetime
import random
import time
from prometheus_client import Counter, generate_latest, Gauge, Summary, Histogram

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

backoff = 0.005

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

# Create a metric to track time spent and requests made.
CONCURRENT_REQUEST = Gauge('concurrent_request', 'Number of concurrent requests.')
BASIC_COUNTER = Counter('basic_counter', 'A basic counter.')
REQUEST_TIME_S = Summary('request_duration_s', 'Time spent processing request with summary')
REQUEST_TIME_H = Histogram('request_duration_h', 'Time spent processing request with histogram')


@app.route('/endpoint', methods=['GET'])
def on_endpoint():
    beginning_time = datetime.datetime.now()
    BASIC_COUNTER.inc()
    CONCURRENT_REQUEST.inc()

    # DO SOME STUFF
    timeout = backoff + random.random() * 0.001
    time.sleep(timeout)

    end_time = datetime.datetime.now()
    diff_time = (end_time - beginning_time).microseconds
    print(f"diff_time is: {diff_time}")
    REQUEST_TIME_S.observe(diff_time)
    REQUEST_TIME_H.observe(diff_time)
    CONCURRENT_REQUEST.dec()
    return("OK")



@app.route('/metrics', methods=['GET'])
def get_data():
    """Returns all data as plaintext."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)