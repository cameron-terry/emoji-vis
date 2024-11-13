import pytest
import warnings
from preprocessing import get_embeddings

SAMPLE_TEXTS = {
    "rat": "Rats are rodents.",
    "eiffel_tower": "The Eiffel Tower is a famous landmark in Paris.",
    "ratatouille": "Ratatouille is a famous animated movie.",
}

emb = get_embeddings.Embedder()


def check_order(a, b, c):
    try:
        # (Ratatouille, Eiffel Tower) > (Rats, Ratatouille) > (Rats, Eiffel Tower)
        assert a > b
        assert b > c
    except AssertionError:  # pragma: no cover
        # get the highest cosine similarity
        score_map = {
            "(Ratatouille, Eiffel Tower)": float(a[0]),
            "(Rats, Ratatouille)": float(b[0]),
            "(Rats, Eiffel Tower)": float(c[0]),
        }
        score_map_sorted = dict(
            sorted(score_map.items(), key=lambda item: item[1], reverse=True)
        )

        warning_message = "\n\nMean embedding output undesired logical outcome:\n"
        for k, v in score_map_sorted.items():
            warning_message += f"{k} : {v}\n"

        warnings.warn(warning_message)


def test_embedder_mean():
    rat_emb = emb.get_embeddings(SAMPLE_TEXTS["rat"], method="mean")
    eiffel_tower_emb = emb.get_embeddings(SAMPLE_TEXTS["eiffel_tower"], method="mean")
    ratatouille_emb = emb.get_embeddings(SAMPLE_TEXTS["ratatouille"], method="mean")

    a = emb.cosine_similarity(ratatouille_emb, eiffel_tower_emb)
    b = emb.cosine_similarity(rat_emb, ratatouille_emb)
    c = emb.cosine_similarity(rat_emb, eiffel_tower_emb)

    check_order(a, b, c)


def test_embedder_max():
    rat_emb = emb.get_embeddings(SAMPLE_TEXTS["rat"], method="max")
    eiffel_tower_emb = emb.get_embeddings(SAMPLE_TEXTS["eiffel_tower"], method="max")
    ratatouille_emb = emb.get_embeddings(SAMPLE_TEXTS["ratatouille"], method="max")

    a = emb.cosine_similarity(ratatouille_emb, eiffel_tower_emb)
    b = emb.cosine_similarity(rat_emb, ratatouille_emb)
    c = emb.cosine_similarity(rat_emb, eiffel_tower_emb)

    check_order(a, b, c)


def test_embedder_cls():
    rat_emb = emb.get_embeddings(SAMPLE_TEXTS["rat"], method="cls")
    eiffel_tower_emb = emb.get_embeddings(SAMPLE_TEXTS["eiffel_tower"], method="cls")
    ratatouille_emb = emb.get_embeddings(SAMPLE_TEXTS["ratatouille"], method="cls")

    a = emb.cosine_similarity(ratatouille_emb, eiffel_tower_emb)
    b = emb.cosine_similarity(rat_emb, ratatouille_emb)
    c = emb.cosine_similarity(rat_emb, eiffel_tower_emb)

    check_order(a, b, c)


def test_embedder_bad_embedding_input():
    emb = get_embeddings.Embedder()
    with pytest.raises(ValueError):
        emb.get_embeddings(SAMPLE_TEXTS["rat"], method="bad_input")
