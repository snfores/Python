import discord
import random
import requests
from bs4 import BeautifulSoup

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    mes = list(message.content.split())
    if client.user != message.author:
        if mes[0] == "$lol":#lolのゲームモードを決める
            m = random.choice(("SR","TFT"))
            await message.channel.send(m)
        if mes[0] == "$exit":#discord上から落とす
            await client.logout()
        if mes[0] == "$Postal":#郵便番号から住所をだすapiが使えるかhttps://miga-dev.hatenablog.com/entry/python_api参考
            if len(mes[1]) != 0:
                url = "http://zipcloud.ibsnet.co.jp/api/search?zipcode=" + str(mes[1])
                r = requests.get(url).json()
                Postal_status = (r["status"])
                if Postal_status == 400 or Postal_status == 500:
                    Postal_mes = (r["message"])
                    Pm = ("エラー" + Postal_mes)
                    await message.channel.send(Pm)
                elif Postal_status == 200:
                    if not r['results']:#status200でもresult:nullがあるため
                        await message.channel.send("予期せぬエラーが発生しました")
                    else:
                        zipcode = (r['results'][0]['zipcode'])
                        address1 = (r['results'][0]['address1'])
                        address2 = (r['results'][0]['address2'])
                        Pm = ("郵便番号" + zipcode + "の住所は" + address1 + address2 + "です")
                        await message.channel.send(Pm)
                else:
                    await message.channel.send("予期せぬエラーが発生しました")
        if mes[0] == "tenki" or mes[0] == "天気":#気象庁webページからスクレイピングで天気予報を集める
            
client.run("NTk3NDE1Mzk1NzgzMzQ0MTM4.XSHwig.dAXtO9tpRuLPUDrofNQQgZVIylE")
