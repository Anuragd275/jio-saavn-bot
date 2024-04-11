import telebot
from config import BOT_TOKEN as TOKEN
from backend import fetch_details

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    chat_id = message.chat.id
    sender_name = message.from_user.first_name if message.from_user.first_name else "Unknown"
    bot.send_message(
        chat_id, f"Hi, {sender_name}\n\nI can download songs available on Jio Saavn, send me title of a song to get started.")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    song_title = message.text
    details = fetch_details(song_title)

    title = details['title']
    artist = details['artist']
    duration = details['duration']
    thumbnail_img = open(f'thumbnail/{title}.jpg', 'rb')
    file_to_send = open(f'song/{title}.mp3', 'rb')

    bot_username = "@jio_saavn_songs_bot"
    bot.send_audio(chat_id, file_to_send,
                   caption=f'{bot_username}', title=title,  performer=artist, duration=duration, thumbnail=thumbnail_img, timeout=90.0)


bot.polling()
