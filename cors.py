"""
    CORS or "Cross-Origin Resource Sharing" refers to
    the situations when a frontend running in a browser has
    JavaScript code that communicates with a backend,
    and the backend is in a different "origin" than the frontend.
    More on CORS at:
    1. https://fastapi.tiangolo.com/tutorial/cors/
    2. https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

"""
# An origin is the combination of:
# protocol (http, https),
# domain (myapp.com, localhost, ...),
# and port (80, 443, 8080).
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3300"
    "http://localhost:5000",
    "http://localhost:8080"
]
