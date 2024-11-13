import pytest
from retrieval import get_all_emojis
from retrieval import config as c

emoji_dict = get_all_emojis.EmojiDict()


def test_get_emoji_data():
    first_place_medal = emoji_dict.data_given("🥇")
    assert first_place_medal["en"] == ":1st_place_medal:"


def test_all_emojis():
    emojis = emoji_dict.get_all_emojis()
    assert len(emojis) > 0


def test_emoji_map():
    emoji_map = emoji_dict.get_emoji_map()
    assert emoji_map["🥇"]["name"] == ":1st_place_medal:"


def test_emoji_filter_by_status():
    emoji_map = emoji_dict.get_emoji_map()
    emojis = emoji_dict.emoji_filter_by_status(emoji_map, "fully_qualified")
    assert len(emojis) > 0


def test_emoji_filter_by_status_bad_input():
    emoji_map = emoji_dict.get_emoji_map()
    with pytest.raises(ValueError):
        emoji_dict.emoji_filter_by_status(emoji_map, "bad_input")


def test_all_emojis_with_data_write():
    emoji_map = emoji_dict.all_emojis_with_data("w")
    assert len(emoji_map) > 0


def test_all_emojis_with_data_read():
    emoji_dict.all_emojis_with_data("w")

    emoji_map = emoji_dict.all_emojis_with_data("r")
    assert len(emoji_map) > 0


def test_all_emojis_with_data_filter(filters=["fully_qualified"]):
    emoji_dict.all_emojis_with_data("w")

    emoji_map = emoji_dict.all_emojis_with_data("r", filters)
    assert len(emoji_map) > 0


def test_all_emojis_with_data_raw():
    emoji_map = emoji_dict.all_emojis_with_data(raw=True)
    assert len(emoji_map) > 0


def test_bad_input():
    with pytest.raises(ValueError):
        emoji_dict.all_emojis_with_data(f"./retrieval/{c.RET_SAVE_DATA_FOLDER}", "x")
