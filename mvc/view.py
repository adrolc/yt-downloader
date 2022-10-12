from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFormLayout,
    QComboBox,
    QLabel,
    QHBoxLayout,
    QCheckBox,
    QProgressBar,
)
from PyQt6.QtGui import (
    QPixmap,
    QIcon,
)

WINDOW_SIZE = (630, 700)

class View(QMainWindow):
    """yt-downloader's main window (View)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("YT Downloader")
        self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.setWindowIcon(QIcon("img/icon.png"))
        self.setStyleSheet(open('./style/style.css').read())
        self.mainLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setContentsMargins(25, 20, 25, 20)
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)
        self.logoLabel = QLabel("<b style='color: #1dd1a1;'>YT</b> Downloader")
        self.logoLabel.setStyleSheet('font-size: 45px;')
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.logoLabel)
        self._createUrlInput()
        self._createVideoInfo()
        self._createDownloadMenu()
        self._createProgressBar()


        self.statusBar().showMessage("Ready")

    def _createUrlInput(self):
        self.ytUrlType = QComboBox()
        self.ytUrlType.addItems(["Video"])
        # self.ytUrlType.addItems(["Video", "Playlist", "Channel"])

        self.ytUrl = QLineEdit()
        self.ytAudioOnlyCheckBox = QCheckBox("Audio only")
        self.ytLoadButton = QPushButton("Load")
        self.ytLoadButton.setFixedWidth(100)

        ytUrlInputLayout = QFormLayout()
        ytUrlInputLayout.addRow("Type:", self.ytUrlType)
        ytUrlInputLayout.addRow("URL:", self.ytUrl)
        ytUrlInputLayout.addRow(self.ytAudioOnlyCheckBox)
        ytUrlInputLayout.addRow(self.ytLoadButton)

        self.mainLayout.addLayout(ytUrlInputLayout)


    def _createVideoInfo(self):
        self.thumbnail = QLabel()
        self.detailsAuthor = QLabel()
        self.detailsTitle = QLabel()
        self.detailsLength = QLabel()
        self.detailsTitle.setWordWrap(True)
        self.detailsTitle.setMaximumWidth(250)

        videoDetailsLayout = QVBoxLayout()
        videoDetailsLayout.addWidget(self.detailsAuthor)
        videoDetailsLayout.addWidget(self.detailsTitle)
        videoDetailsLayout.addWidget(self.detailsLength)

        videoInfoLayout = QHBoxLayout()
        videoInfoLayout.addWidget(self.thumbnail)
        videoInfoLayout.addLayout(videoDetailsLayout)
        
        self.mainLayout.addLayout(videoInfoLayout)
    
    def setThumbnail(self):
        thumbnail = QPixmap("./tmp/thumbnail.jpg")
        thumbnail = thumbnail.scaled(176, 132)
        self.thumbnail.setPixmap(thumbnail)

    def _createDownloadMenu(self):
        self.ytVideoType = QComboBox()
        self.ytVideoType.setHidden(True)

        self.mp3FormatCheckBox = QCheckBox("mp3")
        self.mp3FormatCheckBox.setHidden(True)

        self.ytDownloadButton = QPushButton("Download")
        self.ytDownloadButton.setFixedWidth(100)
        self.ytDownloadButton.setHidden(True)

        self.downloadMenuLayout = QVBoxLayout()
        self.downloadMenuLayout.addWidget(self.ytVideoType)
        self.downloadMenuLayout.addWidget(self.mp3FormatCheckBox)
        self.downloadMenuLayout.addWidget(self.ytDownloadButton)

        self.mainLayout.addLayout(self.downloadMenuLayout)
    
    def _createProgressBar(self):
        self.downloadProgress = QProgressBar()
        self.downloadProgress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.downloadProgress.setHidden(True)
        self.mainLayout.addWidget(self.downloadProgress)
    
    def getYtUrl(self):
        return self.ytUrl.text()
    
    def getYtUrlType(self):
        return self.ytUrlType.currentIndex()
    
    def getYtVideoType(self):
        return self.ytVideoType.currentIndex()
