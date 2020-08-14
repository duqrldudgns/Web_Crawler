import time
import requests
from bs4 import BeautifulSoup as bs

def check(str1, req) :
    print(str(req) + str1 + ' success!!') # 200이어도 로그인된 것인지 확인해 봐야 한다.
    # 200이 아니라면 경고를 띄워준다.
    if req.status_code != 200:
        print( str(req) + 'fail..' )

# 사용되는 URL 정리
LOGINF_URL = 'http://JB/common/login.do?method=loginF'        #    기본 URL GET
LOGIN_URL = 'http://JB/common/login.do?method=login'          #  로그인 URL POST
MACRO_URL = 'http://JB/register/major.do?method=proc&UID='    #  매크로 URL POST, 매번 값이 바뀜, 아래에서 쓰임
LOGOUT_URL = 'http://JB/common/login.do?method=logoutEnd'     #로그아웃 URL POST

#로그인 할 유저정보 (모두 문자열)
LOGIN_info = {
    'HAKBEON' : 'id',
    'PWD' : 'pwd'
}
print(LOGIN_info)

#매크로 헤더
MACRO_headers = {
    'Host': 'JB',
    'Connection': 'keep-alive',
    'Content-Length': '284',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://JB',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://JB/register/major.do?method=list&UID=',    # 매번 값이 바뀜
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
}

#매크로 쿠키
MACRO_cookies = {
    #'WMONID' : '',          # 매번 값이 바뀜
    'NetFunnel_ID' : ''
    #'JSESSIONID' : ''       # 매번 값이 바뀜
}

#매크로 데이터
MACRO_insert_1 = "GB=5&SUGANG_YEAR=2020&SUGANG_HAKGI=2&GWAMOK_CD=56054&BUNBAN=01&JAESUGANG_YEAR=&JAESUGANG_HAKGI=&JAESUGANG_GWAMOK_CD=&CAMPUS_GB=2&HAKGWA_CD=40017&GWAMOK_GB=&ISU_GB=&GWAMOK_NAME=%EC%82%AC%EC%9D%B4%EB%B2%84%ED%85%8C%EB%9F%AC%EC%99%80%EC%A0%95%EB%B3%B4%EC%A0%84&SEARCH_GUBUN=&GUBUN=INSERT"
#MACRO_insert_ = ""
#MACRO_insert_ = ""
#MACRO_insert_ = ""
#MACRO_insert_ = ""

cnt = 1
# Session 생성, with 구문 안에서 유지
with requests.Session() as s:
    while True:
        time.sleep(0.5)

        # 쿠키값을 얻기 위한 get 송신
        first_page = s.get(LOGINF_URL)
        check("first_page", first_page)

        # 매번 바뀌는 값을 파싱하여 입력, 1번만 실행
        if cnt:
            cnt-= cnt
            MACRO_cookies['JSESSIONID'] = first_page.cookies['JSESSIONID']
            MACRO_cookies['WMONID'] = first_page.cookies['WMONID']
            
        # HTTP POST Request: 로그인을 위해 POST url과 함께 전송될 data, headers, cookies 입력
        login_req = s.post(LOGIN_URL, data=LOGIN_info, headers=MACRO_headers, cookies=MACRO_cookies)
        check("login_req", login_req)

        # uid 설정, 매번 새로운 uid를 받아야 함
        html = login_req.content
        soup = bs(html, 'html.parser')
        UID = soup.find('input', {'name': 'UID'}) # input태그 중에서 name이 uid인 것을 찾는다.
        #print(UID['value']) # 위에서 찾은 태그의 value를 가져온다.
        MACRO_URL = 'http://JB/register/major.do?method=proc&UID='    #  매크로 URL POST, 매번 값이 바뀜
        MACRO_URL += UID['value']
        MACRO_headers['Referer'] += UID['value']

        # 매크로 데이터 송신
        macro_req = s.post(MACRO_URL, data=MACRO_insert_1, headers=MACRO_headers, cookies=MACRO_cookies)
        #macro_req = s.post(MACRO_URL, data=MACRO_insert_, headers=MACRO_headers, cookies=MACRO_cookies)
        #macro_req = s.post(MACRO_URL, data=MACRO_insert_, headers=MACRO_headers, cookies=MACRO_cookies)
        #macro_req = s.post(MACRO_URL, data=MACRO_insert_, headers=MACRO_headers, cookies=MACRO_cookies)
        #macro_req = s.post(MACRO_URL, data=MACRO_insert_, headers=MACRO_headers, cookies=MACRO_cookies)       
        check("macro_req", macro_req)

        #이 홈페이지에 대해서는 로그아웃 안 해주면 다음 실행 때 에러 발생
        logout_req = s.post(LOGOUT_URL, data=MACRO_insert_1, headers=MACRO_headers, cookies=MACRO_cookies)
        check("logout_req", logout_req)    


