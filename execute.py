from concurrent.futures import ThreadPoolExecutor
from main import main
from bot import start_bot

with ThreadPoolExecutor() as executor:
    executor.submit(main)
    executor.submit(start_bot)
