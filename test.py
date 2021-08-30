from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        settings = QSettings('my_org', 'my_app')
        self._finishcount = settings.value('finishcount', [], int)
        print('read settings: %s' % self._finishcount)
        # add a new value for testing
        self._finishcount.append(len(self._finishcount))

    def closeEvent(self, event):
        settings = QSettings('my_org', 'my_app')
        settings.setValue('finishcount', self._finishcount)
        print('save settings: %s' % self._finishcount)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(600, 100, 100, 100)
    window.show()
    sys.exit(app.exec_())