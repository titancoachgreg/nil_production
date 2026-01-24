create table divisions (
    id bigserial not null primary key,
    name varchar(255) not null,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table conferences (
    id bigserial not null primary key,
    name varchar(255) not null,
    entity_id bigint not null references entities(id) on delete restrict,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table schools (
    id bigserial not null primary key,
    entity_id bigint not null references entities(id) on delete restrict,
    name varchar(255) not null,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table sports (
    id bigserial not null primary key,
    name varchar(255) not null,
    school_id bigint not null references schools(id) on delete restrict,
    conference_id bigint not null references conferences(id) on delete restrict,
    division_id bigint not null references divisions(id) on delete restrict,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table people (
    id bigserial not null primary key,
    name varchar(255) not null,
    entity_id bigint not null references entities(id) on delete restrict,
    parent_entity_id bigint not null references entities(id) on delete restrict,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);