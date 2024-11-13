import emoji
import json
from typing import List, Dict
import numpy as np
import os

EmojiData = Dict[str, np.ndarray]


class EmojiDict:
    """Dataset of emojis with their names."""

    def __init__(self, load_all_emojis: bool = True):
        self.all_emojis = self.get_all_emojis()
        self.data = {}

        if load_all_emojis:
            self.data = self.all_emojis_with_data("w")

    def data_given(self, given_emoji: str):
        """
        Given an emoji, return the data associated with it.
        Data includes:
            'en' : name (string) <-- important data
            'status' : status (enum)
            'E' : unicode version (number)
        """
        return emoji.EMOJI_DATA[
            given_emoji
        ]  # https://carpedm20.github.io/emoji/docs/api.html#emoji.EMOJI_DATA

    def get_all_emojis(self) -> List[str]:
        """Return a list of all emojis."""
        return list(emoji.EMOJI_DATA.keys())

    def get_emoji_map(self) -> Dict[str, EmojiData]:
        """Get all emojis with their names in a dictionary."""
        return {
            emoji: {
                "name": self.data_given(emoji)["en"],
                "embeddings": None
                if not self.data.get(emoji, None)
                else self.data[emoji]["embeddings"],
            }
            for emoji in self.all_emojis
        }

    def emoji_filter_by_status(self, emoji_map: Dict[str, EmojiData], status: str):
        if status not in emoji.STATUS:
            raise ValueError(f"Status must be one of {list(emoji.STATUS.keys())}")

        """Filter emojis by status."""
        return {
            e: name
            for e, name in emoji_map.items()
            if self.data_given(e)["status"] == emoji.STATUS[status]
        }

    def all_emojis_with_data(
        self, mode: str = "w", filters: List[str] = None, raw: bool = False
    ) -> Dict[str, EmojiData]:
        if mode not in ["r", "w"]:
            raise ValueError("Mode must be 'r' (read) or 'w' (write)")

        """Conditionally read or write all emojis with their names to a file."""
        emojis = {}

        # Get the directory of the current script file (get_all_emojis.py)
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the path to emojis.json relative to get_all_emojis.py
        json_path = os.path.join(script_dir, "data", "emojis.json")

        if raw:
            with open(json_path, "w") as f:
                json.dump(self.data, f, indent=4)
                print("✅ [get_all_emojis.py] wrote to file")
            return self.data

        with open(json_path, mode) as f:
            if mode == "r":
                return json.load(f)

            emojis = self.get_emoji_map()

            if filters:
                for filter in filters:  # pragma: no cover
                    emojis = self.emoji_filter_by_status(emojis, filter)

            json.dump(emojis, f)
            print("✅ [get_all_emojis.py] wrote to file")

        return emojis


if __name__ == "__main__":  # pragma: no cover
    emoji_dict = EmojiDict(load_all_emojis=False)
    emoji_map = emoji_dict.all_emojis_with_data("w")
    for e, d in emoji_map.items():
        print(f"{e} : {d['name']}")
