from src.library import singleton
from src.services.postgres.pg_category_data_provider import PgCategoryDataProvider
from src.services.postgres.pg_event_data_provider import PgEventDataProvider
from src.services.postgres.pg_participant_data_provider import PgParticipantDataProvider


@singleton
class PgDataBase(PgParticipantDataProvider, PgCategoryDataProvider, PgEventDataProvider):

    def __init__(self) -> None:
        super().__init__()
