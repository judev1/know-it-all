from discord.ext.commands import Bot
import sys
import os
import json
import requests

cats = ["General Knowledge",
        "Entertainment: Books",
        "Entertainment: Film",
        "Entertainment: Music",
        "Entertainment: Musicals & Theatres",
        "Entertainment: Television",
        "Entertainment: Video Games",
        "Entertainment: Board Games",
        "Science & Nature",
        "Science: Computers",
        "Science: Mathematics",
        "Mythology",
        "Sports",
        "Geography",
        "History",
        "Politics",
        "Art",
        "Celebrities",
        "Animals",
        "Vehicles",
        "Entertainment: Comics",
        "Science: Gadgets",
        "Entertainment: Japanese Anime & Manga",
        "Entertainment: Cartoon & Animations"]
tempurl = "f'https://opentdb.com/api.php?amount={i}&category={catid}&difficulty={diff}&type=multiple'"

def replace(text):
    text = text.replace("&#039;", "'")
    text = text.replace("&quot;", '"')
    text = text.replace("74&ndash;", "-")
    return text

bot = Bot(command_prefix="kia ")

@bot.event
async def on_connect():
    print(f"\n > Began signing into Discord as {bot.user}")

@bot.event
async def on_ready():
    print(f" > Finished signing into Discord as {bot.user}\n")

@bot.event
async def on_message(message):

    if message.author.id != 270904126974590976: return
    if not message.embeds: return
    
    embed = message.embeds[0]
    if not embed.author: return
    if "trivia question" not in embed.author.name: return
    
    desc = embed.description.split("\n")
    question, answers = desc[0][2:-2], desc[3:]

    fields = embed.fields
    diff = fields[0].value[1:-1].lower()
    catid = cats.index(fields[1].value[1:-1]) + 9
    
    i = 32
    found = False
    async with message.channel.typing():
        while True:
            url = eval(tempurl)
            results = requests.get(url).json()["results"]
            if not results: i = int(i/2)
            for result in results:
                if replace(result["question"]) == question:
                    found = True
                    break
            if found: break

        correct_answer = replace(result["correct_answer"])
        for answer in answers:
            if correct_answer in answer:
                letter = "abcd"[answers.index(answer)]
                break

    await message.channel.send(f"The answer is `{letter}` (*{correct_answer}*)")

bot.run(TOKEN)
