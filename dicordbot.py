# Ctrl + F で検索できる
# 2つ目の文字入れられるところで置換

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
            tenkihenkanhyou={
            "宗谷":301,
            "上川":302,
            "留萌":302,
            "網走":303,
            "北見":303,
            "紋別":303,
            "釧路":304,
            "根室":304,
            "十勝":304,
            "胆振":305,
            "日高":305,
            "石狩":306,
            "空知":306,
            "後志":306,
            "渡島":307,
            "檜山":307,
            "青森":308,
            "秋田":309,
            "岩手":310,
            "山形":311,
            "宮城":312,
            "福島":313,
            "茨城":314,
            "群馬":315,
            "栃木":316,
            "埼玉":317,
            "千葉":318,
            "東京":319,
            "神奈川":320,
            "山梨":321,
            "長野":322,
            "新潟":323,
            "富山":324,
            "石川":325,
            "福井":326,
            "静岡":327,
            "岐阜":328,
            "愛知":329,
            "三重":330,
            "大阪":331,
            "兵庫":332,
            "京都":333,
            "滋賀":334,
            "奈良":335,
            "和歌山":336,
            "島根":337,
            "広島":338,
            "鳥取":339,
            "岡山":340,
            "香川":341,
            "愛媛":342,
            "徳島":343,
            "高知":344,
            "山口":345,
            "福岡":346,
            "佐賀":347,
            "長崎":348,
            "熊本":349,
            "大分":350,
            "宮崎":351,
            "鹿児島":352,
            "沖縄":353,
            "大東島":354,
            "宮古島":355,
            "八重山":356
            }#地名とか件名を地理コードに変換するための辞書
            bashocode = tenkihenkanhyou[msg[1]]
            tenki_url = "https://www.jma.go.jp/jp/yoho/" + str(bashocode) + ".html"
            response = requests.get(tenki_url)
            soup = BeautifulSoup(response.text,'lxml')
            img = soup.find("th",class_="weather")
            iimg = img.find("img")
            tenki_setumei = soup.find("td",class_="info").text
            await message.channel.send(iimg["title"])
            await message.channel.send(tenki_setumei)


client.run("token")
