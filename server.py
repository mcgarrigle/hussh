import os
import re
import json
import functools
from flask import Flask, request, Response
import ssh_ca

base = os.path.dirname(os.path.realpath(__file__))
ca = ssh_ca.CA(base)

app = Flask(__name__)

# 'Authorization': "Bearer eyJhbGciOiJI...uqsKRuw"

def bearer_token(rq):
    authorization = rq.headers.get("Authorization")
    if authorization is None:
        return None
    match = re.match(r'Bearer (.+)', authorization)
    if match is None:
        return None
    token = match.group(1)
    return token

def reply(data, code = 200):
    response = Response()
    if data is None:
        response.status = 404
    else:
        response.status = code
        response.content_type = "application/json"
        response.set_data(json.dumps(data))
    return response

def validate_public_key(text):
    struct = json.loads(text)
    fields = ["name", "key"]
    if len(struct) != len(fields):
        return False
    checks  = [ type(struct.get(f)) == str for f in fields ]
    return all(checks)

def authenticate(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        token = bearer_token(request)
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
    struct = json.loads(request.data)
    result = ca.store_public_key(struct["name"], struct["key"])
    return reply(result, 201)

@app.route("/certs/<digest>", methods=['GET'])
@authenticate
def service_get_cert(digest):
    result = ca.retrieve_public_key(digest)
    public_key = result["key"]
    profile = ca.profile(bearer_token(request))
    certificate = ca.sign(public_key, profile)
    result["certificate"] = certificate 
    result["href"] = f"/certs/{digest}"
    return reply(result)
