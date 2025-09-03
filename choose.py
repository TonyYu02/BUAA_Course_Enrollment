import time
import requests
from bs4 import BeautifulSoup

#这边开始是要填写的
authen = {
    'username': '',
    'password': '',
}

courseList=[
    {'BJDM':'20241-011400-D141061013-1750378896390',
     'lx':'2',
     'skfsdm': "01",  # 02线上上课
     'fromKzwid':'c02d2af43530470fa6c190ef358ea45d',
     }, #工程优化实验
    ]

cour_name = [
        "工程优化实验",
    ]

#以下不要动
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

def get_zwid(file):
    t=get_stamp()
    id_url="https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadFanCourseInfo.do?_="+t+"&pageSize=100"
    zw = get_web(id_url)
    zwj = zw.json()
    for i in zwj["datas"]:
        if "ISKZ" in i :
            if "DXZWID" in i :
                file.write(i["KCLBMC"]+"—"+i["KCMC"]+'\n')
                file.write("DXZWID:"+i["DXZWID"]+'\n')
                file.write("KZWID:"+i["KZWID"]+'\n\n')
            else:
                file.write(i["KCLBMC"] + "—" + i["KCMC"]+'\n')
                file.write("KZWID:" + i["KZWID"]+'\n\n')

def get_csrf():
    indx = "https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkHome/loadPublicInfo_course.do?_="
    rc = get_web(indx + get_stamp())
    rr = rc.json()
    csrf = rr["csrfToken"]
    return csrf

def get_post(k,csrf):
    kc = {
        'bjdm': k['BJDM'],
        'skfsdm': k['skfsdm'],  # 02线上上课
        'lx': k['lx'],
        'csrfToken': csrf,
    }
    if 'fromKzwid' in k and 'fromDxzwid' in k:
        kc['fromKzwid']=k['fromKzwid']
        kc['fromDxzwid']=k['fromDxzwid'],
    elif 'fromKzwid' in k and 'fromDxzwid' not in k:
        kc['fromKzwid']=k['fromKzwid']
    return kc

def query(j,k,csrf):
    xk="https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/choiceCourse.do?_="
    xk = xk + get_stamp()
    kc_data=get_post(k,csrf)
    r = session.post(xk, data=kc_data)
    rj = r.json()
    if rj['msg']=='页面已过期，请刷新页面后重试':
        return "error"
    else:
        print(cour_name[j] + ":" + rj['msg'])
        if (rj['code'] == 1):
            jg_data = {
                'xid': rj["msg"],
                'sfhqdqxkqqs': '1',
            }
            time.sleep(0.5)
            jg_url = "https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadXkjgRes.do?_=" + get_stamp()
            jg = session.post(jg_url, data=jg_data)
            jgj = jg.json()
            print(jgj)
            if (jgj['msg'] == '{"code":1}'):
                print('选课成功。')
            else:
                print("选课失败。")
        return "OK"

def qk(cours, csrf):
    j = 0
    for k in cours:
        a = query(j, k, csrf)
        if a == "OK":
            j += 1
        if a == "error":
            print("界面刷新。")
            return "error"
    time.sleep(0.8)

if __name__ == "__main__":
    csrf=get_csrf()
    i=1
    while True:
        print("第"+str(i)+"次抢课。")
        a=qk(courseList,csrf)
        print("\n")
        if a == "error":
            csrf = get_csrf()
        if i % 50 == 0:
            time.sleep(5)
        i=i+1
