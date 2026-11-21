import os

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setMinimumSize(460, 260)

        layout = QVBoxLayout(self)
        browser = QTextBrowser(self)
        browser.setOpenExternalLinks(True)
        browser.setHtml(
            """
            <h3>Yuval Nissim</h3>
            <p><b>Email:</b> yuval6891@gmail.com</p>
            <p><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/yuval-nissim-832457397/">LinkedIn Profile</a></p>
            <p><b>GitHub Repository:</b> <a href="https://github.com/yuval1188/hw-exe2">https://github.com/yuval1188/hw-exe2</a></p>
            """
        )
        layout.addWidget(browser)


class IceCreamMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Revenue vs. Temperature")
        self.setMinimumSize(900, 680)

        # Data lists - filled when a file is loaded
        self.temperatures = []
        self.revenues = []

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top bar: select file button + file name + about button
        top_bar = QHBoxLayout()
        self.select_file_btn = QPushButton("Select Data File", self)
        self.select_file_btn.clicked.connect(self.open_file_dialog)
        self.file_label = QLabel("No file selected", self)
        self.about_btn = QPushButton("About", self)
        self.about_btn.clicked.connect(self.open_about_window)

        top_bar.addWidget(self.select_file_btn)
        top_bar.addWidget(self.file_label, stretch=1)
        top_bar.addWidget(self.about_btn)
        main_layout.addLayout(top_bar)

        # Matplotlib graph + toolbar (zoom, pan, save graph as file)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)

        self.plot_graph()

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Data File", "", "CSV Files (*.csv)")
        if file_path == "":
            return

        self.file_label.setText(os.path.basename(file_path))

        # Read the file into the two lists
        self.temperatures = []
        self.revenues = []
        f = open(file_path, "r")
        f.readline()  # skip the header line
        for line in f:
            parts = line.strip().split(",")
            self.temperatures.append(float(parts[0]))
            self.revenues.append(float(parts[1]))
        f.close()

        self.plot_graph()

    def plot_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Scatter plot: temperature on X, revenue on Y, point size 1
        ax.scatter(self.temperatures, self.revenues, s=1)

        # Trend line - only when there is data
        if len(self.temperatures) > 0:
            # polyfit with degree 1 returns the slope (m) and intercept (b) of y = m*x + b
            m, b = np.polyfit(self.temperatures, self.revenues, 1)

            # A straight line needs only two points: the lowest and highest temperature
            x1 = min(self.temperatures)
            x2 = max(self.temperatures)
            ax.plot([x1, x2], [m * x1 + b, m * x2 + b], color="red",
                    label="y = " + str(round(m, 2)) + "x + " + str(round(b, 2)))
            ax.legend()

        # Remove the top and right lines of the frame
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.set_title("Revenue vs Temperature")
        ax.set_xlabel("Temperature")
        ax.set_ylabel("Revenue")
        self.canvas.draw()

    def open_about_window(self):
        about_dialog = AboutWindow(self)
        about_dialog.exec()


if __name__ == "__main__":
    app = QApplication([])

    # Load the QSS style file (it sits in the same folder as this file)
    qss_path = os.path.join(os.path.dirname(__file__), "exe2_style.qss")
    style_file = open(qss_path, "r", encoding="utf-8")
    app.setStyleSheet(style_file.read())
    style_file.close()

    window = IceCreamMainWindow()
    window.show()
    app.exec()
