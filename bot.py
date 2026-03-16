import telebot
from telebot import types
import sqlite3
import requests

# ===== CONFIG =====
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
ADMIN_ID = 123456789

bot = telebot.TeleBot(BOT_TOKEN)

# ===== DATABASE =====
db = sqlite3.connect("users.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER UNIQUE
)
""")
db.commit()

# ===== MENU =====
def menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📚 Kurslar", "💰 Narxlar")
    markup.row("📍 Manzil", "📝 Ro'yxatdan o'tish")
    markup.row("🤖 Savol berish")
    return markup

# ===== START =====
@bot.message_handler(commands=['start'])
def start(msg):

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (msg.from_user.id,)
    )
    db.commit()

    bot.send_message(
        msg.chat.id,
        "Assalomu alaykum!\nO'quv markaz botiga xush kelibsiz.",
        reply_markup=menu()
    )

# ===== KURSLAR =====
@bot.message_handler(func=lambda m: m.text == "📚 Kurslar")
def kurslar(msg):

    text = """
📚 Bizning kurslar:

1️⃣ Beginner
2️⃣ Intermediate
3️⃣ Advanced

Davomiyligi: 3 oy
"""

    bot.send_message(msg.chat.id, text)

# ===== NARXLAR =====
@bot.message_handler(func=lambda m: m.text == "💰 Narxlar")
def narx(msg):

    text = """
💰 Kurs narxi:

3 oy: 400 000 so'm
"""

    bot.send_message(msg.chat.id, text)

# ===== MANZIL =====
@bot.message_handler(func=lambda m: m.text == "📍 Manzil")
def manzil(msg):

    bot.send_message(
        msg.chat.id,
        "📍 Toshkent shahri\nMetro yaqinida"
    )

# ===== RO'YXATDAN O'TISH =====
@bot.message_handler(func=lambda m: m.text == "📝 Ro'yxatdan o'tish")
def register(msg):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn = types.KeyboardButton(
        "📞 Telefon yuborish",
        request_contact=True
    )

    markup.add(btn)

    bot.send_message(
        msg.chat.id,
        "Telefon raqamingizni yuboring:",
        reply_markup=markup
    )

# ===== CONTACT =====
@bot.message_handler(content_types=['contact'])
def contact(msg):

    phone = msg.contact.phone_number
    name = msg.from_user.first_name

    bot.send_message(
        msg.chat.id,
        "Rahmat! Admin siz bilan tez orada bog'lanadi.",
        reply_markup=menu()
    )

    bot.send_message(
        ADMIN_ID,
        f"🆕 Yangi ro'yxatdan o'tish\n\nIsm: {name}\nTelefon: {phone}"
    )

# ===== AI FUNCTION =====
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
                "content": "You are an assistant for a learning center."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }

    try:

        r = requests.post(url, headers=headers, json=data)

        res = r.json()

        return res["choices"][0]["message"]["content"]

    except:

        return "AI javob bera olmadi."

# ===== AI CHAT =====
@bot.message_handler(func=lambda m: m.text == "🤖 Savol berish")
def ask_ai(msg):

    bot.send_message(msg.chat.id, "Savolingizni yozing.")

@bot.message_handler(func=lambda m: True)
def chat(msg):

    bot.send_chat_action(msg.chat.id, "typing")

    answer = ai(msg.text)

    bot.send_message(msg.chat.id, answer, reply_markup=menu())

# ===== ADMIN STATS =====
@bot.message_handler(commands=['stats'])
def stats(msg):

    if msg.from_user.id == ADMIN_ID:

        cursor.execute("SELECT COUNT(*) FROM users")

        count = cursor.fetchone()[0]

        bot.send_message(
            msg.chat.id,
            f"👥 Foydalanuvchilar soni: {count}"
        )

# ===== BROADCAST =====
@bot.message_handler(commands=['send'])
def broadcast(msg):

    if msg.from_user.id == ADMIN_ID:

        text = msg.text.replace("/send ", "")

        cursor.execute("SELECT user_id FROM users")

        users = cursor.fetchall()

        for user in users:

            try:
                bot.send_message(user[0], text)
            except:
                pass

# ===== RUN =====
print("Bot ishga tushdi...")
bot.infinity_polling()