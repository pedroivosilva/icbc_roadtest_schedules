import time
import check_schedules as icbc
import telegram_bot
from telegram import Bot
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# get environment variables
BOT_API_KEY = os.getenv('BOT_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')

async def send_msg(msg1):
    bot = Bot(BOT_API_KEY)
    chat_id = CHAT_ID
    await bot.send_message(chat_id=chat_id, text=msg1)


def monitor_icbc_page(seconds: int):
    done = False
    while not done:
        try:
            dates = icbc.check_available_dates()
            time.sleep(seconds)
            done = True
        except:
            done = False
    return True, dates


def check_icbc() -> str:
    monitor, dates = monitor_icbc_page(15)
    if monitor:
        next_date = icbc.next_appointment_date(dates)
        days = icbc.next_appointment_days(dates)

        file_dates = open('dates.txt', "w")
        file_dates.write(str(dates))
        file_dates.close()

        file_next_date = open("next_date.txt", "w")
        file_next_date.write(str(next_date))
        file_next_date.close()

        file_days = open("days.txt", "w")
        file_days.write(str(days))
        file_days.close()
        result = f"OK!"

    else:
        result = f"THERE WAS AN ERROR!"

    return result


def start_monitor():
    monitor, dates = monitor_icbc_page(15)
    checks = 0
    while monitor:
        try:
            next_date = icbc.next_appointment_date(dates)
            days = icbc.next_appointment_days(dates)

            file_dates = open('dates.txt', "w")
            file_dates.write(str(dates))
            file_dates.close()

            file_next_date = open("next_date.txt", "w")
            file_next_date.write(str(next_date))
            file_next_date.close()

            file_days = open("days.txt", "w")
            file_days.write(str(days))
            file_days.close()

            file_checks = open("checks.txt", "w")
            file_checks.write(str(checks))
            file_checks.close()

            time_now = time.localtime()
            if days <= 30 and 23 > time_now.tm_hour > 7:
                msg = f"AVAILABLE APPOINTMENT UNDER 30 DAYS!"
                asyncio.run(telegram_bot.send_msg(msg))

        except Exception as e:
            error_msg = f"THERE WAS AN ERROR! THIS IS THE ERROR MESSAGE: {e}"
            asyncio.run(telegram_bot.send_msg(error_msg))

        error_msg = f"THERE WAS AN ERROR!"
        asyncio.run(telegram_bot.send_msg(error_msg))


if __name__ == '__main__':
    monitor = True
    checks = 0
    msg = f"Monitor was started right now."
    asyncio.run(telegram_bot.send_msg(msg))
    while monitor:
        monitor, dates = monitor_icbc_page(60)
        try:
            next_date = icbc.next_appointment_date(dates)
            days = icbc.next_appointment_days(dates)

            file_dates = open('dates.txt', "w")
            file_dates.write(str(dates))
            file_dates.close()

            file_next_date = open("next_date.txt", "w")
            file_next_date.write(str(next_date))
            file_next_date.close()

            file_days = open("days.txt", "w")
            file_days.write(str(days))
            file_days.close()

            file_checks = open("checks.txt", "w")
            file_checks.write(str(checks))
            file_checks.close()

            if days <= 30:
                msg = (f"AVAILABLE APPOINTMENT UNDER 30 DAYS!\n\n"
                       f"Next available appointment is {next_date}")
                asyncio.run(send_msg(msg))

        except Exception as e:
            error_msg = f"THERE WAS AN ERROR! THIS IS THE ERROR MESSAGE: {e}"
            asyncio.run(send_msg(error_msg))

    error_msg = f"THE MONITOR WAS STOPPED!"
    asyncio.run(send_msg(error_msg))
