import pytube
import os, os.path
import requests
import datetime

class Model:
    def __init__(self):
        self.yt: pytube.YouTube | pytube.Playlist | pytube.Channel = None
        self._createTempDir()

    def setUrl(self, url: str, type: int, downloadProgressBar: callable):
        self.type = type
        match type:
            case 0:
                self.yt = pytube.YouTube(url, on_progress_callback=downloadProgressBar)
                # Raises different exceptions based on why the
                # video is unavailable, otherwise does nothing.
                self.yt.check_availability()
            case 1:
                self.yt = pytube.Playlist(url)
            case 2:
                self.yt = pytube.Channel(url)
    
    def _createTempDir(self):
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")

    def availableStreams(self, only_audio: bool) -> dict:
        """Return dictionary where key is video's itag and value is format description"""
        streamQuery = self.yt.streams
        self.streams = {}

        # Get mp4 formats only
        for stream in streamQuery.filter(subtype="mp4", only_audio=only_audio):
            if stream.type == "video":
                format_description = f"{stream.mime_type} {stream.resolution} {stream.fps}fps"
            if stream.type == "audio":
                format_description = f"{stream.mime_type} {stream.abr}"
            self.streams[stream.itag] = format_description
        return self.streams

    def downloadByTag(self, itag: int, file_format: str):
        """Download video by itag"""
        if os.path.isfile(f"{self.yt.title}.{file_format}"):
            raise FileExistsError

        stream = self.yt.streams.get_by_itag(itag)
        output_file = stream.download(output_path=".")
        if file_format == "mp3":
            base, _ = os.path.splitext(output_file)
            new_file = base + ".mp3"
            os.rename(output_file, new_file) 

    def getThumbnail(self) -> str:
        """Download the video thumbnail then return file name"""
        filename = "thumbnail.jpg"
        img = requests.get(self.yt.thumbnail_url).content
        with open(f"./tmp/{filename}", 'wb') as handler:
            handler.write(img)
        return filename
    
    def getAuthor(self):
        """Get the video author"""
        return self.yt.author

    def getTitle(self):
        """Get the video title"""
        return self.yt.title
    
    def getLength(self):
        """Get the video length in hh:mm:ss format"""
        return str(datetime.timedelta(seconds=self.yt.length))

