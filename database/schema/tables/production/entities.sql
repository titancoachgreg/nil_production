create table entity_types (
    id bigserial not null primary key,
    name varchar(255) not null,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table entities (
    id bigserial not null primary key,
    entity_type_id bigint references entity_types(id) on delete restrict,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);