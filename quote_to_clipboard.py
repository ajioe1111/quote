import requests
from deep_translator import GoogleTranslator
import pyperclip
from langdetect import detect, DetectorFactory
import logging
from colorama import init, Fore, Style
import time

# Фиксированный seed для детектора языка
DetectorFactory.seed = 0

# Инициализация colorama
init()

# Настройка логирования без записи в файл
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Вывод логов на консоль
    ]
)

def get_random_quote():
    try:
        response = requests.get('https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
        response.raise_for_status()
        data = response.json()
        logging.info(Fore.GREEN + 'Успешно получена цитата' + Style.RESET_ALL)
        return data['quoteText']
    except requests.RequestException as e:
        logging.error(Fore.RED + f"Ошибка получения цитаты: {e}" + Style.RESET_ALL)
        return None

def translate_text(text, dest_lang='ru'):
    try:
        translator = GoogleTranslator(target=dest_lang)
        translated_text = translator.translate(text)
        logging.info(Fore.GREEN + f'Цитата успешно переведена на {dest_lang}' + Style.RESET_ALL)
        return translated_text
    except Exception as e:
        logging.error(Fore.RED + f"Ошибка перевода текста: {e}" + Style.RESET_ALL)
        return text

def main():
    print(Fore.CYAN + 'Привет от AJIOE1111' + Style.RESET_ALL)
    logging.info('Запуск скрипта')
    
    quote = get_random_quote()
    if quote:
        # Определение языка цитаты
        detected_lang = detect(quote)
        logging.info(Fore.YELLOW + f'Определённый язык цитаты: {detected_lang}' + Style.RESET_ALL)

        if detected_lang != 'ru':
            quote = translate_text(quote)

        # Копирование цитаты в буфер обмена
        pyperclip.copy(quote)
        logging.info(Fore.GREEN + f'Цитата скопирована в буфер обмена: "{quote}"' + Style.RESET_ALL)
    else:
        logging.warning(Fore.YELLOW + 'Цитата не получена. Скрипт завершен.' + Style.RESET_ALL)

    print(Fore.CYAN + 'Приложение завершило работу. Сделано пользователем Fuuka (AJIOE1111).' + Style.RESET_ALL)
    
    # Задержка перед закрытием приложения
    time.sleep(4)

if __name__ == "__main__":
    main()
