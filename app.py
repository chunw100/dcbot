
import os
# 匯入discord模組，用於建立和管理機器人
import discord
# 匯入fuzzywuzzy模組，用於計算字串間的相似度
from fuzzywuzzy import fuzz





TOKEN = os.getenv('token')
admin = "1132119254062346290"

# 定義一個不雅字眼的清單，用於檢測使用者的訊息內容
bad_words = [
  '不雅字眼', '智障', '神經病', '笨蛋', '他媽', '傻逼', '垃圾', 'fuck', '幹你娘', '靠北', '三小','有病','腦殘'
]

oth= {
    "rickroll我":"像我這種品德優良的機器人怎麼可能會rickroll你啊.....................應該吧\n\n\n\n\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nhttps://youtu.be/dQw4w9WgXcQ",
    "你好機器人":"你好，我是由某某某開發的智能機器人\n我可以偵測不雅字眼，但我上線的時間很少",
    "test":"I'm online."
}
# 定義一個相似度閾值，用於判斷使用者的訊息是否包含不雅字眼
similarity_threshold = 40

# 建立一個Intents物件，用於指定機器人可以接收哪些事件
intents = discord.Intents.default()
# 啟用message_content屬性，讓機器人可以接收訊息內容
intents.message_content = True

# 建立一個Client物件，用於建立和管理機器人
client = discord.Client(intents=intents)

# 註冊一個事件處理函數，用於處理機器人準備就緒的事件
@client.event
async def on_ready():
  # 在終端機中印出機器人的名稱
  print(f'Logged in as {client.user.name}')

# 註冊一個事件處理函數，用於處理機器人收到訊息的事件
@client.event
async def on_message(message):
  # 如果訊息是由機器人本身發送的，則忽略它
  if message.author == client.user:
    return

  # 取得訊息的內容
  content = message.content


  if content[0]=="!" and (content[1:] in oth):
     await message.channel.send(oth[content[1:]])

  # 遍歷不雅字眼清單中的每個字眼
  for word in bad_words:
    # 計算訊息內容與不雅字眼之間的相似度
    similarity = fuzz.token_sort_ratio(content, word)
    # 如果相似度大於閾值，則認為訊息包含不雅字眼
    if similarity > similarity_threshold or word in content:
      # 在訊息所在的頻道中發送一個提醒訊息，並@某個身分組
      await message.channel.send(f'<@&{admin}> 偵測到不雅字眼')
      # 跳出迴圈，不再檢查其他不雅字眼
      break

# 使用TOKEN來登入和啟動機器人
client.run(TOKEN)

