# Theoretical Options Pricing Application

## What is this?
This Python/Streamlit applciation takes real-time data from Yahoo Finance and calculates the theoretical value of stock option contracts utilizing the Black-Scholes pricing model. The user is able to input any valid ticker and select from the available expiry dates. The application will then calculate the theoretical pricing for these given inputs for every strike price that is offered. It also displays the current market value for those same contracts, allowing the user to compare and analyze the theoretical prices against the actual prices.

## Why?
As I found myself looking at the more complex and quantitative side of the stock market, I grew an interest in trading options. As I dug deeper into the pricing of the options, I started the notice that even when a stock was trading flat, both the short-term call options and put options tend to decrease in value, even though the underlying security has barely moved. With that, I wanted to learn more about the way in which the prices of options contracts were calculated. After learning of the Black-Scholes model, I looked to understand more about the effects of implied volatility and time decay, as I believed understanding the way that the many factors in which an options contract's price is affected would help me manage my risk as I trade these derivatives. 

# Technologies
* Streamlit
* Python
* Matplotlib
* yFinance module
* pandas
* numPy