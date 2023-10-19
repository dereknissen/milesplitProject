# Track Visualizations
##### Scraping and visualizing data from mo.milesplit.com

## Description
##### Throughout high school, I was an ambitious track/cross country runner. I spent a lot of my time looking at numbers
and analyzing them. Fortunately, there is a website called milesplit.com in which race stats are uploaded after every race.
I used my computer science knowledge and some tools to visualize the results for me, as MileSplit does not do this.
This was a great way of practicing the ETL process. I used BeautifulSoup & Selenium WebDriver to extract the data, and
then I used Pandas to transform the data to fit my arrays. Finally, I used MatPlotLib to load and visualize the data on plot charts.

## Components
##### BeautifulSoup - For scraping team rosters (quicker but can't login)
##### Selenium WebDriver - For scraping individual stats (slower, but can login for more data)
##### MatPlotLib - Visualization library

##### https://www.youtube.com/watch?v=c4Af2FcgamA - For components of the project
##### https://www.youtube.com/watch?v=lTypMlVBFM4&t=383s - Dynamic Data Scraping
##### https://devinrourke.github.io/posts/python-milesplit-part1/ - Milesplit scraping