## id name = HAKBEON
## pwd name = PWD
## javascript:doLogin();

'''
<div class="login_bg">
    <div class="container">
        <div class="login_img2">
            <div class="inputid"><input type="text" id="HAKBEON" name="HAKBEON" onkeydown="if(event.keyCode==13){doLogin();return false;}" title="아이디" tabindex="1" value="" style="ime-mode:inactive" maxlength="9" class="inputidtext"></div>
            <div class="inputpass"><input type="password" id="PWD" name="PWD" onkeydown="if(event.keyCode==13){doLogin();return false;}" title="비밀번호" tabindex="2" value="" style="ime-mode:inactive" maxlength="50" class="inputpasstaxt"></div>
            <div class="loginbtn"><a href="javascript:doLogin();"><img src="/images/btn_login.png" alt="로그인" title="로그인" border="0px"></a></div>
            <div class="logininfo"><a href="javascript:noticelist()"><img src="/images/logininfo.png" title="공지사항조회" alt="공지사항조회"></a></div>
        </div>          
    </div>
</div>
'''

'''make login
POST http://JB/common/login.do?method=login HTTP/1.1
Host: JB
User-Agent: python-requests/2.24.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 35
Content-Type: application/x-www-form-urlencoded

HAKBEON=id&PWD=pwd
'''

# Cookie: WMONID=@@@@@; NetFunnel_ID=; JSESSIONID= @@@@@
'''real login       
POST http://JB/common/login.do?method=login HTTP/1.1
Host: JB
Connection: keep-alive
Content-Length: 35
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://JB
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://JB/common/login.do?method=loginF
Accept-Encoding: gzip, deflate
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: WMONID=zRruntsNImy; NetFunnel_ID=; JSESSIONID=zWClbkrODAdAeul9dIuEnEiqrYQ15tqvcxaUkw4EJoPrvaDSVuP31gnJmsldNZL5.c3VnYW5nMi9zdWdhbmc=

HAKBEON=91514969&PWD=Dudgns23%21%40
'''

# POST http://JB/register/major.do?method=proc&UID=7a7a42cc:173db1dc8ac:@@@ HTTP/1.1
# Referer: http://JB/register/major.do?method=list&UID=7a7a42cc:173db1dc8ac:@@@
# Cookie: WMONID=@@@@@; NetFunnel_ID=; JSESSIONID= @@@@@
'''real Insert 
POST http://JB/register/major.do?method=proc&UID=7a7a42cc:173db1dc8ac:b3a HTTP/1.1
Host: JB
Connection: keep-alive
Content-Length: 284
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://JB
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://JB/register/major.do?method=list&UID=7a7a42cc:173db1dc8ac:b3a
Accept-Encoding: gzip, deflate
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: WMONID=zRruntsNImy; NetFunnel_ID=; JSESSIONID=gdKmKtcYyyM8yfnMKCtFW3TC2TQqPhCAcI5T0iOYa6pyAEi1VtJs5pa6sUxS9Kwx.c3VnYW5nMi9zdWdhbmc=

GB=5&SUGANG_YEAR=2020&SUGANG_HAKGI=2&GWAMOK_CD=56054&BUNBAN=01&JAESUGANG_YEAR=&JAESUGANG_HAKGI=&JAESUGANG_GWAMOK_CD=&CAMPUS_GB=2&HAKGWA_CD=40017&GWAMOK_GB=&ISU_GB=&GWAMOK_NAME=%EC%82%AC%EC%9D%B4%EB%B2%84%ED%85%8C%EB%9F%AC%EC%99%80%EC%A0%95%EB%B3%B4%EC%A0%84&SEARCH_GUBUN=&GUBUN=INSERT
'''

'''real Delete
POST http://JB/register/major.do?method=proc&UID=7a7a42cc:173db1dc8ac:b3a HTTP/1.1
Host: JB
Connection: keep-alive
Content-Length: 110
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://JB
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://JB/register/result.do?method=list1&UID=7a7a42cc:173db1dc8ac:b3a
Accept-Encoding: gzip, deflate
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: WMONID=zRruntsNImy; NetFunnel_ID=; JSESSIONID=gdKmKtcYyyM8yfnMKCtFW3TC2TQqPhCAcI5T0iOYa6pyAEi1VtJs5pa6sUxS9Kwx.c3VnYW5nMi9zdWdhbmc=

GB=5&SUGANG_YEAR=2020&SUGANG_HAKGI=2&GWAMOK_CD=56054&BUNBAN=01&HAKGWA_CD=&GWAMOK_GB=&ISU_GB=&GUBUN=DELETE&UID=
''' 