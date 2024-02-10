# HUSSH

A HTTP SSH certificate server.

## Use case

You have a community of engineers to need access to a fleet of servers, on 
which you have deployed a CA public key.

This system allows an engineer to:

* Submit a SSH public key
* Sign and retrieve a certificate derived from the public key - with 
  restrictions applied by a system administrator.

## Installation

```
$ pip3 install flask
$ ./setup ca
```
The CA public key that you need to distribute is found at ``ca/user_ca_key.pub``.

## Configuration

```
.
├── ca
│   ├── host_ca_key
│   ├── host_ca_key.pub
│   ├── user_ca_key
│   └── user_ca_key.pub
├── hosts
├── keys
│   ├── dc9bfc42a8b7e5b309f...d63e1107-cert.pub
│   └── dc9bfc42a8b7e5b309f...d63e1107.pub
├── profiles
│   ├── default
│   ├── example
│   └── pete
└── users
    └── 1e8212feddf3b955a6b...9a1fbc51 -> ../profiles/pete
```

## Starting the Server

Run in test mode:
```
$ ./server   # run with Flask
```
or with a WSGI server:
```
$ waitress-serve --host 127.0.0.1 --port 5000 server:app
```
If you want to run this over TLS then you need to install a reverse proxy.

## Configuring Users


## API Usage

Submit your public key:
```
$ curl -L \
  -H 'Token: 1e8212feddf3b955a6b...9a1fbc51' \
  -H "Content-Type: text" \
  -d@$HOME/.ssh/id_rsa.pub \
  http://127.0.0.1:5000/keys

{"id": "dc9bfc42a8b7e5b309f...d63e1107", "href": "/certs/dc9bfc42a8b7e5b309f...d63e1107"}

```
Sign the public key you supplied above:
```
$ curl \
  -H 'Token: 1e8212feddf3b955a6b...9a1fbc51' \
  http://127.0.0.1:5000/certs/dc9bfc42a8b7e5b309f...763d63e1107
```
