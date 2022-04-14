from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import requests
from bs4 import BeautifulSoup

import time
import pyperclip
import re
import paramiko
import os
#import pyautogui

#size = pyautogui.size()
#print(size)

def input_account_info(driver,xpath,user_info):
    pyperclip.copy(user_info)
    driver.find_element(By.XPATH, xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')

browser = webdriver.Chrome('chromedriver', options=options)

# LGEP 로그인
# sso.lge.com 접속
browser.get(url='https://sso.lge.com/')
time.sleep(3)

# LGEP 계정 정보
user_id = 'seyeol.park'
user_id_xpath = '//*[@id="USER"]'
user_password = 'Sweethome1179!'
user_password_xpath = '//*[@id="LDAPPASSWORD"]'
opt_password_xpath = '//*[@id="OTPPASSWORD"]'

# SFTP 주소 및 계정
host = '136.166.4.58' # 접속할 서버 주소
userid = 'seyeol.park'
password = 'Sweethome1179!'

# LGEP 로그인 수행
input_account_info(browser, user_id_xpath, user_id)
input_account_info(browser, user_password_xpath, user_password)
otp_password = input("Input OTP PASSWORD: ")
input_account_info(browser, opt_password_xpath, otp_password)
browser.find_element(By.XPATH, '//*[@id="loginSsobtn"]').send_keys(Keys.ENTER)
time.sleep(5)

# WWFOTA 패키지등록 사이트 접속
browser.execute_script('window.open("http://mlm.lge.com/di/issues/?jql=project%20%3D%20WWFOTA");')
time.sleep(10)
last_tab = browser.window_handles[-1]
browser.switch_to.window(window_name=last_tab) #새탭으로 이동
browser.find_element(By.XPATH, '//*[@id="user-options"]/a').send_keys(Keys.ENTER)
time.sleep(10)

# 패키지등록요청 목록에서 HTML 소스 가져오기
soup_index = BeautifulSoup(browser.page_source, 'html.parser')

# Status 조회
status = soup_index.find('table', {'id':'issuetable'}).find('td', {'class':'status'})
status_text = status.find('span').text

# 파싱에 필요한 리스트 생성
info_td = []
info_span = []
info_p = []
info_a = []
info_all = []
removed_blank = []

# 요청정보
model_name = None
paths = []
imei = []

# Status가 Open 또는 Reopened 인 경우에만 요청 처리
if status_text == 'OPEN' or 'REOPENED' or 'RESOLVED': # 차후 RESOLVED 상태는 제거 예정
    # Key 조회
    key_all = soup_index.find('table', {'id': 'issuetable'}).find('td', {'class': 'issuekey'})
    key = key_all.find('a', {'class': 'issue-link'}).text
    # Summary 조회
    summary_all = soup_index.find('table', {'id':'issuetable'}).find('td', {'class':'summary'})
    summary = summary_all.find('a', {'class':'issue-link'}).text
    # 사업자 구분
    p_carrier = re.compile('ATT|AT&T|Cricket|GOTA|Gota|gota|VZW|VRZ')
    m_carrier = p_carrier.search(summary) # summary 내용 중에 사업자명 찾기
    if m_carrier:
        if m_carrier.group().upper() == 'AT&T':
           package_type = 'ATT'
        package_type = m_carrier.group().upper()
    else:
        package_type = 'LGFOTA'
    # 리스트 초기화 : 다음 요청을 처리할 경우를 위해
    info_td.clear()
    info_span.clear()
    info_p.clear()
    info_a.clear()
    # 패키지 등록 요청 페이지 진입
    browser.find_element(By.LINK_TEXT, key).click() # 가끔 summary 값에 엉뚱한 값이 포함되는 경우가 있어 key 값을 사용하여 링크 클릭
    time.sleep(5)
    # 요청 테이블 파싱
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    mlm_title = soup.select_one('#summary-val').text
    table = soup.find('div', {'id': 'description-val'}).find('tbody') # tbody 확인
    td_all = table.find_all('td') # tbody > td 확인
    for td in td_all:
        info_td.append(td.text) # td 태그에 있는 text 모두 리스트에 추가
        span_all = td.find_all('span') # tbody > td > span 확인
        p_all = td.find_all('p') # tbody > td > p 확인
        a_all = td.find_all('a') # tbody > td > a 확인
        if span_all: # tbody > td > span 태그가 있다면
            for span in span_all:
                info_span.append(span.text)# span 태그에 있는 text 모두 리스트에 추가
        if p_all: # tbody > td > p 태그가 있다면
            for p in p_all:
                info_p.append(p.text) # p 태그에 있는 text 모두 리스트에 추가
        if a_all: # tbody > td > a 태그가 있다면
            for a in a_all:
                info_a.append(a.text) # a 태그에 있는 text 모두 리스트에 추가
    # 리스트 공백 및 중복 제거
    info_all = info_td + info_span + info_p + info_a
    p_boundary = re.compile('^ +$') # 빈 문자열 패턴
    p_nbsp = re.compile('&nbsp;') # &nbsp; 포함된 문자열 패턴
    for info in info_all:
        info = p_boundary.sub('', info) # 빈 문자열을 None으로 만듬
        if info: # 빈 문자열을 필터링 함
            info = p_nbsp.sub('', info) # &nbsp; 포함된 문자열을 None으로 만듬
            if info: # &nbsp; 포함된 문자열을 필터링 함
                removed_blank.append(" ".join(info.split())) # 문자열 사이에 있는 공백을 제거하여 removed_blank 리스트에 넣음
    info_all = list(set(removed_blank)) # removed_blank 리스트에서 중복되는 원소를 제거하여 info_all 리스트에 넘겨줌
    # for info in info_all:
        # print(info)
    # 요청정보 수집에 사용하는 변수
    m_modelname = None
    # 패턴
    # LGFOTA 요청 타입
    p_test_type = re.compile('IOT|FUT') # 사업자 테스트용 패키지명 구분에 사용하는 패턴
    m_test_type = p_test_type.search(summary)
    if m_test_type: # 사업자 테스트용 패키지의 경우
        test_type = m_test_type.group()
    else: # 내부 테스트용 패키지의 경우
        test_type = 'INTERNAL'
    # 모델명
    if package_type == 'GOTA': # GOTA 패키지의 경우
        p_modelname = re.compile(r'[A-Z]-\d{2}[A-Z]+|[A-Z]\d{3}[A-Z]+')
    elif package_type == 'LGFOTA': # LGFOTA 패키지의 경우
        if test_type == 'IOT': # IOT 패키지의 경우 아래 모델명 사용
            p_modelname = re.compile(r'IOT_LM-[A-Z]\d{3}[A-Z\d]+')
        elif test_type == 'FUT': # FUT 패키지의 경우 아래 모델명 사용
            p_modelname = re.compile(r'IOT_FUT_LM-[A-Z]\d{3}[A-Z\d]+')
        else: # 내부 테스트 패키지의 경우 아래 모델명 사용
            p_modelname = re.compile('TEST-MODEL')
    else: # VZW, ATT 패키지의 경우 아래 모델명 사용
        p_modelname = re.compile(r'[A-Z]\d{3}[A-Z]+')
    # 경로
    p1_path = re.compile(r'^\\\\')
    p2_path = re.compile('/ftp')
    if package_type == 'VZW' or 'VRZ': # VZW 패키지의 경우
        if p1_path: # 경로명이 \\로 시작한다면(우선순위 높음)
            p3_path = re.compile(r'\\[a-z]{3}$|/[a-z]{3}$', re.I) # 경로명 패턴으로 UPC를 사용
        elif p2_path: # 경로명에 /ftp가 포함되어 있다면(우선순위 낮음)
            p3_path = re.compile(r'\\FOTA$|/FOTA$|\\UPC$|/UPC$') # 경로명 패턴으로 FOTA를 사용
        else:
            print("경로명 패턴과 일치하는 문자열이 없습니다.")
    p4_path = re.compile('path *: *|Paths *: *')
    # imei
    p_imei = re.compile(r'\d{15}')
    # 요청정보 수집
    info_splited = []
    for info in info_all: # 리스트에서 원소 1개를 가져와
        # 모델명
        if m_modelname == None: # 아직까지는 모델명 패턴과 일치하는 원소가 없었다면
            if p_modelname.search(info): # 해당 원소가 모델명 패턴과 일치한다면
                m_modelname = p_modelname.search(info)
                model_name = m_modelname.group()
        # 경로명
        if p3_path.search(info): # 해당 원소가 경로명 패턴과 일치한다면
            if p4_path.search(info):
                info_splited = info.split(':')
                info_splited = info_splited[1:]
                for info_s in info_splited:
                    paths.append(info_s.strip())
            else:
               paths.append(info)
        # imei
        if p_imei.search(info): # 해당 원소가 imei 패턴과 일치한다면
            m_imei = p_imei.search(info)
            if m_imei:
                imei.append(m_imei.group())
    # print(model_name)
    # for p in path:
        # print(p)
    # for i in imei:
        # print(i)
    # 사업자 별 자동화 테스트 수행
    if package_type == 'ATT' or 'CRICKET':
        pass
    elif package_type == 'VZW' or 'VRZ':
        # path 리스트에 있는 경로에 접근하여 파일을 로컬로 다운로드
        if os.path.exists('C:\ATT_Files'):
            os.chdir('C:\ATT_Files')
            if not os.path.exists(os.path.join(os.getcwd(), model_name)):
                os.mkdir(model_name)
            else:
                print("이미 존재하는 경로입니다.")

        localpath = os.path.join(os.getcwd(), model_name)
        remote_files = []
        local_files = []

        transport = paramiko.transport.Transport(host)
        transport.connect(username=userid, password=password)  # connect 함수를 사용하여 사용자 계정을 추가
        sftp = paramiko.SFTPClient.from_transport(transport)  # sftp 객체 생성

        for remotepath in paths:
            sftp.chdir(remotepath)  # 서버 경로를 전달하여 접속
            files = sftp.listdir()  # 해당 경로에 있는 파일명 조회
            if files:  # remote
                for f in files:
                    remote_files.append(remotepath + '/' + f)
            for f in files:  # local
                local_files.append((localpath + '/' + f))

            # 서버에 있는 패키지 파일을 로컬로 다운로드
            for idx in range(len(files)):
                sftp.get(remote_files[idx], local_files[idx])

        sftp.close()
        transport.close()

    elif package_type == 'GOTA':
        pass
    elif package_type == 'LGFOTA':
        pass
        # iframes = browser.find_element(By.CSS_SELECTOR, 'iframe')
        # for iframe in iframes:
        #     print(iframe.get_attribute('name'))
        # soup_gota = BeautifulSoup(browser.page_source, 'html.parser')
        # browser.switch_to.frame('iframeResult')
        # mlm title, 모델명, 패키지 경로, 패키지 버전명, imei, group name
        # mlm_title = soup_gota.select_one('body > table > tbody > tr:nth-child(1) > td.x167').text
        # print(mlm_title)