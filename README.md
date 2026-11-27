# realclimate-contracts

Shared message contracts for the realclimate services: the Kafka `Envelope`,
the topic registry and the pydantic payload models that services exchange.
Services import these instead of importing each other.

## Contents

| Module | Purpose |
| --- | --- |
| `realclimate_contracts.Envelope` | Transport envelope for every Kafka message |
| `realclimate_contracts.topics` | Names of all Kafka topics |
| `realclimate_contracts.db` | Commands and payloads for the database service |

## Using the package

Add the dependency to a service with a version tag:

```toml
[project]
dependencies = [
    "realclimate-contracts @ git+https://github.com/jackso88/realclimate-contracts.git@v0.1.0",
]
```

Then import from it:

```python
from realclimate_contracts import Envelope
from realclimate_contracts.topics import DB_REQUESTS
```

## Releasing

Every pull request that changes `src/` must bump `version` in `pyproject.toml`
(CI enforces this). After the pull request is merged into `main`, the
`Release` workflow runs the tests, builds the package and publishes a GitHub
release tagged `v<version>` with the wheel and sdist attached. Nothing has to be
released by hand.

Contract changes should stay backwards compatible within a deployment: add new
optional fields first, switch consumers, and only then remove old ones.

## Development

```bash
poetry install --with dev
poetry run black src tests
poetry run pytest --cov
```
