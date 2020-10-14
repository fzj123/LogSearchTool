import mmap
import contextlib
import re


def logFind(file_path, search_word):

    f = open(file_path, 'r')
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
        while True:
            line = m.readline().strip()
            if line.find(search_word.encode()) >= 0:
                print("结果：%s" % (line.decode()))
                m.tell()
                lines = m.read(1000)
                print(lines.decode())
            elif m.tell() == m.size():
                break
            else:
                pass




    


if __name__ == '__main__':
    a = logFind('C:\\Users\\Administrator\\Desktop\\slow.log',
                '100.0.10.180')
