# -*- coding:utf-8 -*-
import os
# 列出当前目录下所有的文件
def RenameAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            portion = os.path.splitext(fullname)
            if portion[-1] == ".txt":
                newname = portion[0] + ".patch"
                os.rename(fullname,newname)
                print(newname)

if __name__ == "__main__":
    RenameAllFile('.')
