from pathlib import Path

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

        # Data lists - filled when a file is loaded
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

        # Matplotlib figure + toolbar (zoom, pan, save graph as file)
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

        # TODO: open the file for reading, scan its data into
        #       self.temperatures and self.revenues, then call self.plot_graph()

    def plot_graph(self):
        # Temporary graph - TODO: edit this method so it draws the correct graph
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
        ax.set_title("Temporary Graph")
        self.canvas.draw()

    def open_about_window(self):
        about_dialog = AboutWindow(self)
        about_dialog.exec()


def load_stylesheet(app: QApplication, qss_path: str = "exe2_style.qss"):
    path = Path(__file__).parent / qss_path
    if path.exists():
        app.setStyleSheet(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    app = QApplication([])
    app.setLayoutDirection(Qt.LeftToRight)
    load_stylesheet(app, "exe2_style.qss")
    window = IceCreamMainWindow()
    window.show()
    app.exec()
