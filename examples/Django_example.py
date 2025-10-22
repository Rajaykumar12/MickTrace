# Description: A minimal example of using MickTrace with the Django web framework.
# This example shows how to use middleware to automatically trace all incoming requests.

# --- How to use this example with a Django project ---
# 1. Make sure you have Django and MickTrace installed:
#    pip install django micktrace

# 2. Create a new Django project if you don't have one:
#    django-admin startproject myproject
#    cd myproject

# 3. This file demonstrates the middleware. In a real project, you might save this
#    class in a file like `myproject/tracing_middleware.py`.

# 4. In your `myproject/settings.py`, add the middleware to the MIDDLEWARE list.
#    It's often best to place it near the top.
#    MIDDLEWARE = [
#        'myproject.tracing_middleware.MickTraceMiddleware',  # Add this line
#        'django.middleware.security.SecurityMiddleware',
#        # ... other middleware
#    ]

# 5. Create a view in a `views.py` file and wire it up in `urls.py`.

# 6. Run the development server:
#    python manage.py runserver
#    Now, every request to your Django site will be traced.

# --- Example Code ---

from micktrace import MickTracer

# 1. Initialize the tracer
# This should be done once when your application loads. A good place for this
# is in your project's `__init__.py` or at the top of your `settings.py`.
tracer = MickTracer(service_name="my-django-app")

class MickTraceMiddleware:
    """
    Django middleware to trace incoming HTTP requests.
    This middleware creates a span for each request, measures its duration,
    and captures relevant data like the URL and status code.
    """
    def __init__(self, get_response):
        """
        This is called once by Django when the server starts.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        This method is called for every request that Django handles.
        """
        # 2. Start a span for the incoming request.
        # The 'with' statement ensures the span is always finished correctly.
        # We name the span using the HTTP method and path for easy identification.
        with tracer.span(name=f"{request.method} {request.path}") as span:
            # Add useful attributes to the span for more context in your tracing system.
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", request.build_absolute_uri())
            span.set_attribute("http.path", request.path)
            
            # Let Django continue processing the request to get the response from the view.
            response = self.get_response(request)
            
            # 3. Add response information to the span before it's finished.
            span.set_attribute("http.status_code", response.status_code)
            
            # The span is automatically finished when the 'with' block exits.
            return response

# --- Example of a view (this would typically be in a `views.py` file) ---
#
# from django.http import HttpResponse
# import time
#
# def index(request):
#     """
#     A simple view that will be automatically traced by the middleware.
#     """
#     # You can also create nested spans for specific operations inside a view.
#     with tracer.span(name="database.query") as span:
#         # Simulate a database call
#         time.sleep(0.05)
#         span.set_attribute("db.statement", "SELECT * FROM users;")
#
#     return HttpResponse("Hello, Django! This request has been traced.")