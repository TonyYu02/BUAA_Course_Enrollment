import time
import requests
from bs4 import BeautifulSoup

###################### 填写待查询的课程名称 ################
chaxun={
    "材料智能基础与AI科研方法",
    "无机合成化学"
}


###################### 以下不要动 ################
def read_account_info(file_path="account.txt"):
    authen = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "：" in line:
                key, value = line.split("：", 1)
            elif ":" in line:
                key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "账号": authen["username"] = value
            elif key == "密码": authen["password"] = value
    return authen

authen = read_account_info("account.txt")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
}

session = requests.Session()

def get_stamp():
    return str(int(time.time() * 1000))

def get_web(url):
    try:
        page =session.get(url, headers=headers, timeout=15)
        return page
    except requests.exceptions.Timeout:
        print("界面超时，请重试。")
        exit(0)

login_page = get_web("https://sso.buaa.edu.cn/login?service=https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/*default/index.do")
soup = BeautifulSoup(login_page.text, 'html.parser')
execution_input = soup.find('input', {'name': 'execution'})
execution_value = execution_input.get('value', '')

login_data = {
    'username': authen['username'],
    'password': authen['password'],
    'type': 'username_password',
    'submit': 'LOGIN',
    '_eventId': 'submit',
    'execution': execution_value
}

r = session.post("https://sso.buaa.edu.cn/login", data=login_data)

c_url="https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadAllCourseInfo.do?_="+get_stamp()+"&pageSize=10000"
jg = session.post(c_url)
jgj = jg.json()
print("lx（课程类型）和skfsdm（上课方式代码）请参考README填写！\n")
for mc in chaxun:
    for cinfo in jgj["datas"]:
        if "KCMC" in cinfo and cinfo["KCMC"] == mc:
            print("课程名称："+cinfo["KCMC"])
            print("BJDM：" + cinfo["BJDM"])
            print("\n")