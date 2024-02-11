import os
import json
import functools
from flask import Flask, request, Response
import ssh_ca

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
        token = request.headers.get("token")
        if not token:
            return Response('Token Missing', 401)
        profile = ca.profile(token)
        if not profile:
            return Response('Invalid Token', 401)
        value = func(*args, **kwargs)
        return value
    return wrapper_decorator

@app.route("/keys", methods=['POST'])
@authenticate
def service_post_key():
    digest = ca.store_public_key(request.data)
    result = { "id": digest, "href": f"/certs/{digest}" }
    return reply(result, 201)

@app.route("/certs/<digest>", methods=['GET'])
@authenticate
def service_get_cert(digest):
    public_key = ca.retrieve_public_key(digest)
    profile = ca.profile(request.headers["token"])
    certificate = ca.sign(public_key, profile)
    result = { "id": digest, "href": f"/certs/{digest}", "certificate": certificate }
    return reply(result)
