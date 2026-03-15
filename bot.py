import telebot
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# MENU
def menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📚 Kurslar", "💰 Narxlar")
    markup.row("📍 Manzil", "📝 Ro'yxatdan o'tish")
    markup.row("🤖 Savol berish")
    return markup

# START
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "Assalomu alaykum!\nKerakli bo'limni tanlang yoki savol yozing.",
        reply_markup=menu()
    )

# KURSLAR
@bot.message_handler(func=lambda m: m.text == "📚 Kurslar")
def kurslar(msg):
    text = """
📚 Ingliz tili kurslari

1️⃣ Beginner
2️⃣ Intermediate
3️⃣ Advanced

Davomiyligi: 3 oy
"""
    bot.send_message(msg.chat.id, text)

# NARXLAR
@bot.message_handler(func=lambda m: m.text == "💰 Narxlar")
def narx(msg):
    text = """
💰 Kurs narxi

3 oy: 400 000 so'm
"""
    bot.send_message(msg.chat.id, text)

# MANZIL
@bot.message_handler(func=lambda m: m.text == "📍 Manzil")
def manzil(msg):
    bot.send_message(
        msg.chat.id,
        "📍 Toshkent shahri\nMo'ljal: Metro yaqinida"
    )

# RO'YXATDAN O'TISH
@bot.message_handler(func=lambda m: m.text == "📝 Ro'yxatdan o'tish")
def register(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = telebot.types.KeyboardButton(
        "📞 Telefon yuborish",
        request_contact=True
    )
    markup.add(btn)

    bot.send_message(
        msg.chat.id,
        "Telefon raqamingizni yuboring",
        reply_markup=markup
    )

# TELEFON QABUL
@bot.message_handler(content_types=['contact'])
def contact(msg):
    phone = msg.contact.phone_number

    bot.send_message(
        msg.chat.id,
        f"Rahmat!\nAdmin siz bilan bog'lanadi.\nTelefon: {phone}",
        reply_markup=menu()
    )

# AI JAVOB
def ai(text):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer briefly."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }

    r = requests.post(url, headers=headers, json=data)

    return r.json()["choices"][0]["message"]["content"]

# SAVOL
@bot.message_handler(func=lambda m: True)
def chat(msg):
    try:
        answer = ai(msg.text)
        bot.send_message(msg.chat.id, answer)
    except:
        bot.send_message(msg.chat.id, "AI javob bera olmadi.")

bot.infinity_polling()

