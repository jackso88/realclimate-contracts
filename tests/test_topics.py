"""Tests for the shared Kafka topic registry."""

import re

from realclimate_contracts import topics

TOPIC_PATTERN = re.compile(r"^[a-z0-9]+([._-][a-z0-9]+)*$")


def registered_topics() -> dict[str, str]:
    return {
        name: value
        for name, value in vars(topics).items()
        if name.isupper() and isinstance(value, str)
    }


def test_topic_names_are_unique():
    values = list(registered_topics().values())

    assert len(values) == len(set(values))


def test_topic_names_are_valid_for_kafka():
    for name, value in registered_topics().items():
        assert TOPIC_PATTERN.match(value), f"{name} has an unusual topic name"


def test_database_request_reply_topics_are_registered():
    assert topics.DB_REQUESTS == "db.requests"
    assert topics.DB_RESPONSES == "db.responses"
