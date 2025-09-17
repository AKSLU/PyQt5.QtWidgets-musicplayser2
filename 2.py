import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QFileDialog, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon
import pygame
from mutagen.mp3 import MP3


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setFixedSize(360, 500)

        self.setStyleSheet("""
            QWidget {
                background-color: SlateGrey;
                color: MistyRose;
            }
            QPushButton {
                background-color: Black;
                border: 1px solid #666;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: Grey;
            }
        """)

        pygame.mixer.init()
        self.filename = ""
        self.duration = 0
        self.playing = False
        self.current_pos = 0  

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slider)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        self.cover = QLabel()
        if os.path.exists("image.jpg"):
            self.cover.setPixmap(QPixmap("image.jpg").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.cover.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.cover)


        self.track_label = QLabel("No file selected")
        self.track_label.setAlignment(Qt.AlignCenter)
        self.track_label.setFont(QFont("Consolas", 16))
        layout.addWidget(self.track_label)

        
        self.open_button = QPushButton("Open File")
        self.open_button.setFont(QFont("Consolas", 12))
        self.open_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_button)

         
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setValue(0)
        self.slider.sliderMoved.connect(self.seek)
        layout.addWidget(self.slider)

        
        control_layout = QHBoxLayout()
        control_layout.setSpacing(0) 

        button_size = 60 

        
        self.rewind_button = QPushButton()
        self.rewind_button.setIcon(QIcon("icons/rewind.png"))
        self.rewind_button.setIconSize(QSize(32, 32))
        self.rewind_button.setFixedSize(button_size, button_size)
        self.rewind_button.setText("")
        self.rewind_button.clicked.connect(self.rewind)
        control_layout.addWidget(self.rewind_button)

        
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("icons/play.png"))
        self.play_button.setIconSize(QSize(32, 32))
        self.play_button.setFixedSize(button_size, button_size)
        self.play_button.setText("")
        self.play_button.clicked.connect(self.toggle_play)
        control_layout.addWidget(self.play_button)

        
        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon("icons/forward.png"))
        self.forward_button.setIconSize(QSize(32, 32))
        self.forward_button.setFixedSize(button_size, button_size)
        self.forward_button.setText("")
        self.forward_button.clicked.connect(self.forward)
        control_layout.addWidget(self.forward_button)

        layout.addLayout(control_layout)
        self.setLayout(layout)

   
    def open_file(self):
        file_filter = "Audio Files (*.mp3 *.wav)"
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", file_filter)

        if self.filename:
            pygame.mixer.music.load(self.filename)
            self.track_label.setText(os.path.basename(self.filename))

            if self.filename.endswith(".mp3"):
                self.duration = int(MP3(self.filename).info.length)
            else:
                self.duration = 100

            self.slider.setMaximum(self.duration)
            self.slider.setValue(0)
            self.current_pos = 0
            self.playing = False
            self.play_button.setIcon(QIcon("icons/play.png"))
            self.timer.stop()

    def toggle_play(self):
        if not self.filename:
            return

        if not self.playing:
            pygame.mixer.music.play(start=self.current_pos)
            self.play_button.setIcon(QIcon("icons/pause.png"))
            self.timer.start(1000)
        else:
            pygame.mixer.music.pause()
            self.play_button.setIcon(QIcon("icons/play.png"))
            self.timer.stop()

        self.playing = not self.playing

    def update_slider(self):
        if self.playing:
            self.current_pos += 1
            if self.current_pos >= self.duration:
                self.current_pos = self.duration
                self.playing = False
                self.play_button.setIcon(QIcon("icons/play.png"))
                self.timer.stop()
                pygame.mixer.music.stop()
        self.slider.setValue(self.current_pos)

    def seek(self, position):
        if self.filename:
            self.current_pos = position
            pygame.mixer.music.play(start=self.current_pos)
            self.play_button.setIcon(QIcon("icons/pause.png"))
            self.playing = True
            self.timer.start(1000)
            self.slider.setValue(self.current_pos)

    def rewind(self):
        if self.filename:
            self.current_pos = max(self.current_pos - 10, 0)
            pygame.mixer.music.play(start=self.current_pos)
            self.play_button.setIcon(QIcon("icons/pause.png"))
            self.playing = True
            self.timer.start(1000)
            self.slider.setValue(self.current_pos)

    def forward(self):
        if self.filename:
            self.current_pos = min(self.current_pos + 10, self.duration)
            pygame.mixer.music.play(start=self.current_pos)
            self.play_button.setIcon(QIcon("icons/pause.png"))
            self.playing = True
            self.timer.start(1000)
            self.slider.setValue(self.current_pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec_())
