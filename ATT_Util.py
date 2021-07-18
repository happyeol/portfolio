#ATT_Util.py
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup

import pyperclip

def login_input(driver,name,user_input):
    pyperclip.copy(user_input)
    driver.find_element(By.NAME,name).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

def View_Package(driver,model,version):
    try:
        driver.find_element(By.LINK_TEXT,'Search').send_keys(Keys.ENTER)
        driver.find_element(By.LINK_TEXT,'Firmware Search').send_keys(Keys.ENTER)

        driver.find_element(By.NAME,'App__MANU_ID').send_keys(Keys.ENTER)
        select = Select(driver.find_element(By.NAME,'App__MANU_ID'))
        select.select_by_visible_text(text='LG')

        driver.find_element(By.NAME,'App__IMEI_ID').send_keys(Keys.ENTER)
        select = Select(driver.find_element(By.NAME,'App__IMEI_ID'))
        select.select_by_visible_text(text=model)

        driver.find_element(By.NAME,'App__APP_CATEGORY').send_keys(Keys.ENTER)
        select = Select(driver.find_element(By.NAME,'App__APP_CATEGORY'))
        select.select_by_visible_text(text='Firmware')

        pyperclip.copy(version)
        driver.find_element(By.NAME,'App__TARGET_VERSION').click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/center/table/tbody/tr/td/table/tbody/tr/td/form/center/input').send_keys(Keys.ENTER)
    except AttributeError as e:
        print(e)
def Chcek_Package(driver,model,version,Fileinfo_list):
    View_Package(driver,model,version)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    FN_list = soup.select('body > table > tbody > tr > td > table > tbody > tr:nth-child(7) > td > table > tbody > tr > td > center > table > tbody > tr > td > table > tbody > tr > td > form > center:nth-child(4) > table > tbody > tr:nth-child(2) > td > table.mftable > tbody > tr > td:nth-child(2)')

    FN_set = set()
    for filename in FN_list:
        FN_set.add(filename.text)

    Upload_list = []
    for fileinfo in Fileinfo_list:
        if fileinfo[0] in FN_set:
            print(f'{fileinfo[0]} 패키지는 업로드된 상태입니다.')
        else:
            print(f'{fileinfo[0]} 패키지는 업로드가 필요합니다.')
            Upload_list.append(fileinfo)
    return Upload_list

