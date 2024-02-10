import os
import json
import ssh_ca
import hashlib
import functools
from flask import Flask, request, Response, redirect

base = os.path.dirname(os.path.realpath(__file__))
ca = ssh_ca.ca(base)

app = Flask(__name__)

def reply(data):
    resp = Response()
    if data is None:
        resp.status = '404'
        return resp
    else:
        resp.status = '200'
        resp.set_data(data)
        return resp

def authenticate(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        profile = ca.profile(request.headers["token"])
        if not profile: return Response('Invalid Token', 401)
        value = func(*args, **kwargs)
        return value
    return wrapper_decorator

def sign(token, profile):
    certfile = ca.sign(f"keys/{token}.pub", profile)
    with open(certfile, "r") as f:
        return f.read()

@app.route("/keys", methods=['POST'])
@authenticate
def service_post_key():
    digest = ca.store_key(request.data)
    report = { "id": digest, "href": f"/certs/{digest}" }
    response = redirect(f"/certs/{digest}", code=302)
    response.set_data(json.dumps(report))
    return response

@app.route("/certs/<digest>", methods=['GET'])
@authenticate
def service_get_cert(digest):
    token = request.headers["token"]
    profile = ca.profile(token)
    if profile:
        cert = sign(digest, profile)
        return reply(cert)
    else:
        return reply(None)
