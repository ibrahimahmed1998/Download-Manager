import sys
import urllib.request
from logging import exception
from pafy.pafy import *
import pafy
import humanize
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUiType    # She is work Don't Edit Here :D
from os import *

## Notes ##
# when Bind Remove () From Function Call
#
#****************************************************************#

FORM_ClASS,_= loadUiType(path.join(path.dirname(__file__),'design.ui')) # Design.ui File Path

class MainApp(QMainWindow,FORM_ClASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_Ui()
        self.handle_btns()
        self.Progress
        self.SaveAt
        self.Custom_Download
        ####################
        self.Get_Info
        self.SaveAt_2
        self.Download_Youtube
        self.playlist

#****************************************************************#
    def handle_Ui(self):          # Handle User Interface
        self.setWindowTitle("Video Downloader")
        self.setFixedSize(800,570)
#****************************************************************#
    def handle_btns(self):         # Handle All Buttons
        self.pushButton.clicked.connect(self.Custom_Download)
        self.pushButton_2.clicked.connect(self.SaveAt)
        self.pushButton_5.clicked.connect(self.SaveAt_2)
        self.pushButton_6.clicked.connect(self.Get_Info)
        self.pushButton_3.clicked.connect(self.Download_Youtube)
        self.pushButton_7.clicked.connect(self.playlist)
#****************************************************************#
#********************** <  TAP - 1 > ****************************#
    def SaveAt(self):       # Handle Save At Button
        location = QFileDialog.getSaveFileName(self,caption="Save At",directory="." , filter="All Files (*.*) ") #  print(location)
        txt = str(location)  # Casting location
        new = (txt[2:].split(',')[0].replace("'", '')) # Split it into 2 Parts
        self.lineEdit_2.setText(new)
#****************************************************************#
    def Progress(self,blocknum,blocksize,totalsize):   # Handle Progress Bar
        read = blocknum * blocksize
        if totalsize > 0 :
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()     # Solution to Not Responding
# ****************************************************************#
    def Custom_Download(self):  # Handle Download Button
        url = self.lineEdit.text()  # print(url)
        save_at = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url, save_at, self.handle_progress)
        except Exception:
            QMessageBox.warning(self, " Download Statues ", " Download Error :( ")  # Err Message Box
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.progressBar.setValue(0)
            return
        QMessageBox.information(self, " Download Statues ", " Compeleted ^_^ ")  # Success Message Box
        self.lineEdit.setText(" ")
        self.lineEdit_2.setText(" ")
        self.progressBar.setValue(0)
#****************************************************************#
#********************** <  TAP - 2 > ****************************#
    def Get_Info(self):             # Button[6] => Get Information About Youtube Videos
        url = self.lineEdit_6.text()
        v = pafy.new(url)           # Video
        stream = v.streams
        for s in stream:
            size = humanize.naturalsize( s.get_filesize() )
            data = '{} {} {} {}'.format(s.mediatype,s.extension,s.quality,size)
            self.comboBox.addItem(data)
#****************************************************************#
    def SaveAt_2(self):   # Button[5] => Get Information About Youtube Videos
        location = QFileDialog.getExistingDirectory(self,"Select Download Directory")  # print(location)
        self.lineEdit_5.setText(location)
#****************************************************************#
    def Download_Youtube(self): # Button[3] => Get Information About Youtube Videos
        video_link = self.lineEdit_6.text()
        Save_At = self.lineEdit_5.text()
        v = pafy.new(video_link)
        stream = v.streams
        Quality =self.comboBox.currentIndex()

        try:
            Download = stream[Quality].download(filepath=Save_At)
        except Exception:
            QMessageBox.warning(self, " Download Statues ", " Download Error :( ")  # Err Message Box
            self.lineEdi_5.setText("")
            self.lineEdit_6.setText("")
            #self.progressBar.setValue(0)
        return

        QMessageBox.information(self, " Download Statues ", " Compeleted ^_^ ")  # Success Message Box
#****************************************************************#
    def playlist(self):
        url =  self.lineEdit_6.text()
        Save_At = self.lineEdit_5.text()

        print("list is--------------- " + url)

        list = pafy.get_playlist2(url)
        videos = list['items']

        os.chdir(Save_At)

        if os.path.exists( str(list['title']) ):
            os.chdir(str(list['title']))
        else:
            os.mkdir(str(list['title']))
            os.chdir(str(list['title']))

        for v in videos:
            p = v['pafy']
            best = p.getbest(preftype='mp4')
            best.download()


#****************************************************************#
#****************************************************************#
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    window.handle_Ui()
    app.exec_() #Infinte Loop TO Don't Close the Window Screen
#****************************************************************#
if __name__ == '__main__':
    main()