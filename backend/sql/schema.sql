CREATE TYPE user_role AS ENUM ('admin', 'editor', 'viewer', 'client');
CREATE TYPE inquiry_status AS ENUM ('new', 'qualified', 'proposal', 'booked', 'closed');

CREATE TABLE IF NOT EXISTS artists (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(120) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    headline VARCHAR(255) NOT NULL,
    discipline VARCHAR(100) NOT NULL,
    group_size VARCHAR(50) NOT NULL,
    mood VARCHAR(100) NOT NULL,
    venue_type VARCHAR(100) NOT NULL,
    technical_requirements JSONB NOT NULL DEFAULT '{}'::jsonb,
    bio TEXT NOT NULL,
    featured BOOLEAN NOT NULL DEFAULT FALSE,
    is_new BOOLEAN NOT NULL DEFAULT FALSE,
    location VARCHAR(150) NOT NULL DEFAULT 'London',
    travel_ready BOOLEAN NOT NULL DEFAULT TRUE,
    hero_video_url VARCHAR(500),
    teaser_video_url VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS inquiries (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL,
    contact_name VARCHAR(200) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    event_type VARCHAR(100) NOT NULL,
    event_date TIMESTAMP,
    location VARCHAR(200) NOT NULL,
    venue_type VARCHAR(100),
    ceiling_height_meters INTEGER,
    budget_min NUMERIC(10,2),
    budget_max NUMERIC(10,2),
    preferred_disciplines JSONB NOT NULL DEFAULT '[]'::jsonb,
    preferred_artist_slugs JSONB NOT NULL DEFAULT '[]'::jsonb,
    message TEXT NOT NULL,
    lead_score INTEGER NOT NULL DEFAULT 0,
    source VARCHAR(100) NOT NULL DEFAULT 'website',
    status inquiry_status NOT NULL DEFAULT 'new',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'viewer',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
