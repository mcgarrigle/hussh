import os
import json
import ssh_ca
import hashlib
import functools
from flask import Flask, request, Response, redirect

base = os.path.dirname(os.path.realpath(__file__))
ca = ssh_ca.ca(base)

app = Flask(__name__)

def reply(data, code = 200):
    response = Response()
    if data is None:
        response.status = 404
    else:
        response.status = code
        response.content_type = "application/json"
        response.set_data(json.dumps(data))
    return response

def authenticate(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        profile = ca.profile(request.headers["token"])
        if not profile: return Response('Invalid Token', 401)
        value = func(*args, **kwargs)
        return value
    return wrapper_decorator

def sign(digest, profile):
    certfile = ca.sign(f"keys/{digest}.pub", profile)
    with open(certfile, "r") as f:
        return f.read()

@app.route("/keys", methods=['POST'])
@authenticate
def service_post_key():
    digest = ca.store_key(request.data)
    result = { "id": digest, "href": f"/certs/{digest}" }
    return reply(result, 201)

@app.route("/certs/<digest>", methods=['GET'])
@authenticate
def service_get_cert(digest):
    profile = ca.profile(request.headers["token"])
    certificate = sign(digest, profile)
    result = { "id": digest, "href": f"/certs/{digest}", "certificate": certificate }
    return reply(result)
