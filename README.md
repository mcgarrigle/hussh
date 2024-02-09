

curl -XPOST \
  -H 'Token: 1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51' \
  -H "Content-Type: application/json" \
  -d '{}' \
  -k https://192.168.1.142:5000/user

curl -L \
  -H 'Token: 1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51' \
  -H "Content-Type: text;utf-8" \
  -d@$HOME/.ssh/id_rsa.pub \
  -k https://192.168.1.142:5000/keys

curl  \
  -H 'Token: 1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51' \
  -k https://192.168.1.142:5000/certs
