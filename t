
rem() {
  :
}

rem curl \
  -H 'Authorization: Bearer 1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51' \
  -H "Content-Type: application/json" \
  -d@fixtures/public_key.json \
  http://127.0.0.1:5000/keys

curl \
  -H 'Authorization: Bearer 1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51' \
  http://127.0.0.1:5000/certs/dc9bfc42a8b7e5b309f31e25a4befa214d4c7e8f43825d38a6bdd763d63e1107
