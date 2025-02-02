import os

class Game:
    def __init__(self, songs_file, players_file):
        self.songs = []            # List of songs
        self.players = []          # List of players
        self.total_scores = {}     # Total score for each song
        self.current_scores = {}   # Current turn score for each song
        self.points_sequence = [1, 3, 6, 9]  # Sequence of points to assign
        self.current_point_index = 0         # Index of the next point to assign
        self.current_player_index = 0        # Index of the current player
        self.original_order = {}             # Original order of songs (song: index)
        self.game_over = False               # Flag to end the game after the last player

        self.load_songs(songs_file)
        self.load_players(players_file)

        # Initialize scores and store original order
        for index, song in enumerate(self.songs):
            self.total_scores[song] = 0
            self.current_scores[song] = 0
            self.original_order[song] = index

    def load_songs(self, songs_file):
        if os.path.exists(songs_file):
            with open(songs_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.songs = [line.strip() for line in lines if line.strip()]
        else:
            self.songs = []

    def load_players(self, players_file):
        if os.path.exists(players_file):
            with open(players_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.players = [line.strip() for line in lines if line.strip()]
        else:
            self.players = []

    def get_current_player(self):
        if self.players:
            return self.players[self.current_player_index]
        return None

    def assign_point(self, song_name):
        """Assigns the next point in the sequence to the chosen song."""
        if self.game_over:
            return None
        if self.current_point_index < len(self.points_sequence):
            points = self.points_sequence[self.current_point_index]
            self.current_scores[song_name] += points
            self.current_point_index += 1
            return points
        else:
            return None

    def is_turn_complete(self):
        """Checks if all points have been distributed for the current turn."""
        return self.current_point_index >= len(self.points_sequence)

    def finalize_turn(self):
        """Transfers the current turn's scores to total scores, resets the turn,
           and advances to the next player. (Note: The presenter’s song order is not changed.)
        """
        if self.game_over:
            return
        for song in self.songs:
            self.total_scores[song] += self.current_scores[song]
            self.current_scores[song] = 0
        self.current_point_index = 0
        if self.current_player_index == len(self.players) - 1:
            self.game_over = True
        else:
            self.current_player_index += 1

    def reset_turn(self):
        """Resets the current turn's scores without transferring them to total scores."""
        if self.game_over:
            return
        for song in self.songs:
            self.current_scores[song] = 0
        self.current_point_index = 0