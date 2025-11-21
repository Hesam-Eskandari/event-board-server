CREATE TABLE tenant.token (
    id              UUID PRIMARY KEY NOT NULL,
    tenant_id       UUID NOT NULL,
    application     VARCHAR(100) NOT NULL,
    role            VARCHAR(100) NOT NULL,
    type            VARCHAR(100) NOT NULL,
    version         VARCHAR(100) NOT NULL,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);


CREATE INDEX token_application_tenant_id_idx ON tenant.token(application, tenant_id);
