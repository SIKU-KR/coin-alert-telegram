import ccxt
import pandas as pd
from datetime import datetime
import telegram
import asyncio


async def send_fun(text):
    chatId = "여기에 TELEGRAM chat id 입력"
    token = "여기에 TELEGRAM token 입력"
    bot = telegram.Bot(token=token)
    await bot.sendMessage(chat_id=chatId, text=text)


def get_message():
    exchange = ccxt.binance()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # 파일 읽기
    data = pd.read_csv('assets.csv', header=0)
    # 평균매입가 계산
    data['평균매입가'] = data['수량'] * data['평단']
    # 평가금액 계산
    for index, row in data.iterrows():
        name = f"{row['이름']}/USDT"
        ticker = exchange.fetch_ticker(symbol=name)
        current_price = ticker['last']
        data.at[index, '현재가'] = ticker['last']
        data.at[index, '평가금액'] = row['수량'] * current_price
    # 평가금액 - 평균매입가로 손익 계산
    data['평가손익'] = data['평가금액'] - data['평균매입가']
    data['수익률'] = data['평가손익'] / data['평균매입가'] * 100
    # 합계 계산하기
    total_purchase = data['평균매입가'].sum()
    total_balance = data['평가금액'].sum()
    pnl = total_balance - total_purchase
    pnl_percentage = pnl / total_purchase * 100
    # 문자열 생성
    output_str = f"{formatted_time}\n"
    output_str += f"평가손익: ${round(pnl, 2)}\n"
    output_str += f"수익률: {round(pnl_percentage, 1)}%\n"
    output_str += "-" * 20 + "\n"
    for index, row in data.iterrows():
        output_str += f"{row['이름']}: ${round(row['평가손익'], 2)}, {round(row['수익률'], 1)}%\n"
    return output_str


if __name__ == "__main__":
    asyncio.run(send_fun(get_message()))
