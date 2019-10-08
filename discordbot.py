# Ctrl + F で検索できる
# 2つ目の文字入れられるところで置換
import ast
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
    msg = list(message.content.split()) # kuruton: messageの一般的な略は msg だと思う
    if client.user != message.author:
        if msg[0] == "$lol":#lolのゲームモードを決める
            m = random.choice(("SR","TFT"))
            await message.channel.send(m)
        if msg[0] == "$exit":#discord上から落とす
            await client.logout()
        if msg[0] == "$postal":#郵便番号から住所をだすapiが使えるか https://miga-dev.hatenablog.com/entry/python_api 参考
            if len(msg[1]) != 0:
                url = "http://zipcloud.ibsnet.co.jp/api/search?zipcode=" + str(mes[1])
                r = requests.get(url).json()
                postal_status = (r["status"]) # kuruton: Pythonは snake_case が一般的
                if postal_status == 400 or postal_status == 500:
                    postal_msg = (r["message"])
                    pm = ("エラー" + postal_msg)
                    await message.channel.send(pm)
                elif postal_status == 200:
                    if not r['results']:#status200でもresult:nullがあるため
                        await message.channel.send("予期せぬエラーが発生しました")
                    else:
                        zipcode = (r['results'][0]['zipcode'])
                        address1 = (r['results'][0]['address1'])
                        address2 = (r['results'][0]['address2'])
                        pm = ("郵便番号" + zipcode + "の住所は" + address1 + address2 + "です")
                        await message.channel.send(pm)
                else:
                    await message.channel.send("予期せぬエラーが発生しました")
        if msg[0] == "tenki" or msg[0] == "天気":#気象庁webページからスクレイピングで天気予報を集める
            with open("kishoutyou_change.txt", "r", encoding="utf-8_sig") as f:
                tenkihenkanhyou = ast.literal_eval(f.read())#地名とか件名を地理コードに変換するための辞書を外部から呼び出し。https://blog.mktia.com/how-to-convert-string-to-dict/参考
            bashocode = tenkihenkanhyou[msg[1]]
            tenki_url = "https://www.jma.go.jp/jp/yoho/" + str(bashocode) + ".html"
            response = requests.get(tenki_url)
            soup = BeautifulSoup(response.text,'lxml')
            img = soup.find("th",class_="weather")
            iimg = img.find("img")
            tenki_setumei = soup.find("td",class_="info").text
            await message.channel.send(iimg["title"])
            await message.channel.send(tenki_setumei)


client.run("TOKEN")
