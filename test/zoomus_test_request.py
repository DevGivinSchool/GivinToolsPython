import requests

url = "https://api.zoom.us/v2/report/users"

querystring = {"page_number": "1", "page_size": "300", "to": "2019-07-09", "from": "2019-07-01", "type": "active"}

headers = {
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjdkdHI4Tlk2UTJtOTF1TjBUUW5mZVEiLCJleHAiOjE1NjMyODAwNzgsImlhdCI6MTU2MjY3NTI3OH0.zJ9dghXMZjDydLAOSOW9cbltukYNrrtm4OKhRckPw6o'}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
