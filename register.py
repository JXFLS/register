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

class register:

    op = webdriver.Chrome()
    URL = 'http://172.16.254.82/selfLogon.do'
    num = '0000'
    wait = WebDriverWait(op, 10)
    name = "JXJJZX"
    valiable = list()
    end = 240
    way = int()

    def nxt(self, num):
        """得到下一个编号"""
        res = int(num) + 1
        res = str(res)
        while len(res) < 4:
            res = '0' + res
        return res

    def __init__(self, _name, _num=1, _end=240, _way=0):
        """初始化函数
        
        name 表示前缀

        num 表示开始的帐号

        end 表示结束的帐号

        如果 way = 0，则会遍历 [num, end] 中的所有帐号
        否则会遍历出现在 result.txt 中的且在 [num, end] 中的帐号
        如果没有 result.txt 则会以 way = 0 处理

        """
        self.name = _name
        self.num = self.nxt(_num - 1)
        self.end = _end
        self.way = _way

    def get_captcha(self):
        """模拟验证码
        
        利用 pyautogui + selenium.ActionChains 模拟下载验证码图片
        耗时 1.6 s 左右，急需优化

        """
        act = ActionChains(self.op)
        act.reset_actions()
        os.system("rm ~/Downloads/AuthenCodeImage*")
        print("getting captcha")
        img = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"img[src=\"/servlet/AuthenCodeImage\"]")))
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

    def login(self, num):
        """模拟登录"""
        self.op.find_element_by_name("user_id").send_keys(self.name + num)
        self.op.find_element_by_name("passwd").send_keys("123456")
        self.op.find_element_by_name("validateCode").send_keys(self.get_captcha())

    def work(self, num):
        try:
            self.op.get(self.URL)
        except:
            self.op.get(self.URL)
        print("work " + str(num))
        self.login(num)
        tmpqwq = 1
        not_ok = int()
        """尝试验证码与密码"""
        while 1:
            try:
                tmp = self.wait.until(EC.presence_of_element_located((By.NAME, "mainFrame")))
            except:
                print("wrong")
                self.login(num)
            else:
                break
            finally:
                tmpqwq += 1
                if tmpqwq == 3:
                    not_ok = 1
                    break
        if not_ok == 1: return 
        self.op.switch_to.frame(tmp)
        """获取到期时间"""
        tmp = self.op.find_elements(By.CSS_SELECTOR, "td[bgcolor=\"FFFFFF\"][align=\"center\"]")
        have_been = int()
        is_ok = int()

        def pd(s):
            res = int()
            for i in s:
                if i == ':': res += 1
            return res == 2

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
                    if (year > nyear 
                        or (year == nyear and month > nmonth) 
                        or (year == nyear and month == nmonth and day > nday
                    )):
                        is_ok = True
                    else: is_ok = False
        print(is_ok)
        time.sleep(0.5)
        """判断 MAC 地址"""
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "绑定信息"))).click()
        time.sleep(0.5)
        ele = self.op.find_elements(By.CSS_SELECTOR, "[bgcolor=\"DAE1EF\"]+td")
        ans = int()
        for e in ele:
            _str = e.text
            for s in _str:
                if s == ':': ans += 1
        print(str(num) + " = " + str(ans))
        if ans < 15 and is_ok:
            print("True")
            return True
        else:
            return False    
        print(str(num) + " = " + str(ans))

    def mainFuc(self):
        """如果不存在 result.txt 或者 way = 0"""
        if self.way == 0 or not os.path.exists("result.txt"):
            if os.path.exists("result.txt"): os.remove("result.txt")
            while 1:
                if self.work(self.num):
                    with open("result.txt", 'a') as out:
                        out.write(str(self.num) + '\n')
                if int(self.num) > self.end: break
                self.num = self.nxt(self.num)
        else:
            with open("result.txt", 'r') as out:
                for line in out.readlines():
                    if not len(line) or int(self.num) > int(line) or int(line) > int(self.end): continue
                    self.valiable.append(line)
            os.remove("result.txt")
            for now in self.valiable:
                if self.work(now):
                    with open("result.txt", 'a') as out:
                        out.write(now + '\n')
                self.num = self.nxt(self.num)
        self.op.quit()