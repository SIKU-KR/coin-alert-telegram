# coin-alert-telegram

### 1. assets.csv 작성하기

다음의 규칙을 따라서 assets.csv 를 본인의 계좌에 맞추어 작성해주세요. (첫줄 수정 금지)

> 코인이름,수량,평단가

### 2. Telegram 봇 만들기 (환경 세팅)

[참고게시글](https://blog.naver.com/lifelectronics/223198582215)

링크를 보고 봇을 생성한뒤, chat id 와 token 을 복사하여 "lambda_function.py" 파일에 붙여넣기하세요

### 3.  lambda_function.py 실행하기 (test)

코드파일이 있는 곳에서 터미널(cmd)를 연뒤 다음과 같이 실행할 수 있습니다

> python3 lambda_function.py

### 4. 자동화 하기

[참고게시글](https://velog.io/@gmlstjq123/EC2%EC%97%90%EC%84%9C-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%8C%8C%EC%9D%BC-%EC%8B%A4%ED%96%89%ED%95%98%EA%B8%B0)

Amazon EC2 또는 Google GCP에서 우분투를 설치하고, 파이썬 코드를 자동으로 실행되게 할 수 있습니다.

이때 지역이 북미 지역으로 설정되면 작동이 안되니 서울로 해야합니다.

pip을 설치한뒤 다음 구문을 터미널에 입력해서 설치해주세요

> pip install ccxt pandas datetime python-telegram-bot asyncio

설정된 EC2 또는 GCP 우분투에서 **Crontab**을 사용하면 특정 시간에 코드를 실행 시킬 수 있습니다.

> 0 9 * * * python3 (source위치)
