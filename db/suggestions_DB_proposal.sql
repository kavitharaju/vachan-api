-- Planning DB structure for AgMT suggestions Module

-- CREATE TABLE public.content_types (
--     content_type_id SERIAL PRIMARY KEY ,
--     content_type text UNIQUE NOT NULL
-- );

-- INSERT INTO content_types(content_type) VALUES('bible');
-- INSERT INTO content_types(content_type) VALUES('commentary');
-- INSERT INTO content_types(content_type) VALUES('dictionary');
-- INSERT INTO content_types(content_type) VALUES('infographics');
-- INSERT INTO content_types(content_type) VALUES('bible_video');

CREATE TABLE public.languages (
    language_id SERIAL PRIMARY KEY,
    language_code char(3) UNIQUE NOT NULL,
    language_name text NOT NULL,
    script_direction text
);

alter table languages alter column script_direction set default 'left-to-right';

-- \COPY languages (language_code,language_name) FROM 'languages.csv' DELIMITER ',' CSV HEADER;

-- CREATE TABLE public.versions (
--     version_id SERIAL PRIMARY KEY,
--     version_code text UNIQUE NOT NULL,
--     version_description text NOT NULL,
--     revision text NOT NULL,
--     metadata jsonb
-- );

-- CREATE TABLE public.sources (
--     source_id SERIAL PRIMARY KEY,
--     table_name text  UNIQUE NOT NULL,
--     year int NOT NULL,
--     license text DEFAULT 'CC BY SA',
--     content_id int NOT NULL
--       REFERENCES content_types(content_type_id) ON DELETE CASCADE,
--     language_id int NOT NULL
--       REFERENCES languages(language_id) ON DELETE CASCADE,
--     created_at_date timestamp with time zone DEFAULT ('now'::text)::timestamp(2) with time zone,
--     status boolean DEFAULT true NOT NULL,
--     version_id int
--       REFERENCES versions(version_id) ON DELETE CASCADE,
--     metadata jsonb 
-- );

CREATE TABLE public.users(
    user_id SERIAL PRIMARY KEY,
    user_name text NOT NULL,
    user_email text NOT NULL unique,
    active boolean default true
);

CREATE TYPE sentence AS(
    sentence_id int,
    sentence_text text
);

CREATE TABLE public.translation_projects(
    project_id SERIAL PRIMARY KEY,
    project_name TEXT unique NOT NULL,
    source_lang_id int NOT NULL
        REFERENCES languages(language_id) ON DELETE CASCADE,
    target_lang_id int NOT NULL 
        REFERENCES languages(language_id) ON DELETE CASCADE,
    source_document sentence[],
    source_document_format text DEFAULT 'USFM',
    draft text,
    draft_corrected boolean DEFAULT false,
    active boolean default true
);

CREATE TABLE public.translation_project_users(
    project_id int REFERENCES translation_projects(project_id),
    user_id int REFERENCES users(user_id)
);

CREATE TYPE occurance AS(
    sentence_id int,
    char_offset int
);

CREATE TYPE suggestion AS(
    suggestion text,
    score numeric
);

CREATE TABLE public.translation_memory(
    translation_id int PRIMARY KEY,
    project_id int REFERENCES translation_projects(project_id),
    token_occurance occurance NOT NULL,
    token text NOT NULL,
    translation_suggestions suggestion[],
    verified_translation_offset occurance NOT NULL,
    verified_translation text
);

