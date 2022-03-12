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

import os
import time
import discord
import asyncio
from email import message
from datetime import date
from socket import timeout
from unicodedata import name
from genericpath import exists
from discord.ext import commands
from keep_alive import keep_alive
from codes.api.lunch_api import BugoLunchMenu

# bot initial settings
prefix = '&'
blm = BugoLunchMenu()
intents= discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = prefix, intents=intents)
bot.remove_command("help")

# declare dictionary which contains users information
global users_dic
users_dic = {}

# bot status
@bot.event
async def on_ready():
    print('로그인중입니다. ')
    print(f"'봇 = {bot.user.name}'으로 연결중")
    print('연결이 완료되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('BugoBot 일'))

# bot help command
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use &help <command> for extended information on a command.", color = ctx.author.color)
    em.add_field(name = "Moderation", value = "1. 급식\n2. 내일급식\n3. 시간표\n4. 내일급식\n5. 설정")

    await ctx.send(embed = em)

# client command error
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.CommandError):
    await ctx.send("해당 명령어는 존재하지 않습니다 ;-;")

# send message when bot invited new server
@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("안녕하세요, 저는 부천고등학교 봇, BugoBot, 입니다.\n저에게는 이러한 기능들이 있어요!")
            await channel.send("""```\n   1. help\n   2. 급식\n   3. 내일급식\n   4. 내일시간표\n   5. 시간표\n   6. 서버정보\n   7. 설정\n   8. 수행평가\n   9. 전체수행평가```""")
            await channel.send("명령어를 실행하시기 위해서는, & 을 명령어 앞에 붙이셔야 해요!")
        break

# set servers' owner's class number and grade
@bot.command(name="설정")
async def settings(ctx):
    timeout = 7
    await ctx.send("기본 세팅 모드입니다.")
    text = """```\n몇 반인지 알려주세요!\n   ex) 2-4 [⚠️ 해당 형식을 꼭 지켜주세요]\n```"""
    await ctx.send(text)

    # get users message
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

# print server's owners class number and grade
@bot.command(name="서버정보")
async def servers_info(ctx):
    guild_name = str(ctx.guild.name)
    
    guild_owner = str(bot.get_user(int(ctx.guild.owner.id)))
    guild_owner = guild_owner[:-5]
    
    try:
        guild_info = str(guild_name) + str(guild_owner)
        guild = users_dic[guild_info]
    except:
        await ctx.send("```\n'&설정'을 입력해 반정보를 입력하여 주세요!\n```")
    else:
        guild_grade = guild['user_grade']
        guild_class_number = guild['user_class']
        
        await ctx.send(f"""```\n해당 서버의 이름은 [{guild_name}]이고 서버 주인은 [{guild_owner}]입니다.\n서버에 입력된 학년 값은 '{guild_grade}학년'이고 반숫자 값은 '{guild_class_number}반'입니다.\n```""")
    
    print(users_dic)

# get and print today's lunch menu
@bot.command(name="급식")
async def menu(ctx):
  today_lunch = blm.td_lunch()
  if (len(today_lunch) == 0):
        await ctx.send('''```\n오늘은 급식이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```''')
  else:
        i = 0
        cnt = 1
        menu_message = "```"
        
        for menu in today_lunch:
            menu_message += str(cnt) + '. ' + menu + '\n'
            cnt += 1
            i += 1
        
        menu_message += '```'
        await ctx.send('오늘의 급식입니다.')
        await ctx.send(menu_message)

# get and print tomorrow's lunch menu
@bot.command(name='내일급식')
async def tomorrow_menu(ctx):
  tomorrow_lunch = blm.tm_lunch()
  if (len(tomorrow_lunch) == 0):
    await ctx.send('''```\n내일은 급식이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```''')
  else:
    i = 0
    cnt = 1
    menu_message = "```"
    
    for menu in tomorrow_lunch:
      menu_message += str(cnt) + '. ' + menu + '\n'
      cnt += 1
      i += 1
        
    menu_message += '```'
    await ctx.send('내일의 급식입니다.')
    await ctx.send(menu_message)

