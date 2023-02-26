import requests
import telebot
import json

TOKEN = '5884474456:AAEsU7xKu6uZJUL1jb7uEK2M9g-mh5sY3IM'

bot = telebot.TeleBot(TOKEN)

# Functions to do extra tasks!

def extract_string(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string

def song_fetcher(title):
    response = requests.get(f'{CONST_SONG_LINK}{title}')
    data = response.json()
    song = data["data"]["results"][0]["name"]
    return song

def artist_fetcher(title):
    response = requests.get(f'{CONST_SONG_LINK}{title}')
    data = response.json()
    artist_name = data["data"]["results"][0]["primaryArtists"]
    return artist_name

def song_dl(title):
    response = requests.get(f'{CONST_SONG_LINK}{title}')
    data = response.json()
    url = data['data']['results'][0]['downloadUrl'][4]['link']
    responses = requests.get(url)
    fp = open(f"{title}.mp3", 'wb')
    fp.write(responses.content)
    fp.close()

# -------------------- FUNCTION TERMINATION LINE --------------------

CONST_SONG_LINK = 'https://saavn.me/search/songs?query='

@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hi, I'm Alive!")

@bot.message_handler(commands=['song'])
def song_request(request):
    chat_id = request.chat.id

    request_text = request.text
    title_input = extract_string(request_text, "/song")

    song_title = f'{CONST_SONG_LINK}{title_input}' 
    bot.send_message(chat_id, f"Getting {title_input}")

    try:
        title = song_fetcher(title_input)
        artist = artist_fetcher(title_input)
        song_dl(title)
        file_to_send = open(f"{title}.mp3", 'rb')
        bot.send_audio(chat_id, file_to_send, caption=f'Title: {title}\n\nArtists: {artist}')

    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")

bot.infinity_polling()
