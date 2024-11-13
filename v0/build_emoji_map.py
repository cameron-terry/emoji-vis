import numpy as np
import json
import random
from retrieval.get_all_emojis import EmojiDict
import preprocessing.tsne_exp as tsne
import visual.basic_interactive as interactive
import sys


def save_emoji_coordinates(emoji_coordinates):
    emoji_coordinates_json_rep = {}
    for emoji, (x, y) in emoji_coordinates.items():
        emoji_coordinates_json_rep[emoji] = {"x": float(x), "y": float(y)}

    with open(f"emoji_coordinates_{SEED}_{SUBSET_SIZE}.json", "w") as f:
        json.dump(emoji_coordinates_json_rep, f)


def save_subset_json(emoji_data, filename="emojis_subset_v0"):
    emoji_data_no_embeddings = emoji_data.copy()
    for emoji in emoji_data_no_embeddings:
        emoji_data_no_embeddings[emoji].pop("embeddings", None)

    with open(f"retrieval/data/{filename}.json", "w") as f:
        json.dump(emoji_data_no_embeddings, f, indent=4)


def build_coordinates(e_dict: EmojiDict, seed=42):
    random.seed(seed)

    embeddings = []
    emojis = []
    dict_emojis = e_dict.all_emojis
    print(
        f"number of emojis: {len(dict_emojis)}, coverage: {len(dict_emojis) / MAX_EMOJIS * 100:.2f}%"
    )

    # Select a random subset of emojis
    sampled_emojis = random.sample(
        dict_emojis, len(dict_emojis) if SUBSET_SIZE == -1 else SUBSET_SIZE
    )

    for emoji in sampled_emojis:
        data = emoji_dict.data[emoji]
        embedding = data["embeddings"][0]
        embeddings.append(embedding)
        emojis.append(emoji)

    # efficient computation
    embeddings = np.array(embeddings)

    # Create a dictionary to map emojis to their 2D coordinates
    emoji_coordinates = {}

    # Perform t-SNE
    embeddings_2d = tsne.fit(embeddings)

    for idx, emoji in enumerate(emojis):
        x, y = embeddings_2d[idx]
        emoji_coordinates[emoji] = (x, y)

    save_emoji_coordinates(emoji_coordinates)

    return embeddings_2d, emojis


if __name__ == "__main__":
    SEED = 42
    SUBSET_SIZE = 1000

    emoji_dict = EmojiDict(read=True, source=sys.argv[1])
    filtered_data = emoji_dict.chain_filter(
        emoji_dict.get_emoji_map(),
        [
            (emoji_dict.emoji_remove_by_name_substr, "tone"),  # skin tone
            (emoji_dict.emoji_remove_by_name_substr, "facing_right"),  # right-arrow
            (
                emoji_dict.emoji_remove_by_emoji_regex,
                r"[\U0001F1E6-\U0001F1FF]{2}",
            ),  # flags
            (emoji_dict.emoji_remove_by_name_substr, "_o\u2019clock"),  # some clocks
        ],
    )

    MAX_EMOJIS = len(emoji_dict.all_emojis)
    emoji_dict.set_data(filtered_data)
    interactive.plot_embeddings(*build_coordinates(emoji_dict, seed=SEED), (1600, 1200))

    save_subset_json(filtered_data)
