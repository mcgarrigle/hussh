# HUSSH

A HTTP SSH certificate server.

## Use case

You have a community of engineers to need access to a fleet of servers, on 
which you have deployed a CA public key.

This system allows an engineer to:

* Submit a SSH public key
* Sign and retrieve a certificate derived from the public key - with 
  restrictions applied by a system administrator.

Usage:
```
hussh key ~/.ssh/id_rsa.pub     # send your public key
1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51
```
Note the key digest. When you want to generate a new certificate use:
```
hussh cert \
   1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51 \
   > ~/.ssh/id_rsa-cert.pub
```

## Installation

```
$ pip3 install flask
$ ./setup ca
```
The CA public key that you need to distribute is found at ``ca/user_ca_key.pub``.

More info an be [found here]( https://smallstep.com/blog/use-ssh-certificates/)

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
│   └── dc9bfc42a8b7e5b309f...d63e1107.pub
├── profiles
│   ├── default
│   ├── example
│   └── pete
└── users
    └── 1e8212feddf3b955a6b...9a1fbc51 -> ../profiles/pete
```

## Starting the Server

Run in test mode using Flask::
```
./server
```
Or with a WSGI server:
```
waitress-serve --host 127.0.0.1 --port 5000 server:app
```
This is primarily meant to be run on a bastion-host accessed via 127.0.0.1, but
if you want to run this over TLS then you need to install a reverse proxy.

## Configuring Users

As an example we will on-board alice, who will be able to login as the 
usernames ``alice`` and ``root``.

1. Generate user token:
```
echo 'random string'| sha256sum -
de07bfdba346deb20705712c2ea07e7191d57f07d793c8c0698ded085bdb5cce  -
```
2. Create a profile for this user at ``profiles/alice``:
```
key_id: 1001
serial: 1
principals:
- alice
- root
extensions:
- permit-X11-forwarding
- permit-agent-forwarding
- permit-port-forwarding
- permit-pty
- permit-user-rc
validity: +1d
```
3. Create token link to profile:
```
ln -s profiles/alice users/de07bfdba346deb20705712c2ea07e7191d57f07d793c8c0698ded085bdb5cce
```
## HUSSH API

Submit your public key:
```
$ curl \
  -H 'Authorization: Bearer 1e8212feddf3b955a6b...9a1fbc51' \
  -H "Content-Type: text" \
  -d@$HOME/.ssh/id_rsa.pub \
  http://127.0.0.1:5000/keys

{"id": "dc9bfc42a8b7e5b309f...d63e1107", "href": "/certs/dc9bfc42a8b7e5b309f...d63e1107"}
```
Sign the public key you supplied above:
```
$ curl \
  -H 'Authorization: Bearer 1e8212feddf3b955a6b...9a1fbc51' \
  http://127.0.0.1:5000/certs/dc9bfc42a8b7e5b309f...763d63e1107
```

Unit tests
```
$ python -m unittest discover
```
