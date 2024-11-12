import emoji
import json
from typing import List, Dict


def data_given(given_emoji: str):
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


def all_emojis() -> List[str]:
    """Return a list of all emojis."""
    return list(emoji.EMOJI_DATA.keys())


def emoji_map() -> Dict[str, str]:
    """Get all emojis with their names in a dictionary."""
    return {emoji: data_given(emoji)["en"] for emoji in all_emojis()}


def emoji_filter_by_status(emoji_map: Dict[str, str], status: str):
    if status not in emoji.STATUS:
        raise ValueError(f"Status must be one of {list(emoji.STATUS.keys())}")

    """Filter emojis by status."""
    return {
        e: name
        for e, name in emoji_map.items()
        if data_given(e)["status"] == emoji.STATUS[status]
    }


def all_emojis_with_data(
    dir: str, mode: str, filters: List[str] = None
) -> Dict[str, str]:
    if mode not in ["r", "w"]:
        raise ValueError("Mode must be 'r' (read) or 'w' (write)")

    """Conditionally read or write all emojis with their names to a file."""
    emojis = {}
    with open(f"{dir}/emojis.json", mode) as f:
        if mode == "r":
            return json.load(f)

        emojis = emoji_map()

        if filters:
            for filter in filters:  # pragma: no cover
                emojis = emoji_filter_by_status(emojis, filter)

        json.dump(emojis, f)

    print(f"✅ Saved emojis to {dir}/emojis.json")
    return emojis


if __name__ == "__main__":  # pragma: no cover
    import config as c

    emoji_map = all_emojis_with_data(c.RET_SAVE_DATA_FOLDER, "w")
    for emoji, name in emoji_map.items():
        print(f"{emoji} : {name}")
