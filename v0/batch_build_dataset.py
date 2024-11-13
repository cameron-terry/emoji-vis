from preprocessing import get_embeddings
from retrieval import get_all_emojis
from tqdm import tqdm

emb = get_embeddings.Embedder()
emoji_dict = get_all_emojis.EmojiDict()

try:
    for emoji, data in tqdm(emoji_dict.data.items(), desc="Embedding emojis"):
        emoji_dict.data[emoji]["embeddings"] = emb.get_embeddings(data["name"]).tolist()
except Exception as e:
    print(e)
except KeyboardInterrupt:
    print("Interrupted by user")

emoji_dict.all_emojis_with_data(raw=True)
