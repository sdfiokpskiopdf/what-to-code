import requests
from essential_generators import DocumentGenerator
import threading

gen = DocumentGenerator()


def create_post():
    for i in range(10):
        res = requests.post(
            "http://localhost:5000/api/v1/posts/",
            json={
                "title": gen.word(),
                "desc": gen.word(),
                "tags": [gen.word(), gen.word(), gen.word()],
            },
        )
        print(res.status_code)


for i in range(10):
    t = threading.Thread(target=create_post)
    t.start()
