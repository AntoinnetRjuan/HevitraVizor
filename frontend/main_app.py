import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QComboBox, QTextEdit, QStackedWidget,
    QListWidget, QListWidgetItem, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DataAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Analysis & Visualization App")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #2e2e2e; color: white;")

        self.data = None

        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        # Menu
        self.menu = QListWidget()
        self.menu.setFixedWidth(200)
        self.menu.setStyleSheet("background-color: #3c3c3c; color: white;")
        for name, icon in [("Home", "home.png"), ("Analysis", "analysis.png"), ("Visualization", "chart.png")]:
            item = QListWidgetItem(QIcon(icon), name)
            self.menu.addItem(item)
        self.menu.currentRowChanged.connect(self.display_page)

        # Pages
        self.stack = QStackedWidget()
        self.stack.addWidget(self.home_page())
        self.stack.addWidget(self.analysis_page())
        self.stack.addWidget(self.visualization_page())

        main_layout.addWidget(self.menu)
        main_layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        welcome = QLabel("Bienvenue dans l'application d'analyse de données !")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet("font-size: 22px; font-weight: bold; margin-top: 20px;")

        image = QLabel()
        pixmap = QPixmap("data.png").scaledToWidth(150)
        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignCenter)

        layout.addWidget(image)
        layout.addWidget(welcome)
        page.setLayout(layout)
        return page

    def analysis_page(self):
        self.analysis_page_widget = QWidget()
        layout = QVBoxLayout()

        self.load_btn = QPushButton("Charger un fichier Excel/CSV")
        self.load_btn.clicked.connect(self.load_file)
        layout.addWidget(self.load_btn)

        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        layout.addWidget(self.analysis_text)

        self.analysis_page_widget.setLayout(layout)
        return self.analysis_page_widget

    def visualization_page(self):
        self.visualization_page_widget = QWidget()
        layout = QVBoxLayout()

        self.column_selector = QComboBox()
        self.column_selector.currentTextChanged.connect(self.plot_histogram)
        layout.addWidget(self.column_selector)

        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)

        self.visualization_page_widget.setLayout(layout)
        return self.visualization_page_widget

    def display_page(self, index):
        self.stack.setCurrentIndex(index)

    def load_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier", "", "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)", options=options
        )
        if file_path:
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            else:
                self.data = pd.read_excel(file_path)

            self.perform_analysis()
            self.column_selector.clear()
            self.column_selector.addItems(self.data.select_dtypes(include='number').columns)

    def perform_analysis(self):
        if self.data is not None:
            text = f"Shape: {self.data.shape}\n\n"
            text += f"Colonnes:\n{list(self.data.columns)}\n\n"
            text += f"Types de données:\n{self.data.dtypes}\n\n"
            text += f"Valeurs manquantes:\n{self.data.isnull().sum()}\n\n"
            text += f"Statistiques descriptives:\n{self.data.describe()}"

            self.analysis_text.setText(text)

    def plot_histogram(self, column):
        if self.data is not None and column:
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)
            ax.hist(self.data[column].dropna(), bins=20, color='skyblue', edgecolor='black')
            ax.set_title(f"Histogramme de {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Fréquence")
            self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataAnalyzer()
    window.show()
    sys.exit(app.exec_())
