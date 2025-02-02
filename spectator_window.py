# spectator_window.py
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QFont

# Layout and style constants
CELL_SPACING = 10
MARGIN = 10
INFO_HEIGHT = 50  # Height for the bottom info cell


class SpectatorContainer(QWidget):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.game = game
        self.gradient_offset = 0.0  # For the shimmering background effect
        # Cached ordering: initially based on finalized scores (plus current, which is zero)
        self.cached_order = sorted(
            self.game.songs,
            key=lambda s: self.game.total_scores[s] + self.game.current_scores[s],
            reverse=True
        )
        # Keep track of the last voted song (if any)
        self.last_voted_song = None

        # Create the info cell (for additional game information) at the bottom of the screen.
        self.info_cell = self.InfoCell(self)
        # Create a SongCell for each song (keyed by song name)
        self.song_cells = {}
        for song in self.game.songs:
            original_number = self.game.original_order[song] + 1
            cell = self.SongCell(song, original_number, self)
            cell.update_data(self.game.total_scores[song], self.game.current_scores[song])
            self.song_cells[song] = cell

        # Timer to update the shimmering background.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gradient)
        self.timer.start(50)  # Update every 50ms

        self.update_layout(initial=True)

    def update_gradient(self):
        self.gradient_offset += 0.01
        if self.gradient_offset > 1.0:
            self.gradient_offset = 0.0
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        # Create a horizontal linear gradient with shifting stops for a shimmering effect.
        gradient = QLinearGradient(0, 0, rect.width(), 0)
        color1 = QColor(30, 30, 60)  # Dark blue
        color2 = QColor(80, 0, 80)  # Deep purple
        gradient.setColorAt(0.0, color1)
        gradient.setColorAt(self.gradient_offset, color2)
        gradient.setColorAt(1.0, color1)
        painter.fillRect(rect, gradient)

    def update_layout(self, initial=False):
        container_width = self.width()
        container_height = self.height()

        # --- Determine ordering ---
        # Only update the ordering (i.e. re-sort) when the turn is complete.
        if self.game.is_turn_complete():
            self.cached_order = sorted(
                self.game.songs,
                key=lambda s: self.game.total_scores[s] + self.game.current_scores[s],
                reverse=True
            )
        sorted_songs = self.cached_order

        n = len(sorted_songs)
        # For two columns: left column gets the first half, right column the rest.
        left_count = (n + 1) // 2
        right_count = n - left_count
        max_rows = max(left_count, right_count)

        # --- Allocate vertical space for songs ---
        # Use the top two-thirds of the container for the songs.
        available_songs_height = int(container_height * 2 / 3) - MARGIN
        # Compute the row height so that max_rows cells and CELL_SPACING gaps fit evenly.
        row_height = 0
        if max_rows > 0:
            row_height = (available_songs_height - (max_rows - 1) * CELL_SPACING) / max_rows

        # --- Position left-column song cells ---
        for i in range(left_count):
            song = sorted_songs[i]
            new_rect = QRect(
                MARGIN,
                MARGIN + int(i * (row_height + CELL_SPACING)),
                (container_width - 3 * MARGIN) // 2,
                int(row_height)
            )
            cell = self.song_cells[song]
            if initial:
                cell.setGeometry(new_rect)
            else:
                self.animate_move(cell, new_rect)

        # --- Position right-column song cells ---
        for i in range(right_count):
            song = sorted_songs[left_count + i]
            new_rect = QRect(
                MARGIN * 2 + (container_width - 3 * MARGIN) // 2,
                MARGIN + int(i * (row_height + CELL_SPACING)),
                (container_width - 3 * MARGIN) // 2,
                int(row_height)
            )
            cell = self.song_cells[song]
            if initial:
                cell.setGeometry(new_rect)
            else:
                self.animate_move(cell, new_rect)

        # --- Position the info cell at the bottom of the screen ---
        info_width = min(300, container_width - 20)
        info_x = (container_width - info_width) // 2
        info_y = container_height - INFO_HEIGHT - MARGIN
        self.info_cell.setGeometry(info_x, info_y, info_width, INFO_HEIGHT)

    def animate_move(self, widget, new_rect):
        anim = QPropertyAnimation(widget, b"geometry")
        anim.setDuration(500)
        anim.setStartValue(widget.geometry())
        anim.setEndValue(new_rect)
        anim.start()
        widget.animation = anim  # Keep a reference to avoid garbage collection

    def update_cells(self):
        # If no points have been assigned in the current round, clear last voted highlight.
        if self.game.current_point_index == 0:
            self.last_voted_song = None
        # Update each SongCell's displayed score and highlight flag.
        for song, cell in self.song_cells.items():
            cell.force_highlight = (song == self.last_voted_song)
            total = self.game.total_scores[song]
            current = self.game.current_scores[song]
            cell.update_data(total, current)
        # Update layout only when the voting round is complete.
        if self.game.is_turn_complete():
            self.update_layout(initial=False)

    def update_last_voted(self, song):
        """Call this method externally (e.g. from the presenter) whenever a vote is cast."""
        self.last_voted_song = song
        self.update_cells()

    def resizeEvent(self, event):
        self.update_layout(initial=True)

    # --- Inner Classes ---
    class InfoCell(QWidget):
        """A small info window with visible edges, positioned at the bottom of the screen."""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.label = QLabel(self)
            self.label.setAlignment(Qt.AlignCenter)
            font = QFont("Arial", 14)
            self.label.setFont(font)
            self.label.setStyleSheet("color: white;")
            self.setStyleSheet(
                "background-color: rgba(20, 20, 20, 180);"
                "border: 2px solid white; border-radius: 5px;"
            )

        def update_status(self, text):
            self.label.setText(text)

        def resizeEvent(self, event):
            self.label.setGeometry(0, 0, self.width(), self.height())

    class SongCell(QWidget):
        """Displays one song’s information on one line (number, title, and score—with current round in parentheses).
           If the cell’s force_highlight flag is True, it remains highlighted even if its current score is zero.
        """

        def __init__(self, song, original_number, parent=None):
            super().__init__(parent)
            self.song = song
            self.original_number = original_number
            self.force_highlight = False  # Persistent highlight flag.
            self.label = QLabel(self)
            self.label.setAlignment(Qt.AlignCenter)
            font = QFont("Arial", 14)
            self.label.setFont(font)
            # Neat dark semi-transparent background with a gray border.
            self.default_color = "rgba(50, 50, 50, 180)"
            self.highlight_color = "rgba(100, 100, 200, 220)"
            self.setStyleSheet(f"background-color: {self.default_color}; border: 1px solid gray;")
            self.label.setStyleSheet("color: white;")

        def update_data(self, total, current):
            # Display the combined score; if current round points exist, show them in parentheses.
            display_total = total + current
            if current:
                text = f"({self.original_number}) {self.song} | {display_total} ({current})"
            else:
                text = f"({self.original_number}) {self.song} | {display_total}"
            self.label.setText(text)
            # If the song received any current points or if force_highlight is True, highlight the cell.
            if current > 0 or self.force_highlight:
                self.setStyleSheet(f"background-color: {self.highlight_color}; border: 1px solid gray;")
            else:
                self.setStyleSheet(f"background-color: {self.default_color}; border: 1px solid gray;")

        def resizeEvent(self, event):
            self.label.setGeometry(0, 0, self.width(), self.height())


class SpectatorWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setWindowTitle("Spectator Window")
        self.resize(800, 600)  # A large, resizable window

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.setCentralWidget(self.scroll_area)

        self.container = SpectatorContainer(self.game)
        self.scroll_area.setWidget(self.container)

    def update_view(self):
        self.container.update_cells()

    def update_status(self, status_text):
        self.container.info_cell.update_status(status_text)

    def update_last_voted(self, song):
        """Delegate update of the last voted song to the container."""
        self.container.update_last_voted(song)

    def set_background(self, customizer):
        customizer.apply_background(self.container)