def File_Upload(driver,uploadfile,model):
    try:
        driver.execute_script('window.open("https://xdme.wireless.att.com/jsp/firmware/group_app_add_fw.jsp");') #새탭 추가
        #print(driver.window_handles)
        last_tab = driver.window_handles[-1]
        driver.switch_to.window(window_name=last_tab) #새탭으로 이동
        #패키지 업로드 수행
        driver.find_element(By.NAME,'GROUP_ID').send_keys(Keys.ENTER)
        select = Select(driver.find_element(By.NAME, 'GROUP_ID'))
        select.select_by_visible_text(text='ATT.LG')

        driver.find_element(By.NAME,'MANU_ID').send_keys(Keys.ENTER)
        select = Select(driver.find_element(By.NAME, 'MANU_ID'))
        select.select_by_visible_text(text='LG')

        driver.find_element(By.NAME,'IMEI_ID').send_keys(Keys.ENTER)
        select = Select(driver.find_element(By.NAME, 'IMEI_ID'))
        select.select_by_visible_text(text=model)

        driver.find_element(By.NAME, 'APP_CATEGORY_ID').send_keys(Keys.ENTER)
        select = Select(driver.find_element(By.NAME, 'APP_CATEGORY_ID'))
        select.select_by_visible_text(text='Firmware')

        pyperclip.copy(uploadfile[0])
        driver.find_element(By.NAME,'APP_NAME').click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        upload = driver.find_element(By.CSS_SELECTOR,'body > table > tbody > tr > td > table > tbody > tr:nth-child(7) > td > table > tbody > tr > td > center > table > tbody > tr > td > table > tbody > tr > td > center > form > table > tbody > tr:nth-child(7) > td:nth-child(2) > input')
        upload.send_keys('C:\ATT_Files\\'+uploadfile[0])

        Temp_list = uploadfile[0].split('.')
        temp_str = Temp_list[0]
        FN_Split = temp_str.split('-')
        if len(FN_Split) == 2:
            if FN_Split[1] == 'Corrupt':
                source = FN_Split[0]
                target = FN_Split[0]+'-'+FN_Split[1]
            else:
                source = FN_Split[0]
                target = FN_Split[1]
        elif len(FN_Split) == 3:
            if FN_Split[1] == 'SVN':
                source = FN_Split[0]+'-'+FN_Split[1]
                target = FN_Split[2]
            else:
                source = FN_Split[0]
                target = FN_Split[1]+'-'+FN_Split[2]

        pyperclip.copy(source)
        driver.find_element(By.NAME,'SOURCE_VERSION').click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        pyperclip.copy(target)
        driver.find_element(By.NAME,'TARGET_VERSION').click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        driver.find_element(By.NAME,'APP_SEVERITY').send_keys(Keys.ENTER)
        select = Select(driver.find_element(By.NAME,'APP_SEVERITY'))
        select.select_by_visible_text(text=uploadfile[1])

        Upgrade = uploadfile[2]
        if Upgrade == 'Upgrade':
            driver.find_element(By.CSS_SELECTOR,'body > table > tbody > tr > td > table > tbody > tr:nth-child(7) > td > table > tbody > tr > td > center > table > tbody > tr > td > table > tbody > tr > td > center > form > table > tbody > tr:nth-child(17) > td:nth-child(1) > input').click()
        elif Upgrade == 'Downgrade':
            driver.find_element(By.CSS_SELECTOR,'body > table > tbody > tr > td > table > tbody > tr:nth-child(7) > td > table > tbody > tr > td > center > table > tbody > tr > td > table > tbody > tr > td > center > form > table > tbody > tr:nth-child(17) > td:nth-child(2) > input').click()

        driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/center/table/tbody/tr/td/table/tbody/tr/td/center/form/input[7]').send_keys(Keys.ENTER)
    except:
        print("File_Upload:패키지 업로드 중에 문제가 발생했습니다.")

def Upload_Package(driver,model,version,Upload_list):
    try:
        Failed_list = []
        for uploadfile in Upload_list:
            File_Upload(driver,uploadfile,model) #패키지 업로드

            #업로드가 정상적으로 되었는 지 확인 후 첫번째 탭을 제외한 모든 탭 닫기
            driver.execute_script('window.open("https://xdme.wireless.att.com/jsp/firmware/group_app_search_result_fw.jsp");')  #새탭 추가
            last_tab = driver.window_handles[-1]
            driver.switch_to.window(window_name=last_tab)  #새탭으로 이동

            View_Package(driver,model,version)

            soup = BeautifulSoup(driver.page_source,'html.parser')

            FN_list = soup.select('body > table > tbody > tr > td > table > tbody > tr:nth-child(7) > td > table > tbody > tr > td > center > table > tbody > tr > td > table > tbody > tr > td > form > center:nth-child(4) > table > tbody > tr:nth-child(2) > td > table.mftable > tbody > tr > td:nth-child(2)')

            FN_set = set()
            for filename in FN_list:
                FN_set.add(filename.text)

            if uploadfile[0] in FN_set:
                driver.close()
                second_tab = driver.window_handles[1]
                driver.switch_to.window(window_name=second_tab)

                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(window_name=first_tab)
            else: #패키지 업로드 실패한 경우
                Failed_list = uploadfile

                driver.close()
                second_tab = driver.window_handles[1]
                driver.switch_to.window(window_name=second_tab)

                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(window_name=first_tab)
                continue
        return Failed_list
    except:
        print("Upload_Package:패키지 업로드 중에 문제가 발생했습니다.")