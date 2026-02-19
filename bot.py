import telebot
import openai
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DRAFT_CHANNEL_ID = int(os.environ.get("DRAFT_CHANNEL_ID"))

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY


def rewrite(text):

    prompt = f"""
بازنویسی کن به سبک خبری برای رسانه Alara Entertainment.

فرمت خروجی:

🇮🇷 فارسی:
headline:
text:

🇬🇧 English:
headline:
text:

متن:
{text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
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
