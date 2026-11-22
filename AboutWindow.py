from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QWidget


class AboutWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("אודות")
        self.setFixedSize(400, 540)

        self.setStyleSheet("background-color: #ffccde;")
        self.image_container = QLabel(self)
        self.image_container.setGeometry(50, 30, 300, 300)
        self.image_container.setStyleSheet(
            "background-color: white; border-radius: 15px; border: 2px solid #ff99bb;")

        self.image_label = QLabel(self.image_container)
        self.image_label.setGeometry(15, 15, 270, 270)
        self.image_label.setScaledContents(True)
        self.image_label.setStyleSheet(
            "border-radius: 10px; qproperty-alignment: 'AlignCenter';")


        image = QPixmap("11.jpeg").scaled(270, 270)
        self.image_label.setPixmap(image)

        self.label_name = QLabel("שם: יובל נסים", self)
        self.label_name.setGeometry(30, 350, 340, 30)
        self.label_name.setStyleSheet(
            "font-size: 12pt; font-weight: bold; color: #800040; background: transparent; qproperty-alignment: 'AlignCenter';")

        self.label_email = QLabel("אימייל: yuval6891@gmail.com", self)
        self.label_email.setGeometry(30, 390, 340, 30)
        self.label_email.setStyleSheet(
            "font-size: 10pt; color: #660033; background: transparent; qproperty-alignment: 'AlignCenter';")

        self.label_linkedin = QLabel('לינקדאין: <a href="https://www.linkedin.com/in/yuval-nissim-832457397/">עמוד ה-LinkedIn</a>',self)
        self.label_linkedin.setGeometry(30, 430, 340, 30)
        self.label_linkedin.setStyleSheet("font-size: 10pt; background: transparent; qproperty-alignment: 'AlignCenter';")
        self.label_linkedin.setOpenExternalLinks(True)

        self.label_github = QLabel('GitHub: <a href="https://github.com/yuval1188/hw-exe2">https://github.com/yuval1188/hw-exe2</a>', self)
        self.label_github.setGeometry(30, 470, 340, 30)
        self.label_github.setStyleSheet("font-size: 10pt; background: transparent; qproperty-alignment: 'AlignCenter';")
        self.label_github.setOpenExternalLinks(True)


if __name__ == "__main__":
    app = QApplication([])
    window = AboutWindow()
    window.show()
    app.exec()