from LogViewToolPage import LogViewTool
from PyQt5.Qt import *
import sys

if __name__ == '__main__':
    app = QApplication([])
    window = LogViewTool()
    window.ui.show()
    sys.exit(app.exec_())

    
