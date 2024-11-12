from preprocessing import get_embeddings


def test_embedder():
    emb = get_embeddings.Embedder()

    rat_emb = emb.get_embeddings("Rats are rodents.")
    eiffel_tower_emb = emb.get_embeddings(
        "The Eiffel Tower is a famous landmark in Paris."
    )
    ratatouille_emb = emb.get_embeddings("Ratatouille is a famous animated movie.")

    assert emb.cosine_similarity(rat_emb, eiffel_tower_emb) < emb.cosine_similarity(
        rat_emb, ratatouille_emb
    )
    assert emb.cosine_similarity(rat_emb, ratatouille_emb) < emb.cosine_similarity(
        eiffel_tower_emb, ratatouille_emb
    )
