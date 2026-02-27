## BUAA抢课
#### 这学期选课结束啦，第一次写抢课代码，摸索了好久，还好抢课系统和不少学校用的个一样的hhh，亲测可用，希望下次能帮到大家咯，明年见~

正在陆续更新以下功能
- [x] 基础选课，主要是post的data数据结构
- [x] 在两处登录如何自动刷新
- [x] 获取课组id，输出为id.txt
- [ ] 自动获取课程信息功能
- [ ] 其他

### 使用方法
1. 填写学号、密码，运行`cxid.py`  
2. 填写所选课程所需的信息，主要是
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

   'fromKzwid'和'fromDxzwid'从id.txt获取
   ```
   另外需要填写课程的名称，方便输出

4. 运行即可

### 开课信息查询
直接loadcourse全输出就行：`https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadAllCourseInfo.do?_=timestamp&pageSize=8000`，会输出所有开课信息，BJDM可从中获取。

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
