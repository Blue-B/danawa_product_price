import requests as r
import bs4
import telegram
import asyncio
import time
import schedule


async def main():
    bot= telegram.Bot(token='Your_Token_Here')
    chat_id = 'Your_chat_id_here'

    product_lnk =['32861312',
                  '33421820',
                  '40580420',
                  '32494520',
                  '13512254'
                  ]
    for product_lnk in product_lnk:
        url = f'https://prod.danawa.com/info/?pcode={product_lnk}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
            
        }
        first_response = r.get(url, headers=headers)
        cookies = first_response.cookies

        product_response = r.get(url, headers=headers, cookies=cookies)
        soup = bs4.BeautifulSoup(product_response.text, features='lxml')
        product_name = soup.findAll(class_="title")
        price_lines = soup.findAll(class_="prc_c")
        # print(price_lines)
        # print(product_name)


        products = []
        prices=[]
        for price in price_lines:
            result_price = price.text.replace('[<em class="prc_c">','')
            result_price =  price.text.replace('</em>, <em class="prc_c">524,000</em>, <em class="prc_c">553,930</em>]','')
            prices.append(result_price)
            
        for product in product_name:
            result_product = product.text.replace('[<span class="title">','')
            result_product = product.text.replace('</span>','')
            products.append(result_product)
            

        await bot.sendMessage(chat_id=chat_id,text=f'{products[0]} : {prices[0]}원')

def job():
    asyncio.run(main())


schedule.every(1).hour.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
