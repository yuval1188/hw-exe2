from pathlib import Path

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
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

GITHUB_URL = "https://github.com/yuval1188/hw-exe2"


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setMinimumSize(460, 260)

        layout = QVBoxLayout(self)
        browser = QTextBrowser(self)
        browser.setOpenExternalLinks(True)
        browser.setHtml(
            f"""
            <h3>Yuval Nissim</h3>
            <p><b>Email:</b> yuval6891@gmail.com</p>
            <p><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/yuval-nissim-832457397/">LinkedIn Profile</a></p>
            <p><b>GitHub Repository:</b> <a href="{GITHUB_URL}">{GITHUB_URL}</a></p>
            """
        )
        layout.addWidget(browser)


class IceCreamMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Revenue vs. Temperature")
        self.setMinimumSize(900, 680)

        # Data lists, filled when a file is loaded
        self.temperatures = []
        self.revenues = []
        self.selected_file = ""

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top bar: select file + file name + about
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

        # Matplotlib figure + toolbar (zoom, pan, save as file)
        self.figure = Figure(figsize=(8, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas, stretch=1)

        self.plot_graph()

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Ice Cream Data File",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if not file_path:
            return

        self.selected_file = file_path
        self.file_label.setText(Path(file_path).name)

        temperatures = []
        revenues = []
        with open(self.selected_file, "r", encoding="utf-8") as f:
            next(f)  # skip header line: Temperature,Revenue
            for line in f:
                line = line.strip()
                if not line:
                    continue
                temp, revenue = line.split(",")
                temperatures.append(float(temp))
                revenues.append(float(revenue))

        self.temperatures = temperatures
        self.revenues = revenues
        self.plot_graph()

    def plot_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Scatter plot: temperature on X, revenue on Y, point size 1
        ax.scatter(self.temperatures, self.revenues, s=1, color="#2563EB", label="Daily data")

        # Remove the top and right lines of the frame
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Linear regression: find the best-fit straight line y = m*x + b
        if len(self.temperatures) >= 2:
            x = np.array(self.temperatures)
            y = np.array(self.revenues)
            # np.polyfit(x, y, 1) fits a polynomial of degree 1 (a straight line)
            # using least squares and returns the coefficients [m, b]
            m, b = np.polyfit(x, y, 1)
            x_line = np.linspace(x.min(), x.max(), 100)
            y_line = m * x_line + b
            ax.plot(x_line, y_line, color="#DC2626", linewidth=2,
                    label=f"Best fit: y = {m:.2f}x + {b:.2f}")
            ax.legend(loc="upper left", frameon=False)

        ax.set_title("Ice Cream Revenue vs. Temperature", fontsize=14, fontweight="bold")
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Revenue ($)")

        self.canvas.draw()

    def open_about_window(self):
        about_dialog = AboutWindow(self)
        about_dialog.exec()


def load_stylesheet(app: QApplication, qss_path: str = "style.qss"):
    path = Path(__file__).parent / qss_path
    if path.exists():
        app.setStyleSheet(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    app = QApplication([])
    app.setLayoutDirection(Qt.LeftToRight)
    load_stylesheet(app, "style.qss")
    window = IceCreamMainWindow()
    window.show()
    app.exec()
