# HUSSH

A SSH server dispensing SSH user certificates.

## Use case

You have a community of engineers to need access to a fleet of servers, on 
which you have deployed a CA public key.

This system allows an engineer to:

* Retrieve a certificate derived from the public key - with 
  restrictions applied by a system administrator.

Usage:
```
ssh tt -p 5555 cert
rsa-sha2-512-cert-v01@openssh.com AAAAIXJzYS1zaGEyLTUxMi1jZXJ0LXYwMUBvcGVuc3NoLmNvbQAAACcyMDMxMzMxOTIyNzU3ODExOTYxMzM2NDY3NDE4MjU0NTgwNzQ0MTAAAAADAQABAAABgQDf8kXhWa9lyfA/0cTtTrlgXSG5V22YIfmWHF/0hyl70KWENujMUTG10+mHDISQncKAsv8UcqKNFnj4nW150yeHaJuJ8FTHPtJgHIwlTEbGQ14i35NvCAhq4iOuoVQ06mTnRi0MIT5JZIup1rf6Mf7jfVnk2ZH8jD1GB2yC8FDfjni5nS/BZIJieLh961UK1FxVBhMerOLDf5NVEFOyAO+SvhcyMEPKrV80flXymVGr39JpBspBE3yerTregx+SoDUHIY99NmiLQ8/PbzUq59FPd8dPXyDEMbCKDPlSYjODl6+l4DrQ9uWk1e8fC6Ouc6v/bBGE9rZ6K5QwAGJ9+4E6TYh4s2ELAledmT2m1ble0imSb7WcUGrR3NSoO7BLIxwW2QfDDX6ptMApZWVxEsfPSXy+OTiT2ii/+9N3YGAzq0rmWSAf7NkwMwMcxygKHS1YBcJV5e14lVFvNGjdiy6t6R7FSM0fbbsifejsyIzPrY0Os593LCQueyRW9hE5kxUAAAAASZYC0gAAAAEAAAARc29tZXVzZXJAc29tZWhvc3QAAAAQAAAABHBldGUAAAAEcm9vdAAAAABplc84AAAAAGmXILgAAAAAAAAAggAAABVwZXJtaXQtWDExLWZvcndhcmRpbmcAAAAAAAAAF3Blcm1pdC1hZ2VudC1mb3J3YXJkaW5nAAAAAAAAABZwZXJtaXQtcG9ydC1mb3J3YXJkaW5nAAAAAAAAAApwZXJtaXQtcHR5AAAAAAAAAA5wZXJtaXQtdXNlci1yYwAAAAAAAAAAAAAAMwAAAAtzc2gtZWQyNTUxOQAAACAd7KmM8Cg7Sh7TST7k6KJfasJAb8YkbBV9sbD/1a8uuAAAAFMAAAALc3NoLWVkMjU1MTkAAABAetOwAhTTI17LYth6ODG2xMcR5ZloSuT7FboicEf3T674cA4lk5M9tJxn6ZiBe4EVrysB1lPGm0FfFPjxxZ6YCQ==

ssh tt -p 5555 cert > ~/.ssh/id_rsa-cert.pub
```

Installation:
```
git clone git@github.com:mcgarrigle/hussh.git
cd hussh/
python -m venv .venv
. .venv/bin/activate
pip3 install paramiko pyaml sshkey-tools
./setup ca
./hussh 
```

## Configuring Users

As an example we will on-board alice, who will be able to login as the 
usernames ``alice`` and ``root``.

1. Allow access to HUSSH
```
cp id_rsa.pub keys/alice.pub  # copy alice's public key so she can connect to the HUSSH server
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
