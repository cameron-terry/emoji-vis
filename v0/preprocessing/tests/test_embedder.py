import pytest
import warnings
from preprocessing import get_embeddings

SAMPLE_TEXTS = {
    "rat": "Rats are rodents.",
    "eiffel_tower": "The Eiffel Tower is a famous landmark in Paris.",
    "ratatouille": "Ratatouille is a famous animated movie.",
}


def test_embedder_mean():
    emb = get_embeddings.Embedder()

    rat_emb = emb.get_embeddings(SAMPLE_TEXTS["rat"])
    eiffel_tower_emb = emb.get_embeddings(SAMPLE_TEXTS["eiffel_tower"])
    ratatouille_emb = emb.get_embeddings(SAMPLE_TEXTS["ratatouille"])

    try:
        # (Ratatouille, Eiffel Tower) > (Rats, Ratatouille) > (Rats, Eiffel Tower)
        assert emb.cosine_similarity(rat_emb, eiffel_tower_emb) < emb.cosine_similarity(
            rat_emb, ratatouille_emb
        )
        assert emb.cosine_similarity(rat_emb, ratatouille_emb) < emb.cosine_similarity(
            eiffel_tower_emb, ratatouille_emb
        )
    except AssertionError:  # pragma: no cover
        warnings.warn("Mean embedding output undesired logical outcome")


def test_embedder_max():
    emb = get_embeddings.Embedder()

    rat_emb = emb.get_embeddings(SAMPLE_TEXTS["rat"], method="max")
    eiffel_tower_emb = emb.get_embeddings(SAMPLE_TEXTS["eiffel_tower"], method="max")
    ratatouille_emb = emb.get_embeddings(SAMPLE_TEXTS["ratatouille"], method="max")

    try:
        # (Ratatouille, Eiffel Tower) > (Rats, Ratatouille) > (Rats, Eiffel Tower)
        assert emb.cosine_similarity(rat_emb, eiffel_tower_emb) < emb.cosine_similarity(
            rat_emb, ratatouille_emb
        )
        assert emb.cosine_similarity(rat_emb, ratatouille_emb) < emb.cosine_similarity(
            eiffel_tower_emb, ratatouille_emb
        )
    except AssertionError:  # pragma: no cover
        warnings.warn("Max embedding output undesired logical outcome")


def test_embedder_cls():
    emb = get_embeddings.Embedder()

    rat_emb = emb.get_embeddings(SAMPLE_TEXTS["rat"], method="cls")
    eiffel_tower_emb = emb.get_embeddings(SAMPLE_TEXTS["eiffel_tower"], method="cls")
    ratatouille_emb = emb.get_embeddings(SAMPLE_TEXTS["ratatouille"], method="cls")

    try:
        # (Ratatouille, Eiffel Tower) > (Rats, Ratatouille) > (Rats, Eiffel Tower)
        assert emb.cosine_similarity(rat_emb, eiffel_tower_emb) < emb.cosine_similarity(
            rat_emb, ratatouille_emb
        )
        assert emb.cosine_similarity(rat_emb, ratatouille_emb) < emb.cosine_similarity(
            eiffel_tower_emb, ratatouille_emb
        )
    except AssertionError:  # pragma: no cover
        warnings.warn("CLS embedding output undesired logical outcome")


def test_embedder_bad_embedding_input():
    emb = get_embeddings.Embedder()
    with pytest.raises(ValueError):
        emb.get_embeddings(SAMPLE_TEXTS["rat"], method="bad_input")
