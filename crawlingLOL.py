import requests
from bs4 import BeautifulSoup

for k in range(1,168):
    try:
        res = requests.get(f"https://lol.inven.co.kr/dataninfo/champion/detail.php?code={k}")
        soup = BeautifulSoup(res.text, "html.parser")

        chname = soup.select_one(".engName").text.split(",")[0].lower()
        chintro = soup.select_one(".descText").text.strip()
        chmail = f"{chname}@lol.inven"

        signup_data = {
            'regName': chname,
            'regPass': chname,
            'regMail': chmail,
            'regCom': chintro
        }
        files = {'regPic': requests.get(soup.select_one(".askin > img").get("src")).content}  # 파일 경로를 사용자 이미지의 실제 경로로 변경해야 합니다.
        response = requests.post('http://127.0.0.1:5000/acc/signup', data=signup_data, files=files)
    except:
        print(k)
