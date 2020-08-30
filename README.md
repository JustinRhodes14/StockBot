# Stockly - A Discord bot that provides information on Stocks

Author: Justin Rhodes

NOTE: This project is still in development, it currently has three fully fleshed out features, however, I plan on adding more over the month of August.

# About Stockly

I started working on Stockly as a way to learn more about Python, as well as to experiment more with retrieving data, and turning it into something more meaningful for a user. Another motivation for this project was for me to learn more about the stock market, and provide a useful tool to myself and my friends as we get more involved with investing. My technical stack consisted of Python, Bokeh, Pandas, Finnhub's API (Stock data library), and Discord's API. Currently there are only 3 commands, however as of now, I plan on adding three more commands. Once I finish the bot I plan on deploying it to a server so me and my friends can always use it even when I'm not running it on my own computer.

# General
Currently there are three commands, I will add more to the list as I work on this project more. The commands are listed below with a description;

!quote <TICKER_SYMBOL>

The quote command will return various information/statistics about a given stock, such as the current price, P/E ratio, 52 week high and low, market cap, and more. It returns the company name, the ticker symbol, and the companies logo. Some stocks have placeholder images, however, I plan on adding their respective images in as I learn more about which stocks are lacking images.

!news <TICKER_SYMBOL> <ARTICLE_NUMBER>

The cnews command returns articles related to the given company that may impact its stock in some way. It returns the headline, a link to the article, as well as a summary of the article. It will also return the thumbnail of the article, as well as the companies logo. The command will inform the user how many articles are available, and will let them know which article out of the total amount they are currently looking at.

!chart <TICKER_SYMBOL> <X_RANGE>

The chart command will return candlestick data for a given company's stock, for a given X_RANGE. Currently, you can view the weekly (WK), half year (HY), yearly (Y), and 5 year (5Y) ranges for a company's candlestick chart data. The command will then request the data from pandas datareader, and will plot the data on a chart using bokeh, which will then send the png image to the server for users to view.

# Future Plans

Currently, I plan on adding a news sentiment analysis, which will anaylze what people are saying about the market currently, providing the user insight to the company's reputation. I also plan on adding a recommendation graph command which will provide to the user a graph that will inform them what percentage of people are saying to buy, hold or sell. Lastly, I plan on adding a command that will inform users of the top and bottom movers of the week/month, as well as some alerts when something big happens to a company's stock or the company itself.
