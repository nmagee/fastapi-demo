import httpx


people = [
    {'name': 'Student 1', 'email': 'abc123@virginia.edu'},
    {'name': 'Student 2', 'email': 'def456@virginia.edu'},
    {'name': 'Student 3', 'email': 'ghi789@virginia.edu'},
    {'name': 'Student 4', 'email': 'jkl012@virginia.edu'},
    {'name': 'Student 5', 'email': 'mno345@virginia.edu'},
    {'name': 'Student 6', 'email': 'pqr678@virginia.edu'},
    {'name': 'Student 7', 'email': 'stu901@virginia.edu'},
    {'name': 'Student 8', 'email': 'vwx234@virginia.edu'},
    {'name': 'Student 9', 'email': 'yz056@virginia.edu'},
    {'name': 'Student 10', 'email': 'abc123@virginia.edu'}
]

for person in people:
    print("Creating person")
    response = httpx.post('http://localhost:8000/people', json=person)
    print(response.json())

print("Getting people")
response = httpx.get('http://localhost:8000/people')
print(response.json())