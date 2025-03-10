# spectator_window.py
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QFont

# Layout and style constants
CELL_SPACING = 10    # vertical gap between cells
MARGIN = 10          # margin for the container
INFO_HEIGHT = 50     # Height for the bottom info cell

# New constants for the voting scoreboard design:
SONG_WIDTH = 800
SONG_HEIGHT = 80
LEFT_WIDTH = 100
RIGHT_WIDTH = 700  # SONG_WIDTH = LEFT_WIDTH + RIGHT_WIDTH

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
        color2 = QColor(80, 0, 80)    # Deep purple
        gradient.setColorAt(0.0, color1)
        gradient.setColorAt(self.gradient_offset, color2)
        gradient.setColorAt(1.0, color1)
        painter.fillRect(rect, gradient)

    def update_layout(self, initial=False):
        container_width = self.width()
        # Center the voting scoreboard horizontally.
        x_pos = (container_width - SONG_WIDTH) // 2

        # When the turn is complete, re-sort the songs.
        if self.game.is_turn_complete():
            self.cached_order = sorted(
                self.game.songs,
                key=lambda s: self.game.total_scores[s] + self.game.current_scores[s],
                reverse=True
            )
        sorted_songs = self.cached_order
        n = len(sorted_songs)
        for i, song in enumerate(sorted_songs):
            new_rect = QRect(
                x_pos,
                MARGIN + i * (SONG_HEIGHT + CELL_SPACING),
                SONG_WIDTH,
                SONG_HEIGHT
            )
            cell = self.song_cells[song]
            if initial:
                cell.setGeometry(new_rect)
            else:
                self.animate_move(cell, new_rect)

        # Position the info cell at the bottom of the screen.
        container_height = self.height()
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
            # Replace "Player:" with "Сейчас голосует:" in the status text.
            text = text.replace("Player:", "Сейчас голосует:")
            self.label.setText(text)

        def resizeEvent(self, event):
            self.label.setGeometry(0, 0, self.width(), self.height())

    class SongCell(QWidget):
        """
        Displays one song's information as a voting block.
        The block is fixed at 800pt x 80pt and divided into:
          - LEFT (100pt wide): Shows the total points (center-aligned, background HEX #1b0f2a)
          - RIGHT (700pt wide): Shows the song details (left-aligned, background HEX #3b2643 at 50% opacity)
        Awarded points (e.g. +1, +3, +6, +9) are shown in HEX #98efff.
        The song name is split at the hyphen and only the first part is shown,
        with an additional 10pt left padding.
        """
        def __init__(self, song, original_number, parent=None):
            super().__init__(parent)
            self.song = song
            self.original_number = original_number
            self.force_highlight = False  # (Not used in this version but preserved for further extensions.)

            # Create two labels for the two visual sectors.
            self.left_label = QLabel(self)
            self.right_label = QLabel(self)

            # Set alignments for each sector.
            self.left_label.setAlignment(Qt.AlignCenter)
            self.right_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            # Enable rich text formatting so HTML tags are rendered.
            self.right_label.setTextFormat(Qt.RichText)

            # Set the specified font: Helvetica Neue Bold, 40pt.
            font = QFont("Helvetica Neue", 40, QFont.Bold)
            self.left_label.setFont(font)
            self.right_label.setFont(font)

            # Set fixed geometry for the two sectors.
            self.left_label.setGeometry(0, 0, LEFT_WIDTH, SONG_HEIGHT)
            self.right_label.setGeometry(LEFT_WIDTH, 0, RIGHT_WIDTH, SONG_HEIGHT)

            # Apply the background colors.
            self.left_label.setStyleSheet("background-color: #1b0f2a; color: white;")
            # For 50% opacity, we use rgba with alpha 127 (out of 255).
            self.right_label.setStyleSheet("background-color: rgba(59, 38, 67, 127); color: white;")

        def update_data(self, total, current):
            # Compute the display total.
            display_total = total + current
            # LEFT sector: display the total points.
            self.left_label.setText(str(display_total))
            # Process the song name: split at the hyphen and keep only the first part.
            song_name = self.song.split('-')[0].strip()
            
            # RIGHT sector: song details (original number and song title)
            # Add 10pt spacing before the song name using Qt's spacing mechanisms
            # We'll use a non-breaking space (&nbsp;) for consistent spacing
            spacing = "&nbsp;" * 5  # Each &nbsp; is approximately 2pt in width
            
            if current:
                text = f"{spacing}{song_name}&nbsp;&nbsp;<span style='color:#98efff;'>+{current}</span>"
            else:
                text = f"{spacing}{song_name}"
                
            self.right_label.setText(text)
            
            # Ensure the right label has proper margins
            self.right_label.setContentsMargins(10, 0, 0, 0)

        def resizeEvent(self, event):
            # Ensure the left and right sectors remain correctly sized if the cell is resized.
            self.left_label.setGeometry(0, 0, LEFT_WIDTH, self.height())
            self.right_label.setGeometry(LEFT_WIDTH, 0, self.width() - LEFT_WIDTH, self.height())

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
