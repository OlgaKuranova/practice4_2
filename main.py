import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, message


bot = Bot(token='5846315074:AAELrKqMN5oLlhxwUHqGlPfDmfQjuar-Mms')
dp = Dispatcher(bot)


keyboard = types.InlineKeyboardMarkup(row_width=2)
button1 = types.InlineKeyboardButton(text="Москва", callback_data="Moscow")
button2 = types.InlineKeyboardButton(text="Санкт-Петербург", callback_data="Saint Petersburg")
button3 = types.InlineKeyboardButton(text="Сочи", callback_data="Sochi")
button4 = types.InlineKeyboardButton(text="Париж", callback_data="Paris")
keyboard.add(button1, button2, button3, button4)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Я Погода-бот. Выбери город, чтобы увидеть текущую погоду: ", reply_markup=keyboard)


def get_weather(message: types.Message):
    OpenWeather_token = "e0a3a76a053eae2619ebec4c4acb1951"
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message}&appid={OpenWeather_token}&units=metric"
        )
    data = r.json()

    city = data["name"]
    cur_weather = data["main"]["temp"]

    weather_description = data["weather"][0]["main"]
    if weather_description in code_to_smile:
         wd = code_to_smile[weather_description]
    else:
         wd = "Выгляните на улицу, не понимаю что там за погода."

    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    wind_dir_deg = data["wind"]["deg"]
    wind_directions = ("С", "С-В", "В", "Ю-В", "Ю", "Ю-З", "З", "С-З")
    direction = int((wind_dir_deg + 22.5) // 45 % 8)

    return (f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind_speed} м/с Направление: {wind_directions[direction]}\n"
              f"Желаю прекрасного дня!"
              )


@dp.callback_query_handler(text=["Moscow", "Saint Petersburg", "Sochi", "Paris"])
async def func(call: types.CallbackQuery):
    if call.data == "Moscow":
        await call.message.answer(get_weather("Moscow"))
    elif call.data == "Saint Petersburg":
        await call.message.answer(get_weather("Saint Petersburg"))
    elif call.data == "Sochi":
        await call.message.answer(get_weather("Sochi"))
    elif call.data == "Paris":
        await call.message.answer(get_weather("Paris"))
    else:
        await call.message.answer('Not Working!')


@dp.message_handler()
async def functions(message: types.Message):
    await message.reply("Напиши /start, чтобы посмотреть погоду")

if __name__ == '__main__':
    executor.start_polling(dp)


