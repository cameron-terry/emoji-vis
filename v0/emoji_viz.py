import numpy as np
import json
import random
from retrieval.get_all_emojis import EmojiDict
import preprocessing.tsne_exp as tsne
import visual.basic_interactive as interactive


def build_coordinates(e_dict: EmojiDict, seed=42):
    random.seed(seed)

    embeddings = []
    emojis = []

    # Get all the emojis from your dictionary
    dict_emojis = e_dict.all_emojis
    print("total:", len(dict_emojis))

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

    # save the dictionary
    emoji_coordinates_json_rep = {}
    for emoji, (x, y) in emoji_coordinates.items():
        emoji_coordinates_json_rep[emoji] = {"x": float(x), "y": float(y)}

    with open(f"emoji_coordinates_{SEED}_{SUBSET_SIZE}.json", "w") as f:
        json.dump(emoji_coordinates_json_rep, f)

    return embeddings_2d, emojis


if __name__ == "__main__":
    SEED = 42
    SUBSET_SIZE = 1000

    emoji_dict = EmojiDict(read=True, source="emojis_unform.json")
    neutral_emoji_data = emoji_dict.emoji_remove_by_name_substr(
        emoji_dict.get_emoji_map(), "tone"
    )
    single_emoji_data = emoji_dict.emoji_remove_by_name_substr(
        neutral_emoji_data, "facing_right"
    )
    emoji_dict.set_data(single_emoji_data)

    embeddings_2d, emojis = build_coordinates(emoji_dict, seed=SEED)
    interactive.plot_embeddings(embeddings_2d, emojis, (1600, 1200))
