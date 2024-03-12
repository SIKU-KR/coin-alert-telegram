from datetime import datetime
from binance.spot import Spot
import pandas as pd
import telegram
import asyncio

# Binance API 정보
chatId = None
token = None
api_key = None
api_secret = None
client = None


def getKey():
    global chatId, token, api_key, api_secret
    with open('./key.txt', 'r') as file:
        lines = file.readlines()
        api_key = lines[0].strip()
        api_secret = lines[1].strip()
        chatId = lines[2].strip()
        token = lines[3].strip()


async def send_fun(text):
    bot = telegram.Bot(token=token)
    await bot.sendMessage(chat_id=chatId, text=text)


def getAverageCost(symbolname):
    trades = client.my_trades(symbolname)
    total = 0
    totalQty = 0
    averageCost = 0
    for item in trades:
        if item["isBuyer"]:
            total += float(item["qty"]) * float(item["price"])
            totalQty += float(item["qty"])
            averageCost = total / totalQty
    return averageCost  # Return both total and averageCost


def getSpotList():
    ret = {}
    data = client.user_asset()
    for item in data:
        name = item['asset']
        qty = float(item['free'])
        if float(item['free']) > 1:
            ret[name] = qty
    return ret


def getMarketPrice(symbolname):
    data = client.ticker_price(symbolname)
    return float(data["price"])


def main():
    global client
    
    getKey()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")

    # get my api access
    client = Spot(api_key, api_secret)

    # dataframe process
    df = pd.DataFrame(list(getSpotList().items()), columns=['name', 'qty'])
    for index, row in df.iterrows():
        name = row['name']
        if name != 'USDT':
            df.at[index, 'average_price'] = getAverageCost(f'{name}USDT')
            df.at[index, 'current_price'] = getMarketPrice(f'{name}USDT')
    df['total_cost'] = df['qty'] * df['average_price']
    df['valuation'] = df['qty'] * df['current_price']
    df['pnl'] = df['valuation'] - df['total_cost']
    df['pnl_percentage'] = df['pnl'] / df['total_cost'] * 100
    df = df.sort_values(by='pnl', ascending=False)

    # calculate total
    total_purchase = df['total_cost'].sum()
    total_balance = df['valuation'].sum()
    pnl = total_balance - total_purchase
    pnl_percentage = pnl / total_purchase * 100

    # make telegram message
    output_str = f"{formatted_time}\n"
    output_str += f"평가손익: ${round(pnl, 2)}({round(pnl_percentage, 1)}%)\n\n"

    for index, row in df.iterrows():
        name = row['name']
        if name != 'USDT':
            output_str += f"{name}: ${round(row['pnl'], 2)}({round(row['pnl_percentage'], 1)}%)\n"

    asyncio.run(send_fun(output_str))


def lambda_handler(event, context):
    main()
    return {
        'status code': 200,
    }


if __name__ == "__main__":
    main()
