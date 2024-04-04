import requests
from bs4 import BeautifulSoup

for k in range(1,1253):
    try:
        res = requests.get(f"https://pokemonkorea.co.kr/pokedex/view/{k}")
        soup = BeautifulSoup(res.text, "html.parser")

        info = soup.select_one("h3").text.split()
        chname = info[-1]
        chpass = "poke"
        chmail = info[-1] + info[-2] + "@poke.world"
        chintro = soup.select_one(".para").text.strip()

        signup_data = {
                    'regName': chname,
                    'regPass': chpass,
                    'regMail': chmail,
                    'regCom': chintro
                }
        files = {'regPic': requests.get(soup.select_one("div>img").get("src")).content} 
        response = requests.post('http://127.0.0.1:5000/acc/signup', data=signup_data, files=files)
    except:
        pass