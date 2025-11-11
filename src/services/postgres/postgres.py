from src.library import singleton
from src.services.postgres.pg_category import PgCategoryDataProvider
from src.services.postgres.pg_participant import PgParticipantDataProvider


@singleton
class PgDataBase(PgParticipantDataProvider, PgCategoryDataProvider):

    def __init__(self) -> None:
        super().__init__()
        self._setup_connection()
