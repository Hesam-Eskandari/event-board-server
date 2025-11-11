CREATE TABLE event_board.event (
    id              UUID PRIMARY KEY NOT NULL,
    title           VARCHAR(100) NOT NULL,
    start           TIMESTAMP WITH TIME ZONE NOT NULL,
    "end"           TIMESTAMP WITH TIME ZONE NOT NULL,
    category_id     UUID NOT NULL,
    participant_id  UUID NOT NULL,
    is_deleted      BOOLEAN NOT NULL,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_category
    FOREIGN KEY(category_id)
        REFERENCES event_board.category(id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_participant
    FOREIGN KEY(participant_id)
        REFERENCES event_board.participant(id)
        ON DELETE RESTRICT
);

CREATE INDEX event_is_deleted_category ON event_board.event(is_deleted, category_id);
CREATE INDEX event_is_deleted_participant ON event_board.event(is_deleted, participant_id);
CREATE INDEX event_is_deleted_start ON event_board.event(is_deleted, start);
CREATE INDEX event_is_deleted_end ON event_board.event(is_deleted, "end");
CREATE INDEX event_is_deleted_title ON event_board.event(is_deleted, title);
