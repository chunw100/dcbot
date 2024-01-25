import discord
import os
from fuzzywuzzy import fuzz
import random
import google.generativeai as genai
from keep_online import keep

keep()

def ai(q):
  genai.configure(api_key=os.environ['API'])

  generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
  }

  safety_settings = []

  model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

  prompt_parts = [q]

  response = model.generate_content(prompt_parts)
  return(response.text)

bad_words = [
    '不雅字眼', '智障', '神經病', '笨蛋', '他媽', '傻逼', '垃圾', 'fuck', '幹你娘', '靠北', '三小',
    '有病喔', '腦殘'
]

oth = {
    "!rickroll我":
    "像我這種品德優良的機器人怎麼可能會rickroll你啊.....................應該吧\n\n\n\n\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nhttps://youtu.be/dQw4w9WgXcQ",
    "你好機器人": "你好，我是由某某某開發的智能機器人\n我可以偵測不雅字眼"
}

rand = [
    "嗨", "需要幫忙嗎？", "你想吃什麼?", "你想喝什麼?", "你想玩什麼?", "嘿", "www", "找我有事嗎？", "我是機器人",
    "你確定？", "真的喔"
]

similarity_threshold = 40

TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = discord.Client(intents=intents)




@client.event
async def on_ready():
  print(f'Logged in as {client.user.name}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  content = message.content

  if content.startswith("!botsay "):
    await message.channel.send(content[8:])
    await message.delete()
    return

  if content.startswith("!ai "):
    await message.channel.send(ai(content[4:]))
    return
  # 遍歷不雅字眼清單中的每個字眼
  for word in bad_words:
    similarity = fuzz.token_sort_ratio(content, word)
    if similarity > similarity_threshold or word in content:
      await message.channel.send('偵測到不雅字眼')
      break
  if content in oth:
    await message.channel.send(oth[content])
  elif content.startswith('!'):
    await message.channel.send(random.choice(rand))



client.run(TOKEN)