# get and print today's time table
@bot.command(name="시간표")
async def time_table(ctx):
    t = date.today().weekday()
    guild_name = str(ctx.guild.name)
    
    guild_owner = str(bot.get_user(int(ctx.guild.owner.id)))
    guild_owner = guild_owner[:-5]
    
    print(t)
    
    try:
        guild_info = str(guild_name) + str(guild_owner)
        guild = users_dic[guild_info]
    except:
        await ctx.send("```\n반 정보가 존재하지 않습니다. '&설정'을 반 정보를 입력해 주세요!\n```")
    else:
        guild_grade = guild['user_grade']
        guild_class_number = guild['user_class']
        try:
            path = './schedule_list/' + str(guild_grade) + str(guild_class_number) + '/time_table/' + str(t) +  '.txt'
            today_schedule = open(path)
        except:
            await ctx.send("```\n오늘은 수업이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```")
        else:
            if t == 5:
                await ctx.send("```\n오늘은 수업이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```")
            elif t == 6:
                await ctx.send("```\n오늘은 수업이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```")
            else:
                await ctx.send(f"오늘 {guild_grade}학년 {guild_class_number}반 시간표 입니다.[학교 사정에 따라 변경될 수 있습니다]")
                await ctx.send(str(today_schedule.read()))

# get and print tomorrow's time table
@bot.command(name="내일시간표")
async def tomorrow_time_table(ctx):
    t = date.today().weekday()
    guild_name = str(ctx.guild.name)
    
    guild_owner = str(bot.get_user(int(ctx.guild.owner.id)))
    guild_owner = guild_owner[:-5]
    
    if (t == 6):
        t = 0
    else:
        t = t + 1

    print(t)
    
    try:
        guild_info = str(guild_name) + str(guild_owner)
        guild = users_dic[guild_info]
    except:
        await ctx.send("```\n반 정보가 존재하지 않습니다. '&설정'을 반 정보를 입력해 주세요!\n```")
    else:
        guild_grade = guild['user_grade']
        guild_class_number = guild['user_class']
        try:
            path = './schedule_list/' + str(guild_grade) + str(guild_class_number) + '/time_table/' + str(t) +  '.txt'
            today_schedule = open(path)
        except:
            await ctx.send("```\n내일은 수업이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```")
        else:
            if t == 5:
                await ctx.send("```\n내일은 수업이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```")
            elif t == 6:
                await ctx.send("```\n내일은 수업이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```")
            else:
                await ctx.send(f"내일 {guild_grade}학년 {guild_class_number}반 시간표 입니다.[학교 사정에 따라 변경될 수 있습니다]")
                await ctx.send(str(today_schedule.read()))

# get and print performance evaluation
@bot.command(name="수행평가")
async def evalutaion(ctx):
    guild_name = str(ctx.guild.name)
    
    guild_owner = str(bot.get_user(int(ctx.guild.owner.id)))
    guild_owner = guild_owner[:-5]
    
    try:
        guild_info = str(guild_name) + str(guild_owner)
        guild = users_dic[guild_info]
    except:
        await ctx.send("```반 정보가 존재하지 않습니다. '&설정'을 반 정보를 입력해 주세요!```")
    else:
        guild_grade = guild['user_grade']
        guild_class_number = guild['user_class']
        
        try:
            path = './schedule_list/' + str(guild_grade) + str(guild_class_number) + '/performance_evaluation/evaluation.txt'
            today_evaluation = open(path, encoding='UTF8')
        except:
            await ctx.send("```반 정보가 존재하지 않습니다. '&설정'을 반 정보를 입력해 주세요!```")
        else:
            await ctx.send(f"{guild_grade}학년 {guild_class_number}반 수행평가입니다.[학교 사정에 따라 변경될 수 있습니다]")
            await ctx.send(today_evaluation.read())

# get and print all of performance evaluation
@bot.command(name="전체수행평가")
async def all_evalutaion(ctx):
    guild_name = str(ctx.guild.name)
    
    guild_owner = str(bot.get_user(int(ctx.guild.owner.id)))
    guild_owner = guild_owner[:-5]
    
    try:
        guild_info = str(guild_name) + str(guild_owner)
        guild = users_dic[guild_info]
    except:
        await ctx.send("```반 정보가 존재하지 않습니다. '&설정'을 반 정보를 입력해 주세요!```")
    else:
        guild_grade = guild['user_grade']
        guild_class_number = guild['user_class']
        
        try:
            path = './schedule_list/' + str(guild_grade) + str(guild_class_number) + '/performance_evaluation/all_evaluation.txt'
            today_evaluation = open(path, encoding='UTF8')
        except:
            await ctx.send("```반 정보가 존재하지 않습니다. '&설정'을 반 정보를 입력해 주세요!```")
        else:
            await ctx.send(f"{guild_grade}학년 {guild_class_number}반 전체수행평가입니다.[학교 사정에 따라 변경될 수 있습니다]")
            await ctx.send(today_evaluation.read())


@bot.command(name="ㄹㅇㅋㅋ")
async def fun(ctx):
  await ctx.send("ㄹㅇㅋㅋ")

keep_alive()

bot.run(os.environ['TOKEN'])