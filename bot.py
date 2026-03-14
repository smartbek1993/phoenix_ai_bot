import telebot
from telebot import types
from groq import Groq
from flask import Flask
import threading
import os

BOT_TOKEN = "8748789297:AAFuGwoFAmrXx8nkfDz6b9ZxmojiWmQaDVo"
ADMIN_ID = 123456789
GROQ_API_KEY = "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"

bot = telebot.TeleBot("8748789297:AAFuGwoFAmrXx8nkfDz6b9ZxmojiWmQaDVo")
client = Groq(api_key="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")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti!"


# START
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("📚 Kurslar")
    btn2 = types.KeyboardButton("💰 Narxlar")
    btn3 = types.KeyboardButton("📍 Manzil")
    btn4 = types.KeyboardButton("📝 Ro‘yxatdan o‘tish")
    btn5 = types.KeyboardButton("🤖 Savol berish")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)

    bot.send_message(
        message.chat.id,
        "Assalomu alaykum!\nKerakli bo‘limni tanlang yoki savol yozing.",
        reply_markup=markup
    )


# KURSLAR
@bot.message_handler(func=lambda m: m.text == "📚 Kurslar")
def courses(message):

    text = """
Bizda quyidagi kurslar mavjud:

Beginner
Elementary
Pre-Intermediate
Intermediate
IELTS tayyorlov
"""

    bot.send_message(message.chat.id, text)


# NARXLAR
@bot.message_handler(func=lambda m: m.text == "💰 Narxlar")
def prices(message):

    text = """
Kurs narxlari:

1 oy: 500 000 so'm
3 oy: 1 400 000 so'm
6 oy: 2 600 000 so'm
"""

    bot.send_message(message.chat.id, text)


# MANZIL
@bot.message_handler(func=lambda m: m.text == "📍 Manzil")
def location(message):

    bot.send_message(
        message.chat.id,
        "Manzil: Toshkent shahri\nMo'ljal: Metro yaqinida"
    )


# REGISTRATION
@bot.message_handler(func=lambda m: m.text == "📝 Ro‘yxatdan o‘tish")
def register(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn = types.KeyboardButton(
        "📱 Telefonni yuborish",
        request_contact=True
    )

    markup.add(btn)

    bot.send_message(
        message.chat.id,
        "Telefon raqamingizni yuboring.",
        reply_markup=markup
    )


# CONTACT
@bot.message_handler(content_types=['contact'])
def contact(message):

    phone = message.contact.phone_number
    name = message.from_user.first_name
    username = message.from_user.username

    text = f"""
🔥 Yangi mijoz

Ism: {name}
Username: @{username}
Telefon: {phone}
"""

    bot.send_message(ADMIN_ID, text)

    bot.send_message(
        message.chat.id,
        "Rahmat! Tez orada siz bilan bog‘lanamiz."
    )


# AI CHAT
@bot.message_handler(func=lambda message: True)
def ai_chat(message):

    try:

        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Sen ingliz tili o‘quv markazi menejerisan. Har bir savolga juda qisqa (2-3 gap) javob ber. Javob oxirida foydalanuvchini kursga yozilishga taklif qil."
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ]
        )

        answer = chat.choices[0].message.content

        bot.send_message(message.chat.id, answer)

    except Exception as e:

        print(e)

        bot.send_message(
            message.chat.id,
            "Kechirasiz, hozir javob berolmayapman."
        )


print("Bot ishlayapti...")


# BOTNI ISHGA TUSHIRISH
def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()


# FLASK SERVER (Render uchun port ochadi)
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)