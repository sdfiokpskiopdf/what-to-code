import requests
import threading



def create_post():
    for i in range(100):
        res = requests.post(
            "http://localhost:5000/api/v1/posts/",
            json={
                "title": "Test",
                "desc": "This was made from the API",
                "tags": ["API", "cool"],
            },
        )
        print(res.status_code)


create_post()
