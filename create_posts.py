import requests
from essential_generators import DocumentGenerator

gen = DocumentGenerator()

for i in range(1):
	res = requests.post("http://localhost:5000/api/v1/posts/", json={"title" : gen.word(),
	 "desc" : gen.word(),
	 "tags" : [gen.word(), gen.word(), gen.word()]})
	print(res.status_code)