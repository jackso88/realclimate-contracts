"""Tests for the database-service command contracts."""

import pytest
from pydantic import ValidationError

from realclimate_contracts import Envelope
from realclimate_contracts.db import (
    ABSENT_ARTICLES_REPLACE,
    AbsentArticlesImportLegacy,
    AbsentArticlesReplace,
    AbsentArticlesState,
)
from realclimate_contracts.topics import DB_RESPONSES


def test_articles_are_stripped_deduplicated_and_sorted():
    payload = AbsentArticlesReplace(articles=[" NC-2 ", "NC-1", "NC-2"])

    assert payload.articles == ["NC-1", "NC-2"]


def test_articles_default_to_an_empty_list():
    assert AbsentArticlesReplace().articles == []
    assert AbsentArticlesImportLegacy().articles == []


@pytest.mark.parametrize("bad", ["", "   "])
def test_blank_article_codes_are_rejected(bad):
    with pytest.raises(ValidationError):
        AbsentArticlesReplace(articles=[bad])


def test_unknown_fields_are_rejected():
    with pytest.raises(ValidationError):
        AbsentArticlesReplace(articles=[], unexpected=True)


def test_payloads_are_immutable():
    payload = AbsentArticlesReplace(articles=["NC-1"])

    with pytest.raises(ValidationError):
        payload.articles = []


def test_state_requires_the_legacy_import_flag():
    with pytest.raises(ValidationError):
        AbsentArticlesState(articles=["NC-1"])

    state = AbsentArticlesState(articles=["NC-1"], legacy_import_done=True)
    assert state.legacy_import_done is True


def test_payload_survives_an_envelope_round_trip():
    request = Envelope.create(
        ABSENT_ARTICLES_REPLACE,
        AbsentArticlesReplace(articles=["NC-2", "NC-1"]).model_dump(mode="json"),
        correlation_id="corr-1",
        reply_to=DB_RESPONSES,
    )

    received = Envelope.decode(request.encode())
    parsed = AbsentArticlesReplace.model_validate(received.payload)

    assert parsed.articles == ["NC-1", "NC-2"]
    assert received.reply_to == DB_RESPONSES
