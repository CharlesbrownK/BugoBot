#   Copyright (C) 2022 Junghoon Kim
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>

from email import message
from genericpath import exists
import time
from unicodedata import name
import discord
import asyncio
from socket import timeout
from codes.api import lunch_api
from discord.ext import commands

# bot initial settings
prefix = '?'
blm = lunch_api.BugoLunchMenu()
intents= discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = prefix, intents=intents)
tomorrow_lunch = blm.tm_lunch()
today_lunch = blm.td_lunch()

global users_dic
users_dic = {}

# bot status
@bot.event
async def on_ready():
    print('로그인중입니다. ')
    print(f"'봇 = {bot.user.name}'으로 연결중")
    print('연결이 완료되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('BugoBot 일'))


@bot.command(name="설정")
async def settings(ctx):
    timeout = 7
    await ctx.send("기본 세팅 모드입니다.")
    text = """```\n몇 반인지 알려주세요!\n   ex) 2-4 [⚠️ 해당 형식을 꼭 지켜주세요]\n```"""
    await ctx.send(text)
    time.sleep(0.5)
    send_message = await ctx.send(f'{timeout}초간 기다립니다!')

    def check(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await ctx.send("""```\n시간이 초과되었네요!\n다시 명령어를 입력해주세요!\n```""")
    else:
        users_class = str(msg.content)
        user_class = users_class[2:]
        user_grade = users_class[0]
        
        guild_name = str(ctx.guild.name)
        guild_owner = str(bot.get_user(int(ctx.guild.owner.id)))
        guild_owner = guild_owner[:-5]
        
        guild_info = str(guild_name) + str(guild_owner)
        
        users_dic[guild_info] = {'user_grade': user_grade, 'user_class': user_class}
        
        await ctx.send("사용자의 정보입니다.")
        await ctx.send(f"""```\n{user_grade}학년 {user_class}반\n```\n만약 올바르지 않다면, 명령어를 다시 입력해주세요!""")


@bot.command(name="서버정보")
async def servers_info(ctx):
    guild_name = str(ctx.guild.name)
    
    guild_owner = str(bot.get_user(int(ctx.guild.owner.id)))
    guild_owner = guild_owner[:-5]
    
    try:
        guild_info = str(guild_name) + str(guild_owner)
        guild = users_dic[guild_info]
    except:
        await ctx.send("```\n'?설정'을 입력해 반정보를 입력하여 주세요!\n```")
    else:
        guild_grade = guild['user_grade']
        guild_class_number = guild['user_class']
        
        await ctx.send(f"""```\n해당 서버의 이름은 [{guild_name}]이고 서버 주인은 [{guild_owner}]입니다.\n서버에 입력된 학년 값은 '{guild_grade}학년'이고 반숫자 값은 '{guild_class_number}반'입니다.\n```""")
    
    print(users_dic)


@bot.command(name="시간표")
async def time_table(ctx):
    await ctx.send(f"오늘 ??학년 ??반 시간표 입니다.")
    await ctx.send("""```\n1. \n2. \n3. \n4. \n```""")

# @bot.command()
# async def 오늘시간표(ctx):
    

# @bot.command()
# async def 내일시간표(ctx):
    

bot.run('your_secret_token')