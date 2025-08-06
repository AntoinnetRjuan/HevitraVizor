import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QFrame, QTextEdit, QComboBox
from PyQt5.QtGui import QFont
from backend.data_loader import load_file
from backend.data_analysis import basic_summary
from backend.visualization import plot_histogram

class CuteDataAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cute Data Analyzer")
        self.setFixedSize(500, 500)
        self.setStyleSheet("background-color: #FFF5F5;")

        self.layout = QVBoxLayout()

        self.title = QLabel("\ud83c\udf38 Cute Data Analyzer")
        self.title.setFont(QFont("Poppins", 20))
        self.title.setStyleSheet("color: #FF69B4; text-align: center;")
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
                background-color: #FFB6C1;
                border-radius: 12px;
                color: white;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #FF69B4;
            }
        """)
        self.loadButton.clicked.connect(self.load_data)
        self.layout.addWidget(self.loadButton)

        self.columnSelector = QComboBox()
        self.columnSelector.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #DDD;
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.columnSelector.currentIndexChanged.connect(self.plot_selected_column)
        self.layout.addWidget(self.columnSelector)

        self.setLayout(self.layout)
        self.df = None

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_path:
            try:
                self.df = load_file(file_path)
                summary = basic_summary(self.df)
                summary_text = f"Rows: {summary['rows']}\nColumns: {summary['columns']}\nMissing Values: {summary['missing_values']}\n\nColumn Types:\n"
                for col, dtype in summary['column_types'].items():
                    summary_text += f"- {col}: {dtype}\n"
                self.infoBox.setText(summary_text)
                self.populate_columns()
            except Exception as e:
                self.infoBox.setText(f"Error loading file:\n{str(e)}")

    def populate_columns(self):
        self.columnSelector.clear()
        if self.df is not None:
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            self.columnSelector.addItems(numeric_cols)

    def plot_selected_column(self):
        column = self.columnSelector.currentText()
        if column and self.df is not None:
            plot_histogram(self.df, column)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CuteDataAnalyzer()
    window.show()
    sys.exit(app.exec_())