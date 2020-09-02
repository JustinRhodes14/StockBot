# Stockly - Graphing data and providing you real time information about stocks in your discord server!

Author: Justin Rhodes

# About Stockly

I started working on Stockly as a way to learn more about Python, as well as to experiment more with retrieving data, and turning it into something more meaningful for a user. Another motivation for this project was for me to learn more about the stock market, and provide a useful tool to myself and my friends as we get more involved with investing. My technical stack consisted of Python, Bokeh, Pandas, Finnhub's API (Stock data library), and Discord's API. As of now, there are 5 commands, I plan on adding a database in the future so people can have their own portfolios of stocks track stocks that they own.

# General
Currently there are five commands, I plan on adding a portfolio command that allows users to track the stocks they currently own;

!quote <TICKER_SYMBOL>

The quote command will return various information/statistics about a given stock, such as the current price, P/E ratio, 52 week high and low, market cap, and more. It returns the company name, the ticker symbol, and the companies logo. Some stocks have placeholder images, however, I plan on adding their respective images in as I learn more about which stocks are lacking images.

!news <TICKER_SYMBOL> <ARTICLE_NUMBER>

The cnews command returns articles related to the given company that may impact its stock in some way. It returns the headline, a link to the article, as well as a summary of the article. It will also return the thumbnail of the article, as well as the companies logo. The command will inform the user how many articles are available, and will let them know which article out of the total amount they are currently looking at.

!chart <TICKER_SYMBOL> <DATE_RANGE>

The chart command will return candlestick data for a given company's stock, for a given X_RANGE. Currently, you can view the weekly (WK), half year (HY), yearly (Y), and 5 year (5Y) ranges for a company's candlestick chart data. The command will then request the data from pandas datareader, and will plot the data on a chart using bokeh, which will then send the png image to the server for users to view.

!recommend <TICKER_SYMBOL>

!recommend returns analyst recommendations about a companys stock in the form of a stacked bar graph. It will inform you about how many analysts are saying you should buy, strongly buy, sell, strongly sell, and hold. This command will request the data through Finnhub's API, and the data will be plotted using bokeh. An appropriate legend is sent before the chart is sent.

!eps <TICKER_SYMBOL>

!eps returns a companies quarterly earnings, and plots the points on the graph, showing the difference between the two in the center of the actual EPS. This command requests the data through Finnhub's API, and the data is plotted using bokeh. The legend is sent before the eps chart is sent.
