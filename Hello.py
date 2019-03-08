from threading import Thread,Lock
import random
import linecache

def task(filename):
    mutex.acquire()  # 上锁
    phone = get_phone(filename)  # 获取手机号
    print('中奖手机号是： %s' % (phone,))
    mutex.release()  # 释放锁

def get_phone(filename):
    '''获取手机号'''
    linecache.updatecache(filename)#更新文件名为filename的缓存。如果filename文件更新了，使用这个函数可以更新linecache.getlines(filename)返回的列表
    count = len(linecache.getlines(filename))#获取不包括最后的空行
    print("此次共有",count,"人参加抽奖")
    num = random.randint(1, count)
    phone = linecache.getline(filename,num)
    removeLine(filename, num-1)
    return phone

def removeLine(filename, lineno):
    '''
    删除文件中的指定行
    :param filename: 文件名
    :param lineno: 行号
    :return:
    '''
    fro = open(filename, "r",encoding='UTF-8')
    current_line = 0
    while current_line < lineno:
        fro.readline()
        current_line += 1

    seekpoint = fro.tell()
    frw = open(filename, "r+")
    frw.seek(seekpoint, 0)

    # read the line we want to discard
    fro.readline()  # 读入一行进内存 ，同时 文件指针下移实现删除

    # now move the rest of the lines in the file
    # one line back
    chars = fro.readline()
    while chars:
        frw.writelines(chars)
        chars = fro.readline()
    fro.close()
    frw.truncate()
    frw.close()

if __name__ == "__main__":
    filename = 'phone.txt'
    mutex = Lock() # 设置锁
    t_l = []
    for i in range(3):
        t = Thread(target=task,args=(filename,)) # 创建线程
        t_l.append(t) # 写入列表
        t.start()     # 开启线程
    for t in t_l:
        t.join()   # 等待子线程结束