-- Planning DB structure for AgMT suggestions Module

CREATE TABLE public.languages (
    language_id SERIAL PRIMARY KEY,
    language_code char(3) UNIQUE NOT NULL,
    language_name text NOT NULL,
    script_direction text
);

alter table languages alter column script_direction set default 'left-to-right';

CREATE TABLE public.translation_projects(
    project_id SERIAL PRIMARY KEY,
    project_name TEXT unique NOT NULL,
    source_lang_id int NOT NULL
        REFERENCES languages(language_id),
    target_lang_id int NOT NULL 
        REFERENCES languages(language_id),
    source_document_format text DEFAULT 'USFM',
    active boolean default true,
    created_user int NULL,
    created_at timestamp with time zone DEFAULT NOW()
);

CREATE TABLE public.translation_project_users(
    project_id int REFERENCES translation_projects(project_id),
    user_id int
);

CREATE TABLE public.translation_drafts(
    draft_id SERIAL PRIMARY KEY,
    project_id int NOT NULL 
        REFERENCES translation_projects(project_id) ON DELETE CASCADE,
    sentence_id int NOT NULL,
    sentence text,
    draft text,
    draft_meta jsonb[],
    last_updated_user int NULL,
    last_updated_at  timestamp with time zone DEFAULT NOW(),
    UNIQUE(project_id, sentence_id)
);

CREATE TABLE public.translation_memory(
    token_id int PRIMARY KEY,
    source_lang_id int NOT NULL
        REFERENCES languages(language_id),
    target_lang_id int NOT NULL 
        REFERENCES languages(language_id),
    token text NOT NULL,
    translations text[],
    UNIQUE(source_lang_id, target_lang_id, token)
);
