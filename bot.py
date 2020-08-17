#BUGS
#RTX doesnt work since it returns None for its company profile I'm assuming (for both news and quote)
#Some stocks don't have pictures (DAL), should use a placeholder value (same with above RTX bug)

#Individual peoples portfolios - Ehhh
    #Show current prices of peoples lists (only current prices) - Big task, need database (server)

#Analyze
    #Robinhood analytics - Recommendation Trends

#History of P/E ratio
#Alerts? - Maybe use yahoo
#More data
    #Market cap, outstanding shares, dividends, quarterly based, earnings reports, announced next earnings reports?
    #Equity to Debt ratio
#General purpose queries
    #Top movers, bottom movers, range, (bottom x top x)
#News Sentiment

#UP NEXT
#News sentiment anaylsis (graph) ,  (recommendation trends) Analysis (robinhood thing) - maybe make a graph, top/bottom movers
import os
import random
from dotenv import load_dotenv
import finnhub
import math
from datetime import datetime, timedelta
from pandas_datareader import data
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text
from bokeh.io import export_png
from selenium.webdriver import Chrome, ChromeOptions



# 1
from discord.ext import commands
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configure API key
configuration = finnhub.Configuration(
    api_key={
        'token': os.getenv('FINNHUB_TOKEN') # Replace this
    }
)

finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))

# 2
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
def inc_dec(c, o):
    if c > o:
        value = "Increase"
    elif c < o:
        value = "Decrease"
    else:
        value = "Equal"
    return value

def time(entry):
    if entry == "HY":
        return 180
    elif entry == "Y":
        return 365
    elif entry == "WK":
        return 7
    elif entry == "5Y":
        return 1825
    return -1 #bad entry

def time2(entry):
    if entry == 180:
        return " Half-Year Chart"
    elif entry == 365:
        return " Yearly Chart"
    elif entry == 7:
        return " Weekly Chart"
    elif entry == 1825:
        return " 5-Year Chart"
    return -1 #bad entry

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="ping")
async def ponging(ctx):
    await ctx.send(f"pong {math.trunc(bot.latency * 1000)} ms")

@bot.command(name="quote") 
async def quote(ctx,*,stock):
    data = finnhub_client.quote(stock.upper())
    otherData = finnhub_client.company_basic_financials(stock.upper(), 'all')

    current = data.c
    if current == None:
        
        await ctx.send(f"The stock ***{stock.upper()}*** does not exist, please try again.")
    else: 
        high = otherData.metric["52WeekHigh"]
        low = otherData.metric["52WeekLow"]
        prevclose = data.pc
        beta = otherData.metric["beta"]
        peRatio = otherData.metric["peInclExtraTTM"]
        marketCap = otherData.metric["marketCapitalization"]
        divYield = float(otherData.metric["currentDividendYieldTTM"])
        if divYield <= 0:
            divYield2 = "N/A"
        else:
            divYield2 = str(divYield)

        data2 = finnhub_client.company_profile2(symbol=stock.upper())
        embed = discord.Embed(
        title = data2.name,
        description = stock.upper(),
        colour = discord.Colour.green()
        )
        
        embed.set_thumbnail(url=data2.logo)
        embed.add_field(name='Current Price', value = f"${current}",inline = False)
        embed.add_field(name='52 Wk High', value = f"${high}",inline = False)
        embed.add_field(name='52 Wk Low', value = f"${low}",inline = False)
        embed.add_field(name='Previous Closing Price', value = f"${prevclose}",inline = False)
        embed.add_field(name='Beta', value = f"{beta}",inline = False)
        embed.add_field(name='P/E Ratio (Trailing 12 Months)', value = f"{peRatio}",inline = False)
        embed.add_field(name='Market Cap', value = f"${marketCap}M",inline = False)
        embed.add_field(name='Div/Yield', value = f"{divYield2}",inline = False)
        embed.set_footer(text=f"{data2.exchange} - {data2.country}")
        await ctx.send(embed=embed)
        #await ctx.send(f"Here are todays prices for ***{stock.upper()}***:\n Opening price: ${opening}\n High price: ${high}\n Low price: ${low}\n Current price: ${current}\n Previous closing price: ${prevclose}")

@bot.command(name="news")
async def news(ctx,stock,number):

    dt = datetime.today() #1 week news report
    dt2 = datetime.today() - timedelta(days=7)

    end = dt.strftime("%Y-%m-%d")
    start = dt2.strftime("%Y-%m-%d")
    data = finnhub_client.company_news(stock.upper(),_from=start,to=end)
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
        embed.add_field(name='Summary :arrow_down_small: ',value= desc,inline=False)
        embed.set_footer(text= f"{data2.ticker} - {data2.exchange} - {data2.country}")

        await ctx.send(embed=embed)
    

@bot.command(name="chart")
async def chart(ctx,stock,span):
    stock2 = stock.upper()
    span2 = span.upper()
    timeVal = time(span2)

    if timeVal == -1:
        await ctx.send(f"Invalid argument {span2}, charts can be given as Weekly (WK), Half Year (HY), Yearly (Y), or 5 Year (5Y).")
        return
    
    end = datetime.today()
    start = datetime.today() - timedelta(days=timeVal)

    try:
        df = data.DataReader(name=stock2,data_source="yahoo",start=start,end=end)
    except:
        await ctx.send(f"The stock ***{stock2}*** could not be found, please try again.")
        return
    
    df["Status"] = [inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"] = (df.Open+df.Close)/2
    df["Height"] = abs(df.Open-df.Close)

    p = figure(x_axis_type='datetime',width=1000,height=300,sizing_mode="fixed",background_fill_color="#a3a3a3",background_fill_alpha=.5,
    y_axis_label="Price",x_axis_label="Date",title=f"Candlestick Data - {stock2}")
    p.grid.grid_line_alpha= 0.3

    hours_12 = 12*60*60*1000 #12 hours in milliseconds

    p.segment(df.index,df.High,df.index,df.Low,color="Black")

    p.rect(df.index[df.Status=="Increase"],df.Middle[df.Status=="Increase"],
        hours_12, df.Height[df.Status=="Increase"],fill_color="#CCFFFF",line_color="black")#y coordinate starts from the middle, x coordinate is where close > open

    p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
        hours_12, df.Height[df.Status=="Decrease"],fill_color="#FF3333",line_color="black") #day opened with a higher price

    options = ChromeOptions()
    options.add_argument("--headless")

    web_driver = Chrome(executable_path= "C:\Python38\Lib\site-packages\chromedriver.exe",options = options)

    #output_file("CS.html")
    export_png(p,filename="CS.png",webdriver = web_driver)

    data2 = finnhub_client.company_profile2(symbol=stock2)
    embed = discord.Embed(
        title = stock2 + time2(timeVal),
        description = f"Candlestick data for {data2.name}",
        colour = discord.Colour.dark_gold()
        )
    embed.set_thumbnail(url= data2.logo)
    #embed.set_image(url= "file:///E:/Projects/Stonk%20Bot/CS.png")
    embed.set_footer(text= f"{data2.ticker} - {data2.exchange} - {data2.country}")

    fileThing = open("CS.png","rb")
    f = discord.File(fileThing,"ChartData.png",spoiler = False)
    await ctx.send(embed=embed)
    await ctx.send(file= f)

@bot.command(name="recommend")
async def recommend(ctx,stock):
    
    stock2 = stock.upper()

    data = finnhub_client.recommendation_trends(stock2)

    if len(data) == 0:
        await ctx.send(f"The stock ***{stock.upper()}*** does not exist, please try again.")
        return

    p = figure(x_axis_type='datetime',plot_width=1000,plot_height=300,x_axis_label="Month", 
           y_axis_label="Recommendations",title=f"Recommendation Trends (6mo) - {stock2}",sizing_mode="fixed",
          background_fill_color="#a3a3a3",background_fill_alpha=.5)
    p.grid.grid_line_alpha=0.3
    p.toolbar.autohide = True

    data2 = data[0:6]

    for item in data2:
        
        total = int(item.buy) + int(item.hold) + int(item.sell) + int(item.strong_buy) + int(item.strong_sell)
        col1 = datetime.strptime(item.period,"%Y-%m-%d") 
        
        p.segment(x0= col1, x1=col1,y0=total-int(item.strong_buy),y1=total,line_color="#0f8058",line_width= 40,
                )
        glyph1 = Text(x=col1, y=total-(item.strong_buy), text=[str(item.strong_buy)], text_color="#FFFFFF",text_align="center")
        p.add_glyph(glyph1) if item.strong_buy > 3 else print("swag")
        total = total-int(item.strong_buy)
        
        p.segment(x0= col1, x1=col1,y0=total-int(item.buy),y1=total,line_color="#02c983",line_width= 40,
                )
        glyph2 = Text(x=col1, y=total-(item.buy), text=[str(item.buy)], text_color="#FFFFFF",text_align="center")
        p.add_glyph(glyph2) if item.buy > 3 else print("swag")
        total = total-int(item.buy)
        
        p.segment(x0= col1, x1=col1,y0=total-int(item.hold),y1=total,line_color="#cf8a0a",line_width= 40,
                )
        glyph3 = Text(x=col1, y=total-(item.hold), text=[str(item.hold)], text_color="#FFFFFF",text_align="center")
        p.add_glyph(glyph3) if item.hold > 3 else print("swag")
        total = total-int(item.hold)
        
        p.segment(x0= col1, x1=col1,y0=total-int(item.sell),y1=total,line_color="#ffda08",line_width= 40,
                )
        glyph4 = Text(x=col1, y=total-(item.sell), text=[str(item.sell)], text_color="#FFFFFF",text_align="center")
        p.add_glyph(glyph4) if item.sell > 3 else print("swag")
        total = total-int(item.sell)
        
        p.segment(x0= col1, x1=col1,y0=total-int(item.strong_sell),y1=total,line_color="#b02b13",line_width= 40,
                )
        glyph5 = Text(x=col1, y=total-(item.strong_sell), text=[str(item.strong_sell)], text_color="#FFFFFF",text_align="center")
        p.add_glyph(glyph5) if item.strong_sell > 3 else print("swag")
    
    #output_file("RT.html")
    #show(p)
    options = ChromeOptions()
    options.add_argument("--headless")

    web_driver = Chrome(executable_path= "C:\Python38\Lib\site-packages\chromedriver.exe",options = options)

    #output_file("CS.html")
    export_png(p,filename="RT.png",webdriver = web_driver)

    fileThing = open("RT.png","rb")
    f = discord.File(fileThing,"Recommendation.png",spoiler = False)
    
    data3 = finnhub_client.company_profile2(symbol=stock2)
    embed = discord.Embed(
        title = f"{stock2} - Recommendation trends",
        description = f"Recommendation trends for {data3.name}",
        colour = discord.Colour.dark_gold()
        )
    embed.set_thumbnail(url= data3.logo)
    #embed.set_image(url= "file:///E:/Projects/Stonk%20Bot/CS.png")
    embed.add_field(name='Legend', value = "Strong Buy: :evergreen_tree: Buy: :green_square: Hold: :orange_square: Sell: :yellow_square: Strong Sell: :red_square:" ,inline = False)
    embed.add_field(name='Note', value = "Recommendations less than 3 display no number on the graph" ,inline = False)
    embed.set_footer(text= f"{data3.ticker} - {data3.exchange} - {data3.country}")
    
    await ctx.send(embed=embed)
    await ctx.send(file=f)

@bot.command(name="eps")
async def eps(ctx,stock):
    stock2 = stock.upper()

    data = finnhub_client.company_earnings(stock2, limit=5)

    if len(data) == 0:
        await ctx.send(f"The stock ***{stock.upper()}*** does not exist, please try again.")
        return

    p = figure(x_axis_type='datetime',plot_width=1000,plot_height=300,x_axis_label="Period", 
           y_axis_label=f"Estimated Price per Share (EPS)",title=f"Quarterly Earnings - {stock2}",sizing_mode="fixed",
          background_fill_color="#a3a3a3",background_fill_alpha=.5,y_range=[-2,5])
    p.grid.grid_line_alpha=0.3
    p.toolbar.autohide = True


    for item in data:
        diff = abs(item.actual-item.estimate)
        diff = int(diff * 100)
        diff = float(diff/100)
        p.circle(x=item.period,y=item.estimate,fill_color="#4098d6",fill_alpha=.5,size=40,line_color="#5c5e5d")
        p.circle(x=item.period,y=item.actual,fill_color="#2eb361",fill_alpha=.6,size=40,line_color="#5c5e5d")
        glyph = Text(x=item.period, y= item.actual, text=[f"{str(diff)}"], text_color="#FFFFFF",text_align="center",
                    text_font_size="12px")
        p.add_glyph(glyph)

    options = ChromeOptions()
    options.add_argument("--headless")

    web_driver = Chrome(executable_path= "C:\Python38\Lib\site-packages\chromedriver.exe",options = options)

    #output_file("CS.html")
    export_png(p,filename="EPS.png",webdriver = web_driver)

    fileThing = open("EPS.png","rb")
    f = discord.File(fileThing,"QEarnings.png",spoiler = False)

    data3 = finnhub_client.company_profile2(symbol=stock2)
    embed = discord.Embed(
        title = f"{stock2} - Quarterly Earnings",
        description = f"EPS Surprises for {data3.name}",
        colour = discord.Colour.dark_gold()
        )
    embed.set_thumbnail(url= data3.logo)
    embed.add_field(name='**Legend**', value ="Actual: :green_square: Estimate: :blue_square:" ,inline = False)
    embed.add_field(name='**Note**', value = "The number represents the difference between the estimate and the actual value (placed on the actual value in green)" ,inline = False)
    embed.set_footer(text= f"{data3.ticker} - {data3.exchange} - {data3.country}")
    
    await ctx.send(embed=embed)
    await ctx.send(file=f)



@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title = "Stock Bot - User Guide",
        description = "All the possibilities of the Stock bot!",
        colour = discord.Colour.gold()
        )
    embed.set_thumbnail(url= "https://cdn.shopify.com/s/files/1/2118/1625/products/000786a-6_2000x2000.png?v=1586266264")
    embed.add_field(name='!quote <STOCK_TICKER>', value = "Returns the stock's prices for the day (opening, low, high, closing, previous closing)" ,inline = False)
    embed.add_field(name='!chart <STOCK_TICKER> <TIME_RANGE>', value = "Returns candlestick chart for a given stock *(Time ranges are as follows:\n Weekly = WK, Half Year = HY, Yearly = Y, Five Year = 5Y)*" ,inline = False)
    embed.add_field(name='!news <STOCK_TICKER> <ARTICLE_NUMBER>', value = "Returns a news article for a given stock (normally only yields 200 articles)" ,inline = False)
    embed.add_field(name='!recommend <STOCK_TICKER>', value = "Returns analyst recommendations as a graph" ,inline = False)
    embed.add_field(name='!eps <STOCK_TICKER>', value = "Returns a company's quarterly earnings as a graph" ,inline = False)
    embed.set_footer(text= " ***NOTE***\nFor functions that return chart data, please allow some time for the charts to be made and converted to an image")
    await ctx.send(embed=embed)

@bot.command(name="exit")
async def exit(ctx):
    await ctx.send("Shutting Down")
    await bot.close()

@news.error
async def news_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Invalid arguments, the command should look like the following: !news <STOCK_SYMBOL> <ARTICLE_NUMBER> (without the brackets).")

@quote.error
async def quote_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Invalid arguments, the command should look like the following: !quote <STOCK_SYMBOL> (without the brackets).")

@chart.error
async def chart_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument) or isinstance(error,commands.errors.MissingRequiredArgument):
        await ctx.send("Invalid arguments, the command should look like the following: !chart <STOCK_SYMBOL> <TIME_FRAME> (without the brackets).")

@recommend.error
async def recommend_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Invalid arguments, the command should look like the following: !recommend <STOCK_SYMBOL> (without the brackets).")

@eps.error
async def eps_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Invalid arguments, the command should look like the following: !eps <STOCK_SYMBOL> (without the brackets).")
bot.run(TOKEN)