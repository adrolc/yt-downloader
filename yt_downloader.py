import sys
from PyQt6.QtWidgets import QApplication

from mvc.view import View
from mvc.model import Model
from mvc.controller import Controller


def main():
    """yt-downloader's main function."""
    App = QApplication([])
    mainWindow = View()
    mainWindow.show()
    Controller(model=Model(), view=mainWindow)
    sys.exit(App.exec())

if __name__ == "__main__":
    main()