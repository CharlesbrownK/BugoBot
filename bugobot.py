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

import time
import discord
import asyncio
from socket import timeout
from codes.api import lunch_api
from discord.ext import commands

prefix = '?'
blm = lunch_api.BugoLunchMenu()
bot = commands.Bot(command_prefix = prefix, help_command = None)
tomorrow_lunch = blm.tm_lunch()
today_lunch = blm.td_lunch()


@bot.event
async def on_ready():
    print('로그인중입니다. ')
    print(f"'봇 = {bot.user.name}'으로 연결중")
    print('연결이 완료되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('BugoBot 일'))

@bot.command()
async def 오늘급식(ctx):
    if (len(today_lunch) == 0):
        await ctx.send('''```\n오늘은 급식이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```''')
    else:
        m = 1
        menu_message = "```"
        for i in today_lunch[i]:
            menu_message += m + ". " + i + "\n"
            m += 1
        menu_message += '```'
        await ctx.send(menu_message)

@bot.command()
async def 내일급식(ctx):
    if (len(tomorrow_lunch) == 0):
        await ctx.send('''```\n내일은 급식이 없습니다.[또는 데이터를 불러오지 못했습니다]\n```''')
    else:
        m = 1
        menu_message = "```"
        for i in tomorrow_lunch[i]:
            menu_message += m + ". " + i + "\n"
            m += 1
        menu_message += '```'
        await ctx.send(menu_message)

@bot.command(name="시간표")
async def time_table(ctx):
    timeout = 7
    await ctx.send("""```시간표를 확인하기 전에 사용자의 반 정보를 알아야 합니다!\n\n몇 반인지 알려주세요!\n   ex) 2-4 [⚠️ 해당 형식을 꼭 지켜주세요]\n```""")
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
        global user_class
        user_class = users_class[2:]
        
        global user_grade
        user_grade = users_class[0]
    
        await ctx.send(f"오늘 {user_grade}학년 {user_class}반 시간표 입니다.")
        await ctx.send("""```\n1. \n2. \n3. \n4. \n```""")

# @bot.command()
# async def 오늘시간표(ctx):
    

# @bot.command()
# async def 내일시간표(ctx):
    

bot.run('your_secret_token')
