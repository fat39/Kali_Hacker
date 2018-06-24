from SID转换到用户名 import sid2user
import os

def returnDir():#找到系统回收站目录
    dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):#判断是否为目录
            return recycleDir

def findRecycled(recycleDir):
    dirList = os.listdir(recycleDir)
    for sid in dirList:
        #print(sid)
        files = os.listdir(recycleDir + sid)
        user = sid2user(sid)
        print('罗列用户: ' + str(user) + ' 的文件！')
        for file in files:
            print('找到文件: ' + str(file))

if __name__ == '__main__':
    recycleDir = returnDir()
    #print(recycleDir)
    findRecycled(recycleDir)