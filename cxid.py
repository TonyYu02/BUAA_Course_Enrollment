from choose import get_zwid

if __name__=="__main__":
    with open("id.txt", "w") as file:
        get_zwid(file)
    print("课组id获取完毕，输出为目录下id.txt文件。")