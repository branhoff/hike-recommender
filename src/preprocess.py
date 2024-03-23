from typing import Any, Dict
import pandas as pd

METERS_PER_MILE = 1609.34

class TrailData:
    """Example usage:

    td = TrailData({"difficulty": ["easy"], "length": [3, 8]})
    td.filter_trails()
    td.candidate_df
    """
    def __init__(self, user_context: Dict[str, Any], fpath="../data/alltrails-data.csv", df=None):
        self.user_context = user_context
        self.fpath = fpath
        self.df = df
        if self.df is None:
            self.load_alltrails_table()
        assert set(user_context.keys()).issubset(["length", "elevation_gain", "difficulty"])

    def convert_difficulty_num2desc(self):
        desc2num = {"easy": ["1", "2", "3"], "medium": ["4", "5", "6"], "hard": ["7", "8", "9"]}
        num2desc = {"1": "easy", "2": "easy", "3": "medium", "4": "medium", "5": "medium", "6": "hard", "7": "hard", "8": "hard", "9": "hard"}
        self.user_context["_data_difficulty"] = []
        for diff in self.user_context["difficulty"]:
            self.user_context["_data_difficulty"] += desc2num[diff]

    def load_alltrails_table(self):
        self.df = pd.read_csv(self.fpath).astype({"difficulty_rating": str})[
            ['trail_id', 'name', 'state_name', "_geoloc", 'popularity', 'length', 'elevation_gain', 'difficulty_rating', 'route_type']
        ]
        self.df = self.df.query("state_name == 'Washington'").reset_index(drop=True)
        self.df["length_miles"] = self.df["length"] / METERS_PER_MILE

    def filter_trails(self) -> pd.DataFrame:
        """Filter trails based on difficulty rating, elevation, and length.
        Return full WA trails if filters lead to empty candidate list."""
        self.candidate_df = self.df.copy()
        if "difficulty" in self.user_context:
            self.convert_difficulty_num2desc()
            difficulty = self.user_context["_data_difficulty"]
            self.candidate_df = self.candidate_df.query("difficulty_rating in @difficulty")
        if "elevation_gain" in self.user_context:
            elevation_gain = self.user_context["elevation_gain"] + 300
            self.candidate_df = self.candidate_df.query("elevation_gain<elevation_gain")
        if "length" in self.user_context:
            min_length, max_length = self.user_context["length"]
            self.candidate_df = self.candidate_df.query("length_miles>=@min_length and length_miles<=@max_length")
        if self.candidate_df.empty:
            self.candidate_df = self.df.copy()
        return self.candidate_df
