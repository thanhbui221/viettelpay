import os 
import sys
import time
import requests
import random
from threading import Thread

class Client:
    def genMachineAddress():
        x = [chr(i) for i in range(ord("a"), ord("z")+1)] + [str(i) for i in range(10)]
        s = ""
        for i in range(8):
            s += random.choice(x)
        s += '-'
        for i in range(4):
            s += random.choice(x)
        s += '-'
        for i in range(4):
            s += random.choice(x)
        s += '-'
        for i in range(4):
            s += random.choice(x)
        s += '-'
        for i in range(12):
            s += random.choice(x)
        return s

class ViettelMoney:
    waitTime = 30
    shortTime = 0.5
    def __init__(self, imei, username, pin, proxy=False):
        self.imei = imei
        self.username = username
        self.proxy = proxy
        self.pin = pin

    def getValidate(self):
        headers = {
            'Host': 'api8.viettelpay.vn',
            'Accept': '*/*',
            'app_version': '5.0.4',
            'Product': 'VIETTELPAY',
            'type_os': 'ios',
            'Accept-Language': 'vi',
            'imei': self.imei,
            'Content-Length': '42',
            'User-Agent': 'Viettel Money/5.0.4 (com.viettel.viettelpay; build:1; iOS 15.2.0) Alamofire/5.0.4',
            'Connection': 'keep-alive',
            'os_version': '15.2',
            'Authority-Party': 'APP',
            'Content-Type': 'application/json',
        }
        data = '{"type":"msisdn","username":"'+self.username+'"}'

        s = requests.session()
        if self.proxy:
            s.proxies.update(self.proxy)

        s_time = time.time()
        while True:
            if time.time() - s_time > ViettelMoney.waitTime:
                raise Exception("Time limit exceeded: getValidate")
            try:
                res = s.post('https://api8.viettelpay.vn/customer/v1/validate/account', headers=headers, data=data)
                return res.json()
            except:
                pass
            time.sleep(ViettelMoney.shortTime)

    def login(self):
        headers = {
            'Host': 'api8.viettelpay.vn',
            'Accept': '*/*',
            'Product': 'VIETTELPAY',
            'app_version': '5.0.4',
            'type_os': 'ios',
            'Accept-Language': 'vi',
            'imei': self.imei,
            'Content-Length': '345',
            'User-Agent': 'Viettel Money/5.0.4 (com.viettel.viettelpay; build:1; iOS 15.2.0) Alamofire/5.0.4',
            'Connection': 'keep-alive',
            'os_version': '15.2',
            'Authority-Party': 'APP',
            'Content-Type': 'application/json',
        }
        data = '{"imei":"'+self.imei+'","pin":"'+self.pin+'","msisdn":"'+self.username+'","typeOs":"iOS","loginType":"BASIC","userType":"msisdn","username":"'+self.username+'"}'

        s = requests.session()
        if self.proxy:
            s.proxies.update(self.proxy)

        s_time = time.time()
        while True:
            if time.time() - s_time > ViettelMoney.waitTime:
                raise Exception("Time limit exceeded: login")
            try:
                res = s.post('https://api8.viettelpay.vn/auth/v1/authn/login', headers=headers, data=data)
                return res.json()
            except:
                pass
            time.sleep(ViettelMoney.shortTime)

    def loginOtp(self, otp, requestId):
        headers = {
            'Host': 'api8.viettelpay.vn',
            'Accept': '*/*',
            'Product': 'VIETTELPAY',
            'app_version': '5.0.4',
            'type_os': 'ios',
            'Accept-Language': 'vi',
            'imei': self.imei,
            'Content-Length': '409',
            'User-Agent': 'Viettel Money/5.0.4 (com.viettel.viettelpay; build:1; iOS 15.2.0) Alamofire/5.0.4',
            'Connection': 'keep-alive',
            'os_version': '15.2',
            'Authority-Party': 'APP',
            'Content-Type': 'application/json',
        }

        data = '{"loginType":"BASIC","otp":"'+otp+'","imei":"'+self.imei+'","pin":"'+self.pin+'","msisdn":"'+self.username+'","username":"'+self.username+'","userType":"msisdn","requestId":"'+requestId+'","typeOs":"iOS"}'

        s = requests.session()
        if self.proxy:
            s.proxies.update(self.proxy)

        s_time = time.time()
        while True:
            if time.time() - s_time > ViettelMoney.waitTime:
                raise Exception("Time limit exceeded: loginOtp")
            try:
                res = s.post('https://api8.viettelpay.vn/auth/v1/authn/login', headers=headers, data=data)
                return res.json()
            except:
                pass
            time.sleep(ViettelMoney.shortTime)

    def getAccounts(self):
        headers = {
            'Host': 'api8.viettelpay.vn',
            'Authorization': f'Bearer {self.loginResponse["data"]["accessToken"]}',
            'Accept': '*/*',
            'Product': 'VIETTELPAY',
            'app_version': '5.0.4',
            'type_os': 'ios',
            'Accept-Language': 'vi',
            'imei': self.imei,
            'User-Agent': 'Viettel Money/5.0.4 (com.viettel.viettelpay; build:1; iOS 15.2.0) Alamofire/5.0.4',
            'Connection': 'keep-alive',
            'os_version': '15.2',
            'Authority-Party': 'APP',
            'Content-Type': 'application/json',
        }

        params = (
            ('home-version', '2.0'),
            ('recommendations', '1'),
            ('sources', '1'),
        )

        s = requests.session()
        if self.proxy:
            s.proxies.update(self.proxy)

        s_time = time.time()
        while True:
            if time.time() - s_time > ViettelMoney.waitTime:
                raise Exception("Time limit exceeded: getAccounts")
            try:
                res = s.get('https://api8.viettelpay.vn/customer/v1/accounts', headers=headers, params=params)
                return res.json()
            except:
                pass
            time.sleep(ViettelMoney.shortTime)

    def getAccountRank(self):
        headers = {
            'Host': 'api8.viettelpay.vn',
            'Channel': 'APP',
            'Authorization': f'Bearer {self.loginResponse["data"]["accessToken"]}',
            'User-Id': self.username,
            'Accept-Language': 'vi',
            'Accept': '*/*',
            'User-Agent': 'Viettel Money/5.0.4 (iPhone; iOS 15.2; Scale/3.00)',
            'Connection': 'keep-alive',
        }

        params = (
            ('msisdn', self.username),
        )

        s = requests.session()
        if self.proxy:
            s.proxies.update(self.proxy)

        s_time = time.time()
        while True:
            if time.time() - s_time > ViettelMoney.waitTime:
                raise Exception("Time limit exceeded: getAccountRank")
            try:
                res = s.get('https://api8.viettelpay.vn/loyalty/mobile/v2/accounts/get-account-rank', headers=headers, params=params)
                return res.json()
            except:
                pass
            time.sleep(ViettelMoney.shortTime)

    def getTotalPoint(self):
        headers = {
            'Host': 'api8.viettelpay.vn',
            'Channel': 'APP',
            'Authorization': f'Bearer {self.loginResponse["data"]["accessToken"]}',
            'User-Id': self.username,
            'Accept-Language': 'vi;q=1.0',
            'Accept': '*/*',
            'User-Agent': 'Viettel Money/5.0.4 (com.viettel.viettelpay; build:1; iOS 15.2.0) Alamofire/5.0.4',
            'Connection': 'keep-alive',
        }

        params = (
            ('isLastExpireDate', '0'),
            ('msisdn', self.username),
        )

        s = requests.session()
        if self.proxy:
            s.proxies.update(self.proxy)

        s_time = time.time()
        while True:
            if time.time() - s_time > ViettelMoney.waitTime:
                raise Exception("Time limit exceeded: getTotalPoint")
            try:
                res = s.get('https://api8.viettelpay.vn/loyalty/mobile/v1/point/total', headers=headers, params=params)
                return res.json()
            except:
                pass
            time.sleep(ViettelMoney.shortTime)
            
    def getBalance():
        #có vẻ như endpoint là bankplus.vn
        #nhưng thấy mỗi post request, không thấy get request,
        #khá là lạ
        #cái post request là một soap-env, dc encrypted rất phức tạp,
        #muốn đọc cái bên trong mà chưa bik decrypt kiểu gì


if __name__ == "__main__":
    # input_username = input("Input phone number")
    input_pin = input("input pin: ")
    
    a = ViettelMoney(
            imei = Client.genMachineAddress().upper(),
            # username = "84984924712", sdt Tung
            username = "0363501035", # sdt minh
            pin = input_pin
        )

    res = a.getValidate()
    print(res)

    res = a.login()
    print(res)

    if res['status']['code'] == "AUT0014":
        otp = input(f"Input Otp {a.username}: ")
        res = a.loginOtp(
                otp = otp,
                requestId = res['data']['requestId']
            )
        print(res)

    if res['status']['code'] != "00":
        raise Exception("Login failed")

    a.loginResponse = res

    res = a.getAccounts()
    print(res)

    res = a.getAccountRank()
    print(res)

    res = a.getTotalPoint()
    print(res)