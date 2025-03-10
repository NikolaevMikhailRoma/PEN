# presenter_window.py
from PyQt5 import QtWidgets, QtCore

class PresenterWindow(QtWidgets.QMainWindow):
    def __init__(self, game, spectator_window):
        super().__init__()
        self.game = game
        self.spectator_window = spectator_window
        self.setWindowTitle("Presenter Window")
        # Set a larger initial size to accommodate all song buttons.
        self.resize(600, 600)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        self.main_layout = QtWidgets.QVBoxLayout()
        central.setLayout(self.main_layout)

        # Information label displaying current player and next point.
        self.info_label = QtWidgets.QLabel("")
        self.main_layout.addWidget(self.info_label)

        # Create a scroll area for the song buttons.
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Container for song buttons.
        self.buttons_container = QtWidgets.QWidget()
        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.buttons_container.setLayout(self.buttons_layout)
        self.scroll_area.setWidget(self.buttons_container)

        # Create buttons for each song in the original order.
        self.create_song_buttons()

        # Layout for control buttons.
        self.control_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.control_layout)

        # Button to finalize the turn.
        self.finalize_button = QtWidgets.QPushButton("Finalize Turn")
        self.control_layout.addWidget(self.finalize_button)
        self.finalize_button.clicked.connect(self.finalize_turn)

        # Button to reset the current turn.
        self.reset_button = QtWidgets.QPushButton("Reset Turn")
        self.control_layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.reset_turn)

        self.update_info()

    def create_song_buttons(self):
        # Clear existing buttons if any.
        for i in reversed(range(self.buttons_layout.count())):
            widget = self.buttons_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Create a button for each song in original order.
        for song in self.game.songs:
            original_number = self.game.original_order[song] + 1
            button_text = f"({original_number}) {song}"
            button = QtWidgets.QPushButton(button_text)
            button.clicked.connect(lambda checked, s=song: self.assign_point(s))
            self.buttons_layout.addWidget(button)

    def update_info(self):
        if self.game.game_over:
            info_text = "Game Over"
        else:
            current_player = self.game.get_current_player() or "N/A"
            if self.game.current_point_index < len(self.game.points_sequence):
                next_point = self.game.points_sequence[self.game.current_point_index]
            else:
                next_point = "Turn complete"
            info_text = f"Player: {current_player} | Next Point: {next_point}"
        self.info_label.setText(info_text)
        # Also update spectator status cell.
        self.spectator_window.update_status(info_text)

    def assign_point(self, song):
        if self.game.game_over:
            self.info_label.setText("Game is over. No more points can be assigned.")
            return
        points_assigned = self.game.assign_point(song)
        if points_assigned is not None:
            # Instead of calling highlight_vote, update the last voted song so that it remains highlighted.
            self.spectator_window.update_last_voted(song)
            self.spectator_window.update_view()
            self.update_info()
        else:
            self.info_label.setText("All points have been distributed. Finalize turn.")

    def finalize_turn(self):
        if self.game.game_over:
            self.info_label.setText("Game is over.")
            return
        if self.game.is_turn_complete():
            self.game.finalize_turn()
            self.spectator_window.update_view()
            self.update_info()
        else:
            self.info_label.setText("Not all points have been assigned yet.")

    def reset_turn(self):
        if self.game.game_over:
            self.info_label.setText("Game is over.")
            return
        self.game.reset_turn()
        self.spectator_window.update_view()
        self.update_info()