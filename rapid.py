import requests

url = "https://api-nba-v1.p.rapidapi.com/seasons"

headers = {
    "X-RapidAPI-Key": "f76514c4dbmsh3312544c3b98049p1cb932jsn2f294071de29",
    "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())