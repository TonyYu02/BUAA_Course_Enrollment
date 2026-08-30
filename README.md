## BUAA抢课

建议配合[预选课](https://github.com/TonyYu02/BUAA_For_Pre-selected_Course_Enrollment)使用

正在陆续更新以下功能
- [x] 基础选课，主要是post的data数据结构
- [x] 在两处登录如何自动刷新
- [x] 获取课组id，输出为id.txt
- [x] 获取课程信息（BJDM）功能
- [ ] 其他

### 各个文件的说明
| 文件名 | 说明 |
|---|---|
| `account.txt` | 储存账号和密码信息的文本文件 |
| `choose.py` | 选课主程序 |
| `cxid.py` | 获取课组 ID 的程序 |
| `search.py` | 按照课程名称获取 BJDM 的程序 |

### 使用方法
0. 如果有需要可以先使用`search.py`获取对应课程的BJDM，只需要填写所需要查询课程的名称（如下例所示），会输出名称、任课教师、上课时间（如果有）和BJDM   
	```
	chaxun={
    "材料智能基础与AI科研方法",
    "无机合成化学"
	}
	```
1. 在`account.txt`文件中填写学号、密码，运行`cxid.py`，获得课组信息id.txt  
2. 在`choose.txt`填写所选课程所需的信息，主要是
   ```
   'BJDM':'',#课程的代码
   'lx':'',#类型
   'skfsdm': "",  # 01线下上课，02线上上课
   'fromKzwid':'', #课组wid
   'fromDxzwid':'', #不知道是啥id的简称
   ```
   其中：
   ```
   lx:0,title:plannedCourses，计划内课程
   lx:1,publicElectiveCourses，任选课
   lx:2,programCourses，培养方案内课程
   lx:5,retakeCourses，重修课
   lx:20,undergraduateCourse，本科课程
   lx:4,haveCourses，已选课，不管
   lx:99,openedCourses，开设课程，不管
   lx:101,导师审核信息，不管

   'fromKzwid'和'fromDxzwid'从id.txt获取，如果该课程不是课组里面的，就不需要添加课组信息
   ```
   另外需要填写课程的名称，方便输出

4. 运行即可

### 开课信息查询
直接loadcourse即可：`https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadAllCourseInfo.do?_=timestamp&pageSize=8000`，会输出所有开课信息，BJDM可从中获取。（已添加查询文件）

### 关于退课
退课的逻辑相对比较简单，主要是post一个退课请求，数据是bjdm和csrfToken，例如：  
```
ca="https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/cancelCourse.do?_=" + get_stamp()
ca_data = {
   'bjdm': "xxxxxxxxxxxxxxxxx",
   'csrfToken': csrf,
 }
cca = session.post(ca, data=ca_data)
camsg=cca.json()
print(camsg['msg'])
```

### 参考
[fdu_course_enrollment](https://github.com/JarynWong/fdu_course_enrollment)  
[BIT-CourseRace](https://github.com/Jump-Wang-111/BIT-CourseRace)
