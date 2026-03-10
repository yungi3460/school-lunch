from flask import Flask, render_template_string
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEY = "82e9dc4cbc6340b2b4e3f5c8a8c56f9c"
ATPT_CODE = "J10"
SCHOOL_CODE = "7530189"

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>우리학교 급식</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{
    font-family: Arial;
    background:#f4f6f8;
    text-align:center;
}

.container{
    max-width:500px;
    margin:auto;
    background:white;
    padding:30px;
    border-radius:15px;
    box-shadow:0 0 10px rgba(0,0,0,0.1);
}

button{
    padding:10px 20px;
    margin:10px;
    font-size:16px;
    border:none;
    border-radius:8px;
    background:#4CAF50;
    color:white;
    cursor:pointer;
}

.menu{
    margin-top:20px;
    font-size:20px;
    line-height:1.8;
}
</style>
</head>

<body>

<div class="container">

<h1>🍱 우리학교 급식</h1>

<button onclick="location.href='/today'">오늘 급식</button>
<button onclick="location.href='/tomorrow'">내일 급식</button>

<div class="menu">
{{menu}}
</div>

</div>

</body>
</html>
"""

def get_menu(date):

    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"

    params = {
        "KEY": API_KEY,
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": ATPT_CODE,
        "SD_SCHUL_CODE": SCHOOL_CODE,
        "MLSV_YMD": date
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()
        menu = data["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        menu = menu.replace("<br/>","<br>")
        return menu
    except:
        return "급식 정보가 없습니다"

@app.route("/")
def home():
    return render_template_string(HTML, menu="버튼을 눌러 급식을 확인하세요")

@app.route("/today")
def today():
    date = datetime.today().strftime("%Y%m%d")
    menu = get_menu(date)
    return render_template_string(HTML, menu=menu)

@app.route("/tomorrow")
def tomorrow():
    date = (datetime.today() + timedelta(days=1)).strftime("%Y%m%d")
    menu = get_menu(date)
    return render_template_string(HTML, menu=menu)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=10000)
