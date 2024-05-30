from fastapi import FastAPI

"""
Uncomment the following lines to
enable HTTPS redirection
only works when the server is running with HTTPS
"""

# from fastapi.middleware.httpsredirect import (
#     HTTPSRedirectMiddleware,
# )

app = FastAPI(title="FastAPI Live Application")

# app.add_middleware(HTTPSRedirectMiddleware)


@app.get("/")
def read_root():
    return {"Hello": "World"}
