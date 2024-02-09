import os
from flask import Flask, request, Response
from . import ssh_ca

base = os.path.dirname(os.path.realpath(__file__))
ca = ssh_ca.ca(base)

app = Flask(__name__)

@app.route("/keys", methods=['POST'])
def webhook_post_key():
    token = request.headers["token"]
    print(f"POST token={token}")
    with open(f"users/{token}.pub", "w") as f:
        f.write(request.data.decode("utf-8"))
    resp = Response()
    resp.status = '201'
    return resp

@app.route("/certs", methods=['GET'])
def webhook_get_cert():
    token = request.headers["token"]
    print(f"GET token={token}")
    profile = ca.profile(token)
    if profile == {}:
        return "PROFILE NOT FOUND"
    certfile = ca.sign(f"users/{token}.pub", profile)
    with open(certfile, "r") as f:
        cert = f.read()
    return cert
