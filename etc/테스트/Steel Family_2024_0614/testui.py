import sys
import os
import datetime
import xlwings as xw
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFrame, QPushButton
from PyQt5.QtGui import QIcon

route_first = "경로 : "
time_first = "생성 시간 : "

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.files = []  # 드래그 앤 드롭된 파일 경로를 저장할 리스트

    def initUI(self):
        self.setWindowTitle('::: CSV creator for Steel Family Catalog :::')
        self.setWindowIcon(QIcon('resources/faviconV2.png'))
        self.setGeometry(500, 300, 500, 300)
        self.setAcceptDrops(True)

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()

        # 상단 레이아웃 생성
        self.label_path = QLabel(route_first, self)
        upper_layout = QVBoxLayout()
        upper_layout.addWidget(self.label_path)

        # 하단 레이아웃 생성
        self.label_time = QLabel(time_first, self)
        lower_layout = QVBoxLayout()
        lower_layout.addWidget(self.label_time)

        # 상단과 하단 레이아웃을 프레임에 추가
        upper_frame = QFrame()
        upper_frame.setLayout(upper_layout)
        upper_frame.setStyleSheet("background-color: lightgray;")

        lower_frame = QFrame()
        lower_frame.setLayout(lower_layout)
        lower_frame.setStyleSheet("background-color: white;")

        # 버튼 생성
        # self.button = QPushButton('Show Creation Time', self)
        # self.button.clicked.connect(self.showCreationTime)
        self.button = QPushButton('Create CSV !', self)
        self.button.clicked.connect(self.saveAllFiles_asCSV)

        # 메인 레이아웃에 프레임과 버튼 추가
        main_layout.addWidget(upper_frame)
        main_layout.addWidget(self.button)
        main_layout.addWidget(lower_frame)
        
        self.setLayout(main_layout)
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.files = [u.toLocalFile() for u in event.mimeData().urls()]
        path_label_text = ""
        for f in self.files:
            print(f)
            path_label_text += route_first + f + "\n"
        self.label_path.setText(path_label_text)

    def showCreationTime(self):
        if not self.files:  # 파일이 드래그 앤 드롭되지 않았다면 함수 종료
            self.label_time.setText("No files dragged and dropped.")
            return
        
        time_label_text = ""
        for f in self.files:
            creation_time = os.path.getctime(f)
            creation_time_formatted = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M')
            time_label_text += time_first + creation_time_formatted + "\n"
        self.label_time.setText(time_label_text)
    
    def saveAllFiles_asCSV(self):
        if not self.files:  # 파일이 드래그 앤 드롭되지 않았다면 함수 종료
            self.label_time.setText("No files dragged and dropped.")
            return
        
        def saveAllSheetAsCSV(tgtFile):
            def saveSheetAsCSV(tgtSheet, subPath):
                if "column" in subPath.lower():
                    memberKind = "Column"
                elif "framing" in subPath.lower():
                    memberKind = "Framing"
                
                sheetName = tgtSheet.name
                sheetName_shape = sheetName.split(" ")[-1] 
                sheetName_code = sheetName.split(" ")[0]
                csv_fileName = f"Steel {memberKind}_{sheetName_shape}_{sheetName_code}"
                usedRng = tgtSheet.used_range
                datas = usedRng.value
                
                with open(f"{subPath}\\{csv_fileName}.txt", "w") as file:
                    writer = csv.writer(file)
                    writer.writerows(datas)
                    
                return subPath
            
            app = xw.App(visible=False)
            workbook = xw.Book(tgtFile)
            fileName = workbook.name
            subPath = os.path.splitext(tgtFile)[0]
            
            if not os.path.exists(subPath):
                os.makedirs(subPath)
                
            all_sheets = workbook.sheets
            
            res = []
            for tgtSheet in all_sheets:
                res.append( saveSheetAsCSV(tgtSheet, subPath) )
            
            app.kill()
            return res
        
        label_text = ""
        allFiles = self.files
        try:
            res = list(map( lambda tgtFile: saveAllSheetAsCSV(tgtFile), allFiles ))
            label_text = "생성 완료!"
            self.label_time.setText(label_text)
        except:
            label_text = "생성 실패.. mk에게 문의하세요"
            self.label_time.setText(label_text)
        return res
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
