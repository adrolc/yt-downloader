from functools import partial
from pytube import exceptions

class Controller:
    """yt-downloader's controller class."""

    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._connectSignalsAndSlots()


    def _connectSignalsAndSlots(self):
        self._view.ytLoadButton.clicked.connect(partial(self._loadVideo))
        self._view.ytDownloadButton.clicked.connect(partial(self._download))
        self._view.ytAudioOnlyCheckBox.stateChanged.connect(partial(self._audioOnlyState))
    
    def _loadVideo(self):
        try:
            self._model.setUrl(self._view.getYtUrl(), self._view.getYtUrlType(), self._downloadProgressBar)
        except exceptions.RegexMatchError:
            self._view.statusBar().showMessage("Error: wrong URL")
        except exceptions.VideoPrivate:
            self._view.statusBar().showMessage("Error: video is private")
        except exceptions.VideoRegionBlocked:
            self._view.statusBar().showMessage("Error: region blocked")
        except exceptions.VideoUnavailable:
            self._view.statusBar().showMessage("Error: video unavailable")
        except:
            self._view.statusBar().showMessage("Error: Something went wrong")
        else:
            # Download and set thumbnail
            self._model.getThumbnail()
            self._view.setThumbnail()
            # View video details
            self._view.detailsAuthor.setText(f"<b>Author</b>: {self._model.getAuthor()}")
            self._view.detailsTitle.setText(f"<b>Title</b>: {self._model.getTitle()}")
            self._view.detailsLength.setText(f"<b>Length</b>: {self._model.getLength()}<hr>")
            self._showDownloadMenu()
            self._view.statusBar().showMessage("Video loaded")
    
    def _showDownloadMenu(self):
        # Check the state of the audio only checkbox
        audio_only = self._view.ytAudioOnlyCheckBox.isChecked()
        # Clear items from ComboBox
        self._view.ytVideoType.clear()
        # Set ComboBox items (video formats)
        # Show download menu
        self._view.ytVideoType.addItems(self._model.availableStreams(only_audio=audio_only).values())
        self._view.ytVideoType.setHidden(False)
        if audio_only:
            self._view.mp3FormatCheckBox.setHidden(False)
        else:
            self._view.mp3FormatCheckBox.setHidden(True)

        self._view.ytDownloadButton.setHidden(False)
        self._view.downloadProgress.setHidden(False)

    def _download(self):
        # Reset progressBar
        self._view.downloadProgress.setValue(0)
        videoTypeIndex = self._view.getYtVideoType()
        itag = list(self._model.streams.keys())[videoTypeIndex]
        mp3Checked = self._view.mp3FormatCheckBox.isChecked()
        format = "mp3" if mp3Checked == True else "mp4"
        try:
            self._model.downloadByTag(itag, format)
        except FileExistsError:
            self._view.statusBar().showMessage("Error: File already exists")
        except:
            self._view.statusBar().showMessage("Error: Something went wrong")
        else:
            self._view.statusBar().showMessage("Successfully downloaded")
    
    def _downloadProgressBar(self, stream, data_chunk, bytes_re):
        percent = int(100 - (bytes_re / stream.filesize * 100))
        self._view.downloadProgress.setValue(percent)
    
    def _audioOnlyState(self):
        if self._model.yt:
            self._view.ytVideoType.clear()
            if self._view.ytAudioOnlyCheckBox.isChecked():
                self._view.ytVideoType.addItems(self._model.availableStreams(only_audio=True).values())
                self._view.mp3FormatCheckBox.setHidden(False)
            else:
                self._view.ytVideoType.addItems(self._model.availableStreams(only_audio=False).values())
                self._view.mp3FormatCheckBox.setHidden(True)
                self._view.mp3FormatCheckBox.setChecked(False)

