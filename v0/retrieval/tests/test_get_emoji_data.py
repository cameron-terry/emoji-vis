import pytest
from retrieval import get_all_emojis
from retrieval import config as c


def test_get_emoji_data():
    first_place_medal = get_all_emojis.data_given("🥇")
    assert first_place_medal["en"] == ":1st_place_medal:"


def test_all_emojis():
    emojis = get_all_emojis.all_emojis()
    assert len(emojis) > 0


def test_emoji_map():
    emoji_map = get_all_emojis.emoji_map()
    assert emoji_map["🥇"] == ":1st_place_medal:"


def test_emoji_filter_by_status():
    emoji_map = get_all_emojis.emoji_map()
    emojis = get_all_emojis.emoji_filter_by_status(emoji_map, "fully_qualified")
    assert len(emojis) > 0


def test_all_emojis_with_data_write():
    emoji_map = get_all_emojis.all_emojis_with_data(
        f"./retrieval/{c.RET_SAVE_DATA_FOLDER}", "w"
    )
    assert len(emoji_map) > 0


def test_all_emojis_with_data_read():
    # Write first
    get_all_emojis.all_emojis_with_data(f"./retrieval/{c.RET_SAVE_DATA_FOLDER}", "w")

    emoji_map = get_all_emojis.all_emojis_with_data(
        f"./retrieval/{c.RET_SAVE_DATA_FOLDER}", "r"
    )
    assert len(emoji_map) > 0


def test_all_emojis_with_data_filter(filters=["fully_qualified"]):
    # Write first
    get_all_emojis.all_emojis_with_data(f"./retrieval/{c.RET_SAVE_DATA_FOLDER}", "w")

    emoji_map = get_all_emojis.all_emojis_with_data(
        f"./retrieval/{c.RET_SAVE_DATA_FOLDER}", "r", filters
    )
    assert len(emoji_map) > 0


def test_bad_input():
    with pytest.raises(ValueError):
        get_all_emojis.all_emojis_with_data(
            f"./retrieval/{c.RET_SAVE_DATA_FOLDER}", "x"
        )
