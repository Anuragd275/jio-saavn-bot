import requests
import telebot
import json
import time
from credentials import BOT_TOKEN
TOKEN = BOT_TOKEN

bot = telebot.TeleBot(TOKEN)

# Functions to do extra tasks!

# extract the title of the song (User Input)


def extract_string(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string

# get the title from API


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

# downloading the song and saving as f'{title}.mp3'


def song_duration(title):
    response = requests.get(f'{CONST_SONG_LINK}{title}')
    data = response.json()
    duration = data["data"]["results"][0]["duration"]
    return duration


def song_dl(title):
    response = requests.get(f'{CONST_SONG_LINK}{title}')
    data = response.json()
    url = data['data']['results'][0]['downloadUrl'][4]['link']
    responses = requests.get(url)
    fp = open(f"{title}.mp3", 'wb')
    fp.write(responses.content)
    fp.close()

# Download 150 * 150 poster and send it as thumbnail


def song_thumbnail(title):
    response = requests.get(f'{CONST_SONG_LINK}{title}')
    data = response.json()
    image_url = data['data']['results'][0]['image'][1]['link']
    # After getting image url, use request to download it.
    image_response = requests.get(image_url)
    fp = open(f"{title}.jpg", "wb")
    fp.write(image_response.content)
    fp.close()

# -------------------- FUNCTION TERMINATION LINE --------------------
# API endpoint


CONST_SONG_LINK = 'https://saavn.me/search/songs?query='

# handeling /start and /help


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hi, I'm Alive!")

# handeling /song


@bot.message_handler(commands=['song'])
def song_request(request):
    chat_id = request.chat.id

    request_text = request.text
    title_input = extract_string(request_text, "/song")
    song_title = f'{CONST_SONG_LINK}{title_input}'
    bot.send_message(chat_id, f"Getting {title_input}")

    #  Bot username to be sent with every response(song)
    bot_username = "@jio_saavn_songs_bot"

    try:
        title = song_fetcher(title_input)
        artist = artist_fetcher(title_input)
        duration = song_duration(title_input)
        # Download the song and then send it
        song_dl(title)
        file_to_send = open(f"{title}.mp3", 'rb')
        song_thumbnail(title)
        thumbnail_img = open(f"{title}.jpg", 'rb')
        bot.send_audio(chat_id, file_to_send,
                       caption=f'{bot_username}', title=title,  performer=artist, duration=duration, thumbnail=thumbnail_img, timeout=90.0)
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")


# Run the bot
bot.infinity_polling()
