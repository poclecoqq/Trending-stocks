# Trending stocks

## Project goal
The goal of this project is to give the most trending stocks on the market based on market sentiment. We want the software to be a tool to help the selection of stocks to analyse for investement. In no way it should be use for stock picking.

## Project overview


## Prerequisites
- Download a Selenium [chrome driver](https://chromedriver.chromium.org/downloads). Place it in this [folder](./app/find_stocks) under the name "chromedriver".
- Have [GOT](https://github.com/Jefferson-Henrique/GetOldTweets-python) downloaded in this [folder](./app/tweets_handler).


## How to use te interface
To launch the program, execute the following command:
```
python3 app.py [Options]
```
Where options are the following:
### Period
Stocks are analysed over a certain time period. To specify this period, you must first choose its ending date, then its length. The starting date of the period is obtained by substracting for the ending date the time period. By default, the ending date is the current day, and the period is 30 days.
```
End year:   -y YYYY 
            --year YYYY
End month:  -m MM
            --month MM
End day:    -d DD
            --day DD
Period:    -p X
            --period X
```
The specified en date must be between 1st january of 2007 and the current date.

### Sector
A sector may be specified to the program to limit the scope of the analysis. Only stocks in this sector will be considered in the analysis. By default, no sector is chosen.
```
-s XX 
--sector XX
```
XX might be one of the following values:
```
0 - All sectors
1 - cpc
2 - Clean Technologies
3 - Closed-End Funds
4 - Comm & Media
5 - Diversified industries
6 - ETP
7 - Financial services
8 - Forest Products and paper
9 - Life Science
10 - Mining
11 - Oil and gas
12 - Real Estate
13 - Technology
14 - Utilities & Pipeline
```

### Other utilities options
#### Threads
Multi-threading is used to querry Twitter. Only 2 threads are created by default. The user might specify the number of threads. Higher number of threads might give better performences, but will increase computer ressources consumption. The user has also to keep in mind that he might get blacklisted by twitter if a monstruous number of request is sent at the same time. If it happens, Twitter will not responds to any querries from your current IP address for a certain period of time.
```
-t --thread XX
```

#### Step
To start the program from a certain step, using cached data. The goal of this option is to be able to test certain parts of the program without having to execute everything.
```
-s --step X
```