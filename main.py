STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://www.newsapi.org/v2/everything"

STOCK_API_KEY = "RF6ZTTDL8R808IK8"
NEWS_API_KEY = "abd3106c3ec1406fb3f0384864f52380"
TWILIO_SID = 'TWILIO_SID'
TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN"
import requests
from twilio.rest import Client
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "apikey": STOCK_API_KEY,
    "symbol": STOCK_NAME
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
diff_percent = (difference / float(yesterday_closing_price)) * 100
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if diff_percent > 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)
    three_articles = articles[:3]
    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        if float(yesterday_closing_price) - float(day_before_yesterday_closing_price) > 0:
            message = client.messages.create(
                body=f"""TSLA: 🔺{round(diff_percent, 2)}%
                {article}""",
                from_='TWILIO_NUMBER',
                to='YOUR_NUMBER'
            )
            print(message.sid)
        else:
            message = client.messages.create(
                body=f"""TSLA: 🔻{round(diff_percent)}%
                            {article}""",
                from_='TWILIO_NUMBER',
                to='YOUR_NUMBER'
            )
            print(message.sid)

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

