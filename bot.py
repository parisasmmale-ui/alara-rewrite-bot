import telebot
import os
from openai import OpenAI

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DRAFT_CHANNEL_ID = int(os.environ.get("DRAFT_CHANNEL_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

# حذف webhook برای جلوگیری از conflict
bot.remove_webhook()

# ساخت client جدید OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def rewrite(text):

    prompt = f"""
بازنویسی کن به سبک خبری برای رسانه Alara Entertainment.

🇮🇷 فارسی:
headline:
text:

🇬🇧 English:
headline:
text:

متن:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


@bot.message_handler(func=lambda message: True)
def handle(message):

    if message.text:

        new_text = rewrite(message.text)

        bot.send_message(
            DRAFT_CHANNEL_ID,
            new_text
        )


print("Bot running...")
bot.infinity_polling()
