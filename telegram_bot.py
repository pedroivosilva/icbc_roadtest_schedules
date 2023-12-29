import logging
# import monitor
import datetime as dt
from telegram import Update, Bot
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# get environment variables
BOT_API_KEY = os.getenv('BOT_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Not yet implemented, sorry!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = open("days.txt", "r")
    days = str(file.read())
    file.close()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="The next available appointment is {} days ahead.".format(days))


async def next_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = open("next_date.txt", "r")
    n_date = str(file.read())
    file.close()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="The next available date is {}.".format(n_date))


async def available_dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = open("dates.txt", "r")
    dates = str(file.read())
    file.close()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="These are all available dates:\n {}.".format(dates))


async def last_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = Path('dates.txt')
    last_modified = path.stat().st_mtime
    last_modified = dt.datetime.fromtimestamp(last_modified)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Last check was:\n {}.".format(
                                       last_modified.strftime("%d-%b-%Y %H:%M:%S")))


async def send_msg(msg):
    bot = Bot(BOT_API_KEY)
    chat_id = CHAT_ID
    await bot.send_message(chat_id=chat_id, text=msg)


async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = open("checks.txt", "r")
    checks = str(file.read())
    file.close()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"We already did {checks} checks until the last start.")


# async def checknow(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     result = monitor.check_icbc()
#     await context.bot.send_message(chat_id=update.effective_chat.id,
#                                    text=result)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Available commands:\n"
                                        "/start - [IN PROGRESS]Start routine check againts ICBC Road Test website.\n"
                                        "/checknow - Check againts ICBC Road Test website once.\n"
                                        "/days - Display how many days until the earliest available appointment.\n"
                                        "/nextdate - Show the earliest available appointment.\n"
                                        "/dates - Show latest 5 available dates.\n"
                                        "/lastcheck - Display when was the last check on ICBC Road Test page.")


# async def start_monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     monitor_script = open("monitor.py")
#     subprocess.call("dir C:", shell=True)
#     exec(monitor_script.read())
#     await context.bot.send_message(chat_id=update.effective_chat.id,
#                                    text="The next available date is {}.".format(n_date))


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_API_KEY).build()

    start_handler = CommandHandler('start', start)
    # checknow = CommandHandler('checknow', checknow)
    days_handler = CommandHandler('days', days)
    next_date_handler = CommandHandler('nextdate', next_date)
    available_dates = CommandHandler('dates', available_dates)
    last_check = CommandHandler('lastcheck', last_check)
    # = CommandHandler('', )
    count = CommandHandler('count', count)
    help = CommandHandler('help', help)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    # application.add_handler(checknow)
    application.add_handler(days_handler)
    application.add_handler(next_date_handler)
    application.add_handler(available_dates)
    application.add_handler(last_check)
    application.add_handler(count)
    application.add_handler(help)
    application.add_handler(echo_handler)

    application.run_polling()
