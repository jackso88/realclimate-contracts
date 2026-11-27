"""Commands and payloads exchanged with the database service over Kafka.

Services never touch the database themselves. A service sends a command
envelope to ``DB_REQUESTS`` with ``reply_to`` set to ``DB_RESPONSES`` and a
correlation ID; the database service answers on ``DB_RESPONSES`` with a result
envelope carrying the same correlation ID, or with ``error`` set on failure.
"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

ABSENT_ARTICLES_GET = "absent_articles.get"
ABSENT_ARTICLES_REPLACE = "absent_articles.replace"
ABSENT_ARTICLES_IMPORT_LEGACY = "absent_articles.import_legacy"
ABSENT_ARTICLES_STATE = "absent_articles.state"
DB_ACK = "db.ack"

ArticleCode = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class DbContract(BaseModel):
    """Base class for database-service payloads: immutable and strict."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class ArticleSet(DbContract):
    """A set of article codes, normalized to a sorted list without duplicates.

    Args:
        articles: Article codes; whitespace is stripped and duplicates removed.
    """

    articles: list[ArticleCode] = Field(default_factory=list)

    @field_validator("articles")
    @classmethod
    def _sorted_unique(cls, value: list[str]) -> list[str]:
        return sorted(set(value))


class AbsentArticlesReplace(ArticleSet):
    """Payload of ``absent_articles.replace``: the complete tracked set."""


class AbsentArticlesImportLegacy(ArticleSet):
    """Payload of ``absent_articles.import_legacy``: state read from old Kafka."""


class AbsentArticlesState(ArticleSet):
    """Payload of ``absent_articles.state``, the answer to ``absent_articles.get``.

    Args:
        legacy_import_done: Whether the old Kafka state has already been imported.
    """

    legacy_import_done: bool
