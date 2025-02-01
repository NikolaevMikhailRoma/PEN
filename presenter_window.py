from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt

class PresenterWindow(QMainWindow):
    def __init__(self, game, spectator_window):
        super().__init__()
        self.game = game
        self.spectator_window = spectator_window
        self.setWindowTitle("Окно для ведущего")
        self.resize(400, 300)
        # Окно ведущего можно свободно перемещать

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # Информационная метка о текущем игроке и следующем очке
        self.info_label = QLabel("")
        layout.addWidget(self.info_label)

        # Комбобокс для выбора песни
        self.song_combo = QComboBox()
        self.song_combo.addItems(self.game.songs)
        layout.addWidget(self.song_combo)

        # Кнопка для присвоения очка выбранной песне
        self.assign_button = QPushButton("Присвоить очко")
        layout.addWidget(self.assign_button)
        self.assign_button.clicked.connect(self.assign_point)

        # Кнопка для завершения хода
        self.finalize_button = QPushButton("Завершить ход")
        layout.addWidget(self.finalize_button)
        self.finalize_button.clicked.connect(self.finalize_turn)

        self.update_info()

    def update_info(self):
        current_player = self.game.get_current_player() or "N/A"
        if self.game.current_point_index < len(self.game.points_sequence):
            next_point = self.game.points_sequence[self.game.current_point_index]
        else:
            next_point = "Ход завершён"
        self.info_label.setText(f"Игрок: {current_player} | Следующее очко: {next_point}")

    def assign_point(self):
        selected_song = self.song_combo.currentText()
        points_assigned = self.game.assign_point(selected_song)
        if points_assigned is not None:
            self.spectator_window.update_table()
            self.update_info()
        else:
            self.info_label.setText("Все очки распределены. Завершите ход.")

    def finalize_turn(self):
        if self.game.is_turn_complete():
            self.game.finalize_turn()
            self.spectator_window.update_table()
            self.update_info()
        else:
            self.info_label.setText("Еще не все очки распределены.")
