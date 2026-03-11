import httpx

person = {'name': 'My Name', 'email': 'abc123@virginia.edu'}

response = httpx.post('http://localhost:8000/people', json=person)
print(response.json())

print("Getting people")
response = httpx.get('http://localhost:8000/people')
print(response.json())