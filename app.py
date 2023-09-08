import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
from scipy.stats import norm

st.title('Options Pricing Application')

input_ticker = st.text_input('Select Ticker', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
st.title(input_ticker)
if input_ticker:
  ticker = yf.Ticker(input_ticker)
  st.title(ticker.info['currentPrice'])
  date_list = ticker.options

  input_date = st.selectbox('Dates', date_list)
  input_type = st.selectbox('Dates', ('Calls', 'Puts'))
  print(ticker)
  print(date_list)

  options = ticker.option_chain(date = input_date).calls if input_type == 'Calls' else ticker.option_chain(date = input_date).puts

  data = pd.DataFrame(options)


  r = 0.26 #risk free interest rate (US Treasury One Year Rate as of 2021-12-13)
  S = ticker.info['currentPrice'] #Spot price


  end_date =  dt.datetime.strptime(input_date, '%Y-%m-%d')
  start_date = dt.datetime.today() - dt.timedelta(hours = 5)

  difference = end_date-start_date
  difference_in_years = (difference.days + difference.seconds/86400)/365.2425
  t = difference_in_years #time to maturity (time in years)
  df = pd.DataFrame(columns = ['Theoretical Options Price', 'Strike', 'Implied Volatility', 'Current Price'])

  for i in options['strike'].values:
    K = i #Strike Price

    rslt_df = options.loc[options['strike'] == K]
    rslt_df = rslt_df.reset_index(drop=True)
    current_price = rslt_df['lastPrice'][0].astype(float)
    sigma = rslt_df['impliedVolatility'][0].astype(float)
    d1 = (np.log(S/K) + (r + (sigma*sigma)/2)*t)/(sigma * np.sqrt(t))
    d2 = d1-(sigma*np.sqrt(t))

    if input_type == "Calls":
      price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*t)*norm.cdf(d2, 0 ,1 )
    elif input_type == "Puts":
      price = K*np.exp(-r*t)*norm.cdf(-d2, 0 ,1 ) - S*norm.cdf(-d1, 0, 1)


    dict1 = {'Theoretical Options Price': price, 'Strike': K, 'Implied Volatility': sigma, 'Current Price': current_price }
    df = df.append(dict1,ignore_index = True)

  print("Theoretical Options Pricing for " + input_ticker + " " + input_type + ". Expiry Date: " + input_date )

  # st.dataframe(data=df)
  st.dataframe(df.style.format({"Implied Volatility": "{:.2f}", "Strike":"{:.0f}", "Current Price": "{:.2f}"}))


  strike_date= input_date
  print("Current Price of " + input_ticker + " is: $" + str(ticker.info['currentPrice']))


  def highlight_itm(s):
    return ['background-color: #90EE90']*len(s) if s.inTheMoney else None

  display_df = options[['contractSymbol','lastTradeDate', 'strike', 'lastPrice', 'inTheMoney','bid', 'ask', 'volume', 'impliedVolatility']]
  display_df = display_df.rename(columns={"contractSymbol": "Contract Symbol", "lastTradeDate": "Last Traded", 'strike' : 'Strike Price', 'lastPrice' :'Last Price', 'intheMoney' : 'In The Money', 'bid' : 'Bid', 'ask': 'Ask', 'volume': 'Volume',
                                         'impliedVolatility' : 'Impolied Volatility'})
  st.dataframe(display_df.style.apply(highlight_itm, axis=1))




  def call_pl(stock_price, strike_price, premium): 
      return np.where(stock_price > strike_price, stock_price - strike_price, 0) - premium
  def put_pl(stock_price, strike_price, premium):
    return np.where(stock_price < strike_price, strike_price - stock_price, 0) - premium

  call_options = ticker.option_chain(date = strike_date).calls
  put_options = ticker.option_chain(date = strike_date).puts
  s = np.arange(options['strike'].min()/1.5,options['strike'].max()*1.5)
  strike = st.selectbox('Strike Price',  options['strike'])
  call_rslt_df = call_options.loc[call_options['strike'] == strike]
  call_rslt_df = call_rslt_df.reset_index(drop=True)

  put_rslt_df = put_options.loc[put_options['strike'] == strike]
  put_rslt_df = put_rslt_df.reset_index(drop=True)
  try:
    call_premium =call_rslt_df['lastPrice'][0]
    put_premium = put_rslt_df['lastPrice'][0]
  except:
    raise Exception("Strike price not applicable")

  long_call = call_pl(s, strike, call_premium)
  long_put = put_pl(s, strike, put_premium)

  print("")
  print("Call option for " + input_ticker + ". Strike Price: $" + str(strike)+ ". Expiration Date: " + strike_date)
  print ("Max Loss (Premium for call):", min(long_call))
  print("")
  print("Put option for " + input_ticker + ". Strike Price: $" + str(strike) + ". Expiration Date: " + strike_date)
  print ("Max Loss (Premium for put):", min(long_put))
  print("")
  fig, ax = plt.subplots()
  ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
  ax.plot(s,long_put,label='Long Put')
  ax.plot(s,long_call,label='Long Call')
  plt.xlabel('Stock Price', ha='left')
  plt.ylabel('P&L')
  plt.legend()
  st.pyplot(fig=fig)