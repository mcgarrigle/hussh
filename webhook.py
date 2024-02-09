import os
from flask import Flask, request, Response
from . import ssh_ca

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

def sign(token, profile):
    certfile = ca.sign(f"users/{token}.pub", profile)
    with open(certfile, "r") as f:
        return f.read()

@app.route("/keys", methods=['POST'])
def webhook_post_key():
    token = request.headers["token"]
    with open(f"users/{token}.pub", "w") as f:
        f.write(request.data.decode("utf-8"))
    resp = Response()
    resp.status = '201'
    return resp

@app.route("/certs", methods=['GET'])
def webhook_get_cert():
    token = request.headers["token"]
    profile = ca.profile(token)
    if profile == {}:
        return reply(None)
    else:
        cert = sign(token, profile)
        return reply(cert)
