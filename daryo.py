import requests
from bs4 import BeautifulSoup as bs
import config
import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

HOST = 'https://daryo.uz'
HOST_T = 'https://www.terabayt.uz'
# задаем уровень логов
logging.basicConfig(level=logging.INFO)
# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

def get_html(url, params=None):
	r = requests.get(url)
	return r


def par_t(html_text):
	soup = bs(html_text, 'lxml')	
	text_teg = soup.find_all(attrs={"class": "news_item media-info scalable"})
			
	news_terra=[]
	for item in text_teg:
		news_terra.append({
			'mavzu': item.find('p', class_='news-title').get_text(),
			'heshteg': '#texnologiya',
			'izoh': item.find('p', class_=None).get_text(),
			'link': HOST_T + item.find('p', class_='news-title').find_next('a').get('href') + '/'
			})
	return news_terra



def par_d(html_text):
	soup = bs(html_text, 'lxml')	
	text_teg = soup.find_all(attrs={"class": "itemDatas"})
			
	news_daryo=[]
	for item in text_teg:
		news_daryo.append({
			'mavzu': item.find('div', class_='itemTitle').get_text(),
			'heshteg': '#' + item.find('div', class_='itemCat').get_text(),
			'vaqt': item.find('div', class_='itemData').get_text(),
			'izoh': item.find('div', class_='postText').get_text(),
			'link': HOST + item.find('div', class_='itemTitle').find_next('a').get('href')
			})
	return news_daryo


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer("admin @bbc_group")




async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		url_d = 'https://daryo.uz/category/texnologiyalar/'# for dy
		url_t = 'https://www.terabayt.uz/category/xabarlar'# for tr
		html_text_d = get_html(url_d).text
		html_text_t = get_html(url_t).text
		news_daryo = par_d(html_text_d)
		news_terra = par_t(html_text_t)
		idp = -1001471609965
		#idp = -1001462619192
		await bot.send_message(idp, f'{news_daryo[0]["heshteg"]} \n<b>{news_daryo[0]["mavzu"]}</b>\n<i>{news_daryo[0]["izoh"]}</i>\n {news_daryo[0]["link"]}', parse_mode='html' )
		await bot.send_message(idp, f'{news_terra[0]["heshteg"]} \n<b>{news_terra[0]["mavzu"]}</b>\n<i>{news_terra[0]["izoh"]}</i>\n {news_terra[0]["link"]}', parse_mode='html' )

		

if __name__ == '__main__':
	dp.loop.create_task(scheduled(7000)) # пока что оставим 10 секунд (в качестве теста)
	executor.start_polling(dp, skip_updates=True)