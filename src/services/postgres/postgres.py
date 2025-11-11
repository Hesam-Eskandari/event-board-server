from src.library import singleton
from src.services.postgres.pg_category import PgCategoryDataProvider
from src.services.postgres.pg_event import PgEventDataProvider
from src.services.postgres.pg_participant import PgParticipantDataProvider


@singleton
class PgDataBase(PgParticipantDataProvider, PgCategoryDataProvider, PgEventDataProvider):

    def __init__(self) -> None:
        super().__init__()
