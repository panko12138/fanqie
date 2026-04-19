from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from utils.logger import get_logger
from utils.helpers import get_resources_path
import os

logger = get_logger(__name__)


class WhiteNoisePlayer(QObject):
    state_changed = pyqtSignal(bool)
    volume_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent())
        self.is_playing = False
        self.volume = 50
        self.current_noise = None
        self.available_noises = self._scan_noises()

    def _scan_noises(self) -> list:
        noises_dir = os.path.join(get_resources_path(), "sounds", "white_noise")
        if not os.path.exists(noises_dir):
            return []

        noises = []
        for filename in os.listdir(noises_dir):
            if filename.endswith((".mp3", ".wav", ".ogg")):
                name = os.path.splitext(filename)[0]
                noises.append({
                    "name": name,
                    "path": os.path.join(noises_dir, filename),
                })
        return noises

    def get_available_noises(self) -> list:
        return self.available_noises

    def play(self, noise_name: str = None):
        noise_path = None

        if noise_name:
            noise = next((n for n in self.available_noises if n["name"] == noise_name), None)
            if noise:
                noise_path = noise["path"]
                self.current_noise = noise_name
        elif self.available_noises:
            noise_path = self.available_noises[0]["path"]
            self.current_noise = self.available_noises[0]["name"]

        if noise_path and os.path.exists(noise_path):
            url = QUrl.fromLocalFile(noise_path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.setVolume(self.volume)
            self.player.play()
            self.is_playing = True
            self.state_changed.emit(True)
            logger.info(f"播放白噪音: {self.current_noise}")

    def stop(self):
        self.player.stop()
        self.is_playing = False
        self.state_changed.emit(False)
        logger.info("停止白噪音")

    def set_volume(self, volume: int):
        self.volume = max(0, min(100, volume))
        self.player.setVolume(self.volume)
        self.volume_changed.emit(self.volume)

    def get_volume(self) -> int:
        return self.volume

    def is_active(self) -> bool:
        return self.is_playing

    def get_current_noise(self) -> str:
        return self.current_noise
