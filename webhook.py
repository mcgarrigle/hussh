import os
import json
import ssh_ca
import hashlib
from flask import Flask, request, Response, redirect

base = os.path.dirname(os.path.realpath(__file__))
ca = ssh_ca.ca(base)

app = Flask(__name__)

def sign(token, profile):
    certfile = ca.sign(f"keys/{token}.pub", profile)
    with open(certfile, "r") as f:
        return f.read()

def reply(data):
    resp = Response()
    if data is None:
        resp.status = '404'
        return resp
    else:
        resp.status = '200'
        resp.set_data(data)
        return resp

@app.route("/keys", methods=['POST'])
def webhook_post_key():
    token  = request.headers["token"]
    digest = ca.key(request.data)
    report = { "id": digest, "href": f"/certs/{digest}" }
    response = redirect(f"/certs/{digest}", code=302)
    response.set_data(json.dumps(report))
    return response

@app.route("/certs/<digest>", methods=['GET'])
def webhook_get_cert(digest):
    token = request.headers["token"]
    # print(f"token = {token}")
    profile = ca.profile(token)
    if profile == {}:
        return reply(None)
    else:
        cert = sign(digest, profile)
        return reply(cert)
