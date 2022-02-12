import sys
import main
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton, QProgressBar
from PyQt5.QtCore import QObject, QThread, QSize, pyqtSignal

class Basic_view(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(500, 150))    
        self.setWindowTitle("PyInvestingStock") 

        # Two labels 
        self.in_label = QLabel(self)
        self.in_label.setText('Input file location:')
        self.in_label.resize(200, 32)
        self.in_label.move(20, 20)

        self.out_label = QLabel(self)
        self.out_label.setText('Output file location:')
        self.out_label.resize(200, 32)
        self.out_label.move(20, 60)

        # Two input fields
        self.in_edit = QLineEdit(self)
        self.in_edit.resize(220, 22)
        self.in_edit.move(160, 26)

        self.out_edit = QLineEdit(self)
        self.out_edit.resize(220, 22)
        self.out_edit.move(160, 66)

        # Two buttons for updating lines and one to start the script
        self.in_button = QPushButton('Update', self)
        self.in_button.clicked.connect(lambda: self.get_input(self.in_edit.text()))
        self.in_button.resize(80,32)
        self.in_button.move(400, 22)

        self.out_button = QPushButton('Update', self)
        self.out_button.clicked.connect(lambda: self.get_input(self.out_edit.text()))
        self.out_button.resize(80,32)
        self.out_button.move(400, 62)   

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(lambda: self.on_start())
        self.start_button.resize(380,32)
        self.start_button.move(60, 108)

    def get_input(self, input):
        print(input)
    
    def on_start(self):
        if not main.check_output_file():
            self.close()
            self.error = Error_view()
            self.error.show()
        else:
            self.close()
            self.progressview = Progress_view()
            self.progressview.show()
            self.progressview.main_loop()
        
class Progress_view(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(500, 150))    
        self.setWindowTitle("PyInvestingStock - progress")
        self.progress_value = 0
        self.max_value = 10
        
        self.info_label = QLabel(self)
        self.info_label.setText('Fetching data: ') 
        self.info_label.resize(200, 32)
        self.info_label.move(20, 20)
        
        self.progress = QProgressBar(self)
        self.progress.setMaximum(self.max_value)
        self.progress.setValue(self.progress_value)
        self.progress.resize(460,32)
        self.progress.move(20, 60)

        self.start_button = QPushButton('Stop', self)
        self.start_button.clicked.connect(lambda: self.on_stop())
        self.start_button.resize(380,32)
        self.start_button.move(60, 108)

    def main_loop(self):
        self.thread = QThread()
        self.worker = Worker(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def on_stop(self):
        self.close()

class Worker(QObject):
    def __init__(self, progresslink):
        super(Worker, self).__init__()
        self.finished = pyqtSignal()
        self.progress = pyqtSignal(int)
        self.progresslink = progresslink

    def run(self): 
        main.main(self.progresslink)

class Error_view(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(300, 120))    
        self.setWindowTitle("Error")

        self.err_label = QLabel(self)
        self.err_label.setText('Error occured: Check input/output paths')
        self.err_label.resize(260, 32)
        self.err_label.move(20, 20)

        self.close_button = QPushButton('Exit', self)
        self.close_button.clicked.connect(lambda: self.close())
        self.close_button.resize(100,32)
        self.close_button.move(100, 80)

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwin = Basic_view()
    mainwin.show()
    sys.exit(app.exec_())