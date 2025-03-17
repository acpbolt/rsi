import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

# Load the data into a dataframe
symbol = yf.Ticker("ASHM.L")
symbol = yf.Ticker("COKE")
company_name = symbol.info['longName']
df_btc = symbol.history(interval="1d", period="max")

# Filter the data by date
df_btc = df_btc[df_btc.index > datetime(2024,1,1, tzinfo=pytz.UTC)]
df_btc = df_btc[df_btc.index < datetime(2025,3,16, tzinfo=pytz.UTC)]

# Print the result
print(df_btc)

# Delete unnecessary columns
del df_btc["Dividends"]
del df_btc["Stock Splits"]

change = df_btc["Close"].diff()
change.dropna(inplace=True)

# Create two copies of the Closing price Series
change_up = change.copy()
change_down = change.copy()

#
change_up[change_up<0] = 0
change_down[change_down>0] = 0

# Verify that we did not make any mistakes
change.equals(change_up+change_down)

# Calculate the rolling average of average up and average down
avg_up = change_up.rolling(14).mean()
avg_down = change_down.rolling(14).mean().abs()

rsi = 100 * avg_up / (avg_up + avg_down)

# Take a look at the 20 oldest datapoints
rsi.head(20)

# Set the theme of our chart
plt.style.use('fivethirtyeight')

# Make our resulting figure much bigger
plt.rcParams['figure.figsize'] = (20, 20)

# Create two charts on the same figure.
ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

# First chart:
# Plot the closing price on the first chart
ax1.plot(df_btc['Close'], linewidth=2)
ax1.set_title(company_name)

# Second chart
# Plot the RSI
ax2.set_title('Relative Strength Index')
ax2.plot(rsi, color='orange', linewidth=1)
# Add two horizontal lines, signalling the buy and sell ranges.
# Oversold
ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')
# Overbought
ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')

# Display the charts
plt.show()
