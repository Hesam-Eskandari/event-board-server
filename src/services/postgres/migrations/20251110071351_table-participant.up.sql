CREATE TABLE event_board.participant (
    id              UUID PRIMARY KEY NOT NULL,
    firstname       VARCHAR(100) NOT NULL,
    lastname        VARCHAR(100) NOT NULL,
    image_url       VARCHAR(100) NOT NULL,
    is_deleted      BOOLEAN NOT NULL,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);


CREATE INDEX participant_is_deleted_idx ON event_board.participant(is_deleted);