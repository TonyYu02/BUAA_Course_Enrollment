import time
import requests
from bs4 import BeautifulSoup

authen = {
    'username': '',
    'password': '',
}

courseList=[
	{'BJDM':'20251-014100-T411041003-1753879498897',
	 'lx':'2',
	 'fromKzwid':'d4cb37030bc24378b67304064e00c948',
	 'fromDxzwid':'3650EDADF723DD8DE0630211FE0AE544'}, 
	#强化学习 2-9周 星期一[6-7节]A212;10-16周 星期一[6-7节]A212;17周 星期一[6-7节]A212
    ]

'''
关于lx
lx:0,title:plannedCourses，计划内课程
lx:1,publicElectiveCourses，任选课
lx:2,programCourses，培养方案内课程
lx:5,retakeCourses，重修课
lx:20,undergraduateCourse，本科课程
lx:4,haveCourses，已选课，不管
lx:99,openedCourses，开设课程，不管
lx:101,导师审核信息，不管
'''
cour_name = [
        "强化学习",
    ]

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

def get_csrf():
    indx = "https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkHome/loadPublicInfo_course.do?_="
    rc = get_web(indx + get_stamp())
    rr = rc.json()
    csrf = rr["csrfToken"]
    return csrf

def query(j,k,csrf):
    xk="https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/choiceCourse.do?_="
    xk = xk + get_stamp()
    kc_data={
        'bjdm': k['BJDM'],
        'skfsdm': "01", #02线上上课
        'lx': k['lx'],
        'csrfToken': csrf,
    }
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
            jg_url = "https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadXkjgRes.do?_=" + get_stamp()
            jg = session.post(jg_url, data=jg_data)
            jgj = jg.json()
            if (jgj['dqxkqqs'] == 1):
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
