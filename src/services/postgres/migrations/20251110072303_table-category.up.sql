CREATE TABLE event_board.category (
    id              UUID PRIMARY KEY NOT NULL,
    title           VARCHAR(100) NOT NULL UNIQUE,
    is_deleted      BOOLEAN NOT NULL,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX category_not_deleted_title_idx ON event_board.category(is_deleted, title);
