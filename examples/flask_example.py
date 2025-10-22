# Description: A minimal example of using MickTrace with the Flask web framework.
# This example shows how to trace incoming web requests in a simple Flask application.

# To run this example:
# 1. Install the required libraries: pip install flask micktrace
# 2. Run the script: python examples/flask_example.py
# 3. Open your browser and navigate to http://127.0.0.1:5000/

from flask import Flask
from micktrace import MickTracer
import time

# 1. Initialize the MickTracer
# It's best practice to initialize the tracer once when your application starts.
# The 'service_name' helps you identify traces from this specific application.
tracer = MickTracer(service_name="my-flask-app")

app = Flask(__name__)

# 2. Trace a Flask route
# Use the tracer's `span` context manager to wrap the logic of your web request.
# This creates a 'span' which represents a single unit of work (e.g., an HTTP request).
@app.route("/")
def hello_world():
    """
    This is the main route of the web application.
    The tracer will measure the execution time of this function.
    """
    with tracer.span(name="flask.request") as span:
        # You can add attributes to your span for more detailed context.
        # These attributes will be visible in your tracing backend.
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.url", "/")

        # Simulate some work being done
        time.sleep(0.1)

        # The span will automatically be finished when the 'with' block is exited.
        return "<p>Hello, World! This request has been traced.</p>"

if __name__ == "__main__":
    # Run the Flask development server.
    # In a production environment, you would use a production-ready WSGI server like Gunicorn.
    app.run(debug=True, port=5000)