# Description: A minimal example of using MickTrace with the FastAPI web framework.
# This example demonstrates how to use MickTrace as middleware to automatically trace all incoming requests.

# To run this example:
# 1. Install the required libraries: pip install "fastapi[all]" micktrace
# 2. Run the server: uvicorn examples.fastapi_example:app --reload
# 3. Open your browser and navigate to http://127.0.0.1:8000/ or http://127.0.0.1:8000/items/42

from fastapi import FastAPI, Request
from micktrace import MickTracer
import time

# 1. Initialize the MickTracer
# Initialize the tracer once for your application.
# The 'service_name' helps you identify traces from this application.
tracer = MickTracer(service_name="my-fastapi-app")

app = FastAPI()

# 2. Add MickTrace as middleware
# Middleware is a function that processes every request before it reaches the endpoint
# and every response before it is sent to the client. This is an efficient way
# to trace all requests to your application without decorating each endpoint individually.
@app.middleware("http")
async def trace_requests(request: Request, call_next):
    """
    This middleware function creates a span for each incoming request.
    """
    # Start a new span for the incoming request.
    async with tracer.span(name=f"{request.method} {request.url.path}") as span:
        # Add relevant attributes to the span for context.
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))

        # Process the request and get the response.
        response = await call_next(request)

        # Add response attributes to the span.
        span.set_attribute("http.status_code", response.status_code)

        # The span is automatically finished here.
        return response

# A simple root endpoint.
@app.get("/")
async def root():
    """
    A simple endpoint that will be traced by the middleware.
    """
    return {"message": "Hello World"}

# An endpoint with a path parameter.
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    This endpoint simulates doing some work and will also be traced.
    """
    # You can create nested spans to trace specific operations within a request.
    with tracer.span(name="process_item") as span:
        span.set_attribute("item.id", item_id)
        # Simulate a database call or other work.
        time.sleep(0.05)
        return {"item_id": item_id}