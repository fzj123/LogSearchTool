from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
from LogFind import logFind
import xlwt
import os
import mmap
import contextlib


class LogViewTool(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("resource\\UI\\LogViewTool.ui")

        # 选择多选
        # self.ui.list_conditions.setSelectionMode(
        #    QAbstractItemView.ExtendedSelection)
        self.ui.list_conditions.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
    
        self.ui.btn_add.clicked.connect(self.addContent)
        self.ui.btn_delete.clicked.connect(self.deleContent)
        self.ui.btn_clear.clicked.connect(self.clearContent)
        self.ui.btn_open.clicked.connect(self.openLog)
        self.ui.btn_export.clicked.connect(self.excelExport)

        file = open('temp.txt')
        while True:
            text = file.readline()
            text = text.strip('\n')
            self.ui.list_conditions.addItem(text)
            print(text)
            if not text:
                break
        file.close()

    def addContent(self):
        text = self.ui.lineEdit.text()
        self.ui.list_conditions.addItem(text)
        self.ui.lineEdit.clear()

        file_txt = 'temp.txt'
        with open(file_txt, "a") as file:
            file.write(text + "\n")

    def deleContent(self):
        list_id = self.ui.list_conditions.currentRow()
        dele_text = self.ui.list_conditions.currentItem().text()
        print(list_id)
        print(dele_text)
        self.ui.list_conditions.takeItem(list_id)

        with open("temp.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("temp.txt", "w", encoding="utf-8") as f_w:
            for line in lines:
                if dele_text in line:
                    continue
                f_w.write(line)

    def clearContent(self):
        self.ui.list_conditions.clear()
        with open("temp.txt", 'w') as f:
            f.truncate()

    def openLog(self):

        filePath, _ = QFileDialog.getOpenFileName(
            self.ui,             # 父窗口对象
            "选择要打开的日志",  # 标题
            r".",        # 起始目录
            "日志类型 (*.log *.log*)"  # 选择类型过滤项，过滤内容在括号中
        )
        print('打开日志的路径：%s' % filePath)
        str_query = self.ui.list_conditions.currentItem().text()
        print('选择查询条件：%s' % str_query)

        f = open(filePath, 'r')
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            while True:
                line = m.readline().strip()
                if line.find(str_query.encode()) >= 0:
                    print("结果：%s" % (line.decode()))
                    m.tell()
                    lines = m.read(1000)
                    print(lines.decode())
                    self.ui.pte_content.appendPlainText(line.decode())
                    self.ui.pte_content.appendPlainText(lines.decode())
                    self.ui.pte_content.appendPlainText("--------------------------------------------------------")
                elif m.tell() == m.size():
                    break
                else:
                    pass
       



    def excelExport(self):
        filePath = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
        print('保存路径：%s' % filePath)


#app = QApplication([])
#window = LogViewTool()
# window.ui.show()
# app.exec_()
