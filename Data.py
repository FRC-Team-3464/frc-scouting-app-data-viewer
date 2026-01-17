import json
import requests

#url = ["https://pokeapi.co/api/v2/pokemon/pikachu"]#
#res = requests.get(url)
x='{"name":"John"}'
f= json.loads(x)

print(f["name"])
