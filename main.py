import requests
import telebot

TOKEN = '5884474456:AAEsU7xKu6uZJUL1jb7uEK2M9g-mh5sY3IM'

bot = telebot.TeleBot(TOKEN)

# Functions to do extra tasks!

def extract_string(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string

def song_fetcher(title):
    response = requests.get(f'{CONST_SONG_LINK}{title}')
    song = response["data"]["results"][0]["name"]
    return(song)

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
    print(request_text)
    title_input = extract_string(request_text, "/song")
    song_title = f'{CONST_SONG_LINK}{title_input}' 
    bot.send_message(chat_id, f"Getting {song_title}")
    # title = song_fetcher(title_input)
    # bot.send_message(chat_id, title)

bot.infinity_polling()