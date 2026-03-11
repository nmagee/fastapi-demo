import httpx

# This is the equivalent of a CURL request from the command line:
# curl -X POST -H "Content-Type: application/json" \
#   -d '{"name":"Myster","email":"mst3k@virginia.edu"}' \
#   http://localhost:8000/people

person = {'name': 'My Name', 'email': 'abc123@virginia.edu'}

response = httpx.post('http://localhost:8000/people', json=person)
print(response.json())

print("Getting people")
response = httpx.get('http://localhost:8000/people')
print(response.json())