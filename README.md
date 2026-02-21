# HUSSH

A SSH server dispensing SSH user certificates.

## SSH Certificate CA

You have a community of engineers to need access to a fleet of servers, on 
which you have deployed a CA public key.

This system allows an engineer to:

* Authenticate to HUSSH with their SSH private/public keys

* Retrieve a certificate derived from the public key - with 
  restrictions applied by a system administrator via a defined
  profile

* This certificate will allow login to any machine that trusts it

Usage:
```
$ ssh hussh.mac.wales -p 5555 cert
rsa-sha2-512-cert-v01@openssh.com AAAAIXJzY...fFPjxxZ6YCQ==

$ ssh tt -p 5555 cert > ~/.ssh/id_rsa-cert.pub
```

## Secret Server

In addition to a SSH CA, HUSSH can act as a secret store, saving secrets in encrypted form.

Usage:
```
# set/update secret

$ ssh hussh.mac.wales -p 5555 secret set production.redis.credentials admin:passw0rd

# get secret

$ CREDENTIALS=$(ssh hussh.mac.wales -p 5555 secret set production.redis.credentials)

$ echo $CREDENTIALS
admin:passw0rd

# list secrets

$ ssh hussh.mac.wales -p 5555 secret list
production.redis.credentials
test.redis.credentials
development.redis.credentials
```

Installation:
```
$ git clone git@github.com:mcgarrigle/hussh.git
$ cd hussh/
$ ./setup install   # python venv and dependencies
$ ./setup ca        # create user and host keys
$ ./setup run       # start SSH server
```

## Configuring Users

As an example we will on-board alice, who will be able to login as the 
usernames ``alice`` and ``root``.

1. Allow access to HUSSH
```
$ cp id_rsa.pub keys/alice.pub  # copy alice's public key so she can connect to the HUSSH server
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

## Configuring Servers

Sample cloud-init user-data file that copies the ``ssh_ca_user_key`` and adds a ``sshd_config`` fragment to tell ssh to use it.

```
#cloud-config

write_files:
- path: /etc/ssh/ssh_ca_user_key.pub
  content: "${SSH_CA_USER_KEY}"
  owner: root:root
  permissions: '0644'
- path: /etc/ssh/sshd_config.d/10-ssh-certs.conf
  content: "TrustedUserCAKeys /etc/ssh/ssh_ca_user_key.pub"
  owner: root:root
  permissions: '0644'
```
