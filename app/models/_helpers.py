from uuid import UUID

import ulid


def uuid_factory() -> UUID:
    return ulid.new().uuid
