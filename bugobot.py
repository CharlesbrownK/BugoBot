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

import discord
import asyncio
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

# @bot.command()
# async def 오늘시간표(ctx):
    

# @bot.command()
# async def 내일시간표(ctx):
    

bot.run('your_secret_token')
