# Trending stocks

## Project goal
The goal of this project is to give the most trending stocks on the market based on market sentiment. We want the software to be a tool to help the selection of stocks to analyze for investement. In no way it should be use for stock picking.


## Project overview
The project process is done in two steps. It first fetches tweets, then perform a sentiment analysis on them. Twitter is querried with specific filters to obtain the most relevant information on the stocks given by the user. These tweets are then analyzed with TextBlob.

[app.py](./app.py) is the interface of the program.
Folders:
- [docs](./docs): Documentation of the project (UML, Design choices, etc.)
- [installDependencies](./installDependencies): Dependencies management. See [next section](#dependencies)
- [app](./app): Contains the modules of the project. The main ones are [tweets handler](./app/tweets_handler/) and [sentiment analysis](./app/sentiment_analysis.py).


## Dependencies
To have all the dependencies installes, simply enter the project virtual environnement. Read the [instructions](installDependencies/README.md)


## How to use from the command line
To launch the program, execute the following command:
```
python3 app.py [Options]
```
To list the options: ``` python3 app.py -h```
The following subsections will describe the options.

### File
The user must provide a file listing all the stock that are going to be considered by the application to give the stocks with best market sentiment. 
The file must be a csv file where each line is ``` COMPANY_NAME, TICKER ```.

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


### Threads
Multi-threading is used to querry Twitter. Only 2 threads are created by default. The user might specify the number of threads. Higher number of threads might give better performences, but will increase computer ressources consumption. The user has also to keep in mind that he might get blacklisted by twitter if a monstruous number of request is sent at the same time. If it happens, Twitter will not responds to any querries from your current IP address for a certain period of time.
```
-t --thread XX
```
