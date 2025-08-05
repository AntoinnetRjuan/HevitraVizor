import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QFrame, QTextEdit
from PyQt5.QtGui import QFont, QIcon
from backend.data_loader import load_file
from backend.data_analysis import basic_summary

class CuteDataAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cute Data Analyzer")
        self.setFixedSize(500, 400)
        self.setStyleSheet("background-color: #FFF5F5;")

        self.layout = QVBoxLayout()

        self.title = QLabel("\ud83c\udf38 Cute Data Analyzer")
        self.title.setFont(QFont("Poppins", 20))
        self.title.setStyleSheet("color: #005ab5; text-align: center;")
        self.layout.addWidget(self.title)

        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: #FFFFFF; border-radius: 15px; border: 1px solid #DDD;")
        self.frame.setFixedHeight(200)
        self.frameLayout = QVBoxLayout(self.frame)

        self.infoBox = QTextEdit()
        self.infoBox.setReadOnly(True)
        self.infoBox.setStyleSheet("border: none; font-size: 14px; color: #555;")
        self.frameLayout.addWidget(self.infoBox)

        self.layout.addWidget(self.frame)

        self.loadButton = QPushButton("\ud83d\udcc2 Import Data File")
        self.loadButton.setStyleSheet("""
            QPushButton {
                background-color: #4aa5ff;
                border-radius: 12px;
                color: white;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005ab5;
            }
        """)
        self.loadButton.clicked.connect(self.load_data)

        self.layout.addWidget(self.loadButton)

        self.setLayout(self.layout)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_path:
            try:
                df = load_file(file_path)
                summary = basic_summary(df)
                summary_text = f"Rows: {summary['rows']}\nColumns: {summary['columns']}\nMissing Values: {summary['missing_values']}\n\nColumn Types:\n"
                for col, dtype in summary['column_types'].items():
                    summary_text += f"- {col}: {dtype}\n"
                self.infoBox.setText(summary_text)
            except Exception as e:
                self.infoBox.setText(f"Error loading file:\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CuteDataAnalyzer()
    window.show()
    sys.exit(app.exec_())