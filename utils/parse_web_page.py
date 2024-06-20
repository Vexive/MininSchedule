from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import io
import time
import pytesseract
from PIL import Image

"""
pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract\tesseract.exe'

user_data = {}


def get_schedule_screenshot(url, group, day_selector):
    try:
        firefox_driver_path = 'C:/geckodriver/geckodriver.exe'
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        service = FirefoxService(firefox_driver_path)

        driver = webdriver.Firefox(service=service, options=firefox_options)
        driver.get(url)

        print("Страница успешно загружена")

        group_input = driver.find_element(By.CSS_SELECTOR, '#searchGroup')
        group_input.send_keys(group)
        time.sleep(1)

        submit_button = driver.find_element(By.CSS_SELECTOR,
                                            'span.input-group-btn:nth-child(3) > button:nth-child(1)')
        submit_button.click()

        time.sleep(1)

        current_day = driver.find_element(By.CSS_SELECTOR, day_selector)
        current_day.click()
        time.sleep(1)

        height = driver.execute_script("return document.body.scrollHeight")

        driver.set_window_size(1920, height)

        screenshot = driver.get_screenshot_as_png()

        driver.quit()

        return screenshot
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Этот бот создан для вывода расписания.')
    bot.send_message(message.chat.id, 'Используйте команду /schedule для получения расписания.')
    bot.send_message(message.chat.id, 'Используйте команду /scheduletoday, чтобы узнать какие сегодня пары.')


@bot.message_handler(commands=['schedule'])
def request_group(message):
    bot.send_message(message.chat.id, 'Введите название группы:')
    bot.register_next_step_handler(message, process_group_step)


def process_group_step(message):
    try:
        group = message.text.strip()
        user_data[message.chat.id] = {'group': group}
        bot.send_message(message.chat.id, 'Введите день (число от 01 до 31):')
        bot.register_next_step_handler(message, process_day_step)
    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка при вводе группы. Попробуйте снова.')


def process_day_step(message):
    try:
        day = message.text.strip().zfill(2)
        user_data[message.chat.id]['day'] = day
        bot.send_message(message.chat.id, 'Введите месяц (число от 01 до 12):')
        bot.register_next_step_handler(message, process_month_step)
    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка при вводе дня. Попробуйте снова.')


def process_month_step(message):
    try:
        month = message.text.strip().zfill(2)
        group = user_data[message.chat.id]['group']
        day = user_data[message.chat.id]['day']
        del user_data[message.chat.id]

        url = 'https://ya.mininuniver.ru/shedule'
        day_selector = f"td.day.calendar-day-2024-{month}-{day}"
        screenshot = get_schedule_screenshot(url, group, day_selector)


        if screenshot:
            image = Image.open(io.BytesIO(screenshot))

            x = 1030
            y = 370
            width = 800
            height = 800
            cropped_image = image.crop((x, y, x + width, y + height))

            text = pytesseract.image_to_string(cropped_image, lang='rus')

            bio_full = io.BytesIO()
            image.save(bio_full, format='PNG')
            bio_full.seek(0)
            bot.send_message(message.chat.id, 'Расписание с сайта:')
            bot.send_photo(message.chat.id, bio_full)

            bot.send_message(message.chat.id, f'Расписание для группы {group}:\n{text}')
        else:
            bot.send_message(message.chat.id, 'Произошла ошибка при получении расписания.')

    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


@bot.message_handler(commands=['scheduletoday'])
def request_group_today(message):
    bot.send_message(message.chat.id, 'Введите название группы:')
    bot.register_next_step_handler(message, process_group_today_step)


def process_group_today_step(message):
    try:
        group = message.text.strip()
        url = 'https://ya.mininuniver.ru/shedule'
        day_selector = "td.day.today"
        screenshot = get_schedule_screenshot(url, group, day_selector)

        if screenshot:
            image = Image.open(io.BytesIO(screenshot))

            x = 1030
            y = 370
            width = 800
            height = 800
            cropped_image = image.crop((x, y, x + width, y + height))

            text = pytesseract.image_to_string(cropped_image, lang='rus')

            bio_full = io.BytesIO()
            image.save(bio_full, format='PNG')
            bio_full.seek(0)
            bot.send_message(message.chat.id, 'Расписание с сайта:')
            bot.send_photo(message.chat.id, bio_full)

            bot.send_message(message.chat.id, f'Расписание на сегодня для группы {group}:\n{text}')
        else:
            bot.send_message(message.chat.id, 'Произошла ошибка при получении расписания.')

    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


"""
"""
pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract\tesseract.exe'

API_TOKEN = 'YOUR_BOT_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_data = {}

class Parser:
    @staticmethod
    def get_schedule_screenshot(url, group, day_selector):
        try:
            firefox_driver_path = 'C:/geckodriver/geckodriver.exe'
            firefox_options = Options()
            firefox_options.add_argument("--headless")
            service = FirefoxService(firefox_driver_path)

            driver = webdriver.Firefox(service=service, options=firefox_options)
            driver.get(url)

            print("Страница успешно загружена")

            group_input = driver.find_element(By.CSS_SELECTOR, '#searchGroup')
            group_input.send_keys(group)
            time.sleep(1)

            submit_button = driver.find_element(By.CSS_SELECTOR, 'span.input-group-btn:nth-child(3) > button:nth-child(1)')
            submit_button.click()

            time.sleep(1)

            current_day = driver.find_element(By.CSS_SELECTOR, day_selector)
            current_day.click()
            time.sleep(1)

            height = driver.execute_script("return document.body.scrollHeight")

            driver.set_window_size(1920, height)

            screenshot = driver.get_screenshot_as_png()

            driver.quit()

            return screenshot
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

class Handlers:
    @staticmethod
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        await bot.send_message(message.chat.id, 'Привет! Этот бот создан для вывода расписания.')
        await bot.send_message(message.chat.id, 'Используйте команду /schedule для получения расписания.')
        await bot.send_message(message.chat.id, 'Используйте команду /scheduletoday, чтобы узнать какие сегодня пары.')

    @staticmethod
    @dp.message_handler(commands=['schedule'])
    async def request_group(message: types.Message):
        await bot.send_message(message.chat.id, 'Введите название группы:')
        dp.register_message_handler(Handlers.process_group_step, state=None)

    @staticmethod
    async def process_group_step(message: types.Message):
        try:
            group = message.text.strip()
            user_data[message.chat.id] = {'group': group}
            await bot.send_message(message.chat.id, 'Введите день (число от 01 до 31):')
            dp.register_message_handler(Handlers.process_day_step, state=None)
        except Exception as e:
            await bot.send_message(message.chat.id, 'Ошибка при вводе группы. Попробуйте снова.')

    @staticmethod
    async def process_day_step(message: types.Message):
        try:
            day = message.text.strip().zfill(2)
            user_data[message.chat.id]['day'] = day
            await bot.send_message(message.chat.id, 'Введите месяц (число от 01 до 12):')
            dp.register_message_handler(Handlers.process_month_step, state=None)
        except Exception as e:
            await bot.send_message(message.chat.id, 'Ошибка при вводе дня. Попробуйте снова.')

    @staticmethod
    async def process_month_step(message: types.Message):
        try:
            month = message.text.strip().zfill(2)
            group = user_data[message.chat.id]['group']
            day = user_data[message.chat.id]['day']
            del user_data[message.chat.id]

            url = 'https://ya.mininuniver.ru/shedule'
            day_selector = f"td.day.calendar-day-2024-{month}-{day}"
            screenshot = Parser.get_schedule_screenshot(url, group, day_selector)

            if screenshot:
                image = Image.open(io.BytesIO(screenshot))

                x = 1030
                y = 370
                width = 800
                height = 800
                cropped_image = image.crop((x, y, x + width, y + height))

                text = pytesseract.image_to_string(cropped_image, lang='rus')

                bio_full = io.BytesIO()
                image.save(bio_full, format='PNG')
                bio_full.seek(0)
                await bot.send_message(message.chat.id, 'Расписание с сайта:')
                await bot.send_photo(message.chat.id, bio_full)

                await bot.send_message(message.chat.id, f'Расписание для группы {group}:\n{text}')
            else:
                await bot.send_message(message.chat.id, 'Произошла ошибка при получении расписания.')

        except Exception as e:
            await bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

    @staticmethod
    @dp.message_handler(commands=['scheduletoday'])
    async def request_group_today(message: types.Message):
        await bot.send_message(message.chat.id, 'Введите название группы:')
        dp.register_message_handler(Handlers.process_group_today_step, state=None)

    @staticmethod
    async def process_group_today_step(message: types.Message):
        try:
            group = message.text.strip()
            url = 'https://ya.mininuniver.ru/shedule'
            day_selector = "td.day.today"
            screenshot = Parser.get_schedule_screenshot(url, group, day_selector)

            if screenshot:
                image = Image.open(io.BytesIO(screenshot))

                x = 1030
                y = 370
                width = 800
                height = 800
                cropped_image = image.crop((x, y, x + width, y + height))

                text = pytesseract.image_to_string(cropped_image, lang='rus')

                bio_full = io.BytesIO()
                image.save(bio_full, format='PNG')
                bio_full.seek(0)
                await bot.send_message(message.chat.id, 'Расписание с сайта:')
                await bot.send_photo(message.chat.id, bio_full)

                await bot.send_message(message.chat.id, f'Расписание на сегодня для группы {group}:\n{text}')
            else:
                await bot.send_message(message.chat.id, 'Произошла ошибка при получении расписания.')

        except Exception as e:
            await bot.send_message(message.chat.id, f'Произошла ошибка: {e}')



"""