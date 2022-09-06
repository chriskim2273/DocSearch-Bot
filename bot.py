import discord
import os
import requests
from io import StringIO
import json
from discord.ext import commands
import answer_retrieval

intents = discord.Intents.default()
intents.typing = False
intents.messages = True
intents.message_content = True
intents.presences = False
# client = discord.Client()
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.command()
async def get_webpage_answer(ctx, url, *args):
    print("Command Called")
    question = ""
    for arg in args:
        question = question + " " + arg
    answer = answer_retrieval.get_webpage_answer(url, question)
    print("Answer found")
    await ctx.channel.send(answer["answer"])


@bot.command()
async def get_answer_from_txt(ctx, *args):
    print("Command Called")
    question = ""
    for arg in args:
        question = question + " " + arg
    attachment_url = ctx.message.attachments[0].url
    file_request = requests.get(attachment_url)
    context = file_request.content.decode("utf-8")
    answer = answer_retrieval.get_answer(context, question)
    print("Answer Found")
    await ctx.channel.send(answer["answer"])


bot.run("NzcxODcxODk0ODA2MjAwMzQx.GUS5D7.wXs1TOc6CqMmEu5PaK6iQJcla-HDc8J-DxLu6Q")
