#BUGS
#RTX doesnt work since it returns None for its company profile I'm assuming (for both cnews and quote)
#Some stocks don't have pictures (DAL), should use a placeholder value (same with above RTX bug)
import os
import random
from dotenv import load_dotenv
import finnhub
import math
from datetime import datetime, timedelta

# Configure API key
configuration = finnhub.Configuration(
    api_key={
        'token': 'bs1oipfrh5rbe4rks0i0' # Replace this
    }
)

finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))

# 1
from discord.ext import commands
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="ping")
async def ponging(ctx):
    await ctx.send(f"pong {math.trunc(bot.latency * 1000)} ms")

@bot.command(name="quote")
async def quote(ctx,*,stock):
    data = finnhub_client.quote(stock.upper())
    
    opening = data.o
    high = data.h
    low = data.l
    current = data.c
    prevclose = data.pc

    if (opening == None and high == None and low == None and current == None and prevclose == None):
        
        await ctx.send(f"The stock ***{stock.upper()}*** does not exist, please try again.")
    else:
        data2 = finnhub_client.company_profile2(symbol=stock)
        embed = discord.Embed(
        title = data2.name,
        description = stock,
        colour = discord.Colour.green()
        )
        
        embed.set_thumbnail(url=data2.logo)
        embed.add_field(name='Opening Price', value = f"${opening}",inline = False)
        embed.add_field(name='High Price', value = f"${high}",inline = False)
        embed.add_field(name='Low Price', value = f"${low}",inline = False)
        embed.add_field(name='Current Price', value = f"${current}",inline = False)
        embed.add_field(name='Previous Closing Price', value = f"${prevclose}",inline = False)
        embed.set_footer(text=f"{data2.exchange} - {data2.country}")
        await ctx.send(embed=embed)
        #await ctx.send(f"Here are todays prices for ***{stock.upper()}***:\n Opening price: ${opening}\n High price: ${high}\n Low price: ${low}\n Current price: ${current}\n Previous closing price: ${prevclose}")

@bot.command(name="cnews")
async def cnews(ctx,stock,number):

    dt = datetime.today() #1 week news report
    dt2 = datetime.today() - timedelta(days=7)

    end = dt.strftime("%Y-%d-%m")
    start = dt2.strftime("%Y-%d-%m")

    data = finnhub_client.company_news(stock.upper(), _from=start, to=end)

    if (len(data) == 0):
        await ctx.send(f"The stock ***{stock.upper()}*** does not exist, please try again.")
        return

    length = len(data)

    num = int(number)

    if num > length:
        await ctx.send("The number you inputted is beyond the number of articles in the list, enter a smaller number and try again.")
    else:
        item = data[num]
        headline = item.headline
        source = item.url
        desc = item.summary
        data2 = finnhub_client.company_profile2(symbol=stock)

        embed = discord.Embed(
        title = headline,
        description = f"{data2.name} ({stock.upper()}) - Article {num} of {length}",
        url = source,
        colour = discord.Colour.red()
        )
        embed.set_thumbnail(url= data2.logo)
        embed.set_image(url= item.image)
        embed.add_field(name='Summary',value= desc,inline=False)
        embed.set_footer(text= f"{data2.ticker} - {data2.exchange} - {data2.country}")

        await ctx.send(embed=embed)
    

@bot.command(name="exit")
async def exit(ctx):
    await ctx.send("Shutting Down")
    await bot.close()

@cnews.error
async def cnews_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Invalid arguments, the command should look like the following: !cnews <STOCK_SYMBOL> <ARTICLE_NUMBER> (without the brackets).")

@quote.error
async def quote_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Invalid arguments, the command should look like the following: !quote <STOCK_SYMBOL> (without the brackets).")

bot.run(TOKEN)