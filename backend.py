import requests


def fetch_details(song_title):

    url = "https://saavn.dev/api/search/songs"

    querystring = {"query": f"{song_title}"}

    response = requests.get(url, params=querystring)

    data = response.json()

    response_title = data['data']['results'][0]['name']
    response_artist = data['data']['results'][0]['artists']['primary'][0]['name']
    response_duration = data['data']['results'][0]['duration']
    response_thumbnail = data['data']['results'][0]['image'][1]['url']
    response_url = data['data']['results'][0]['downloadUrl'][4]['url']

    with open(f"song/{response_title}.mp3", 'wb') as f:
        f.write(requests.get(response_url).content)

    with open(f"thumbnail/{response_title}.jpg", 'wb') as f:
        f.write(requests.get(response_thumbnail).content)

    song_details = {
        "title": f"{response_title}",
        "artist": f"{response_artist}",
        "duration": f"{response_duration}",
    }

    return song_details
