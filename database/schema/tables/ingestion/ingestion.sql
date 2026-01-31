create table ncaa_directory (
    id bigserial not null primary key,
    external_id bigint not null,
    name varchar(255) not null,
    member_type int,
    json_data jsonb,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table directory_sports (
    id bigserial not null primary key,
    name varchar(255) not null,
    code varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table directory_sport_aliases (
    id bigserial not null primary key,
    ncaa_directory_sport_id bigint not null references directory_sports(id) on delete restrict,
    name varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table ncaa_sport_directory (
    id bigserial not null primary key,
    ncaa_directory_id bigint not null references ncaa_directory(id) on delete restrict,
    ncaa_directory_sport_id bigint not null references directory_sports(id) on delete restrict,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table endpoint_types (
    id bigserial not null primary key,
    name varchar(255),
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table endpoints (
    id bigserial not null primary key,
    ncaa_sport_directory_id bigint not null references ncaa_sport_directory(id) on delete restrict,
    parent_endpoint_id bigint references endpoints(id) on delete restrict,
    endpoint_type_id bigint not null references endpoint_types(id) on delete restrict,
    endpoint text,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);

create table routes (
	id bigserial not null primary key,
	parent_id bigint references endpoints(id) on delete restrict,
	child_id bigint references endpoints(id) on delete restrict,
	created_at timestamptz not null,
    updated_at timestamptz not null,
    deleted_at timestamptz
);
    