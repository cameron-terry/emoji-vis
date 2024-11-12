from retrieval import get_all_emojis


def test_get_emoji_data():
    first_place_medal = get_all_emojis.data_given("🥇")
    assert first_place_medal["en"] == ":1st_place_medal:"
