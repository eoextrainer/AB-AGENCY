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
    years_experience INTEGER NOT NULL DEFAULT 0,
    featured BOOLEAN NOT NULL DEFAULT FALSE,
    is_new BOOLEAN NOT NULL DEFAULT FALSE,
    location VARCHAR(150) NOT NULL DEFAULT 'London',
    travel_ready BOOLEAN NOT NULL DEFAULT TRUE,
    portrait_image_url VARCHAR(500),
    spoken_languages JSONB NOT NULL DEFAULT '[]'::jsonb,
    performance_resume JSONB NOT NULL DEFAULT '[]'::jsonb,
    hero_video_url VARCHAR(500),
    teaser_video_url VARCHAR(500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS media_assets (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES artists(id) ON DELETE CASCADE,
    asset_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    alt_text VARCHAR(255),
    asset_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS testimonials (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES artists(id) ON DELETE SET NULL,
    client_name VARCHAR(200) NOT NULL,
    client_type VARCHAR(100) NOT NULL,
    quote TEXT NOT NULL,
    event_name VARCHAR(200),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS inquiries (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL,
    contact_name VARCHAR(200) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    event_type VARCHAR(100) NOT NULL,
    event_date TIMESTAMPTZ,
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
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    artist_id INTEGER UNIQUE REFERENCES artists(id) ON DELETE SET NULL,
    role user_role NOT NULL DEFAULT 'viewer',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    inquiry_id INTEGER REFERENCES inquiries(id) ON DELETE SET NULL,
    artist_id INTEGER REFERENCES artists(id) ON DELETE SET NULL,
    booking_date TIMESTAMPTZ,
    status VARCHAR(100) NOT NULL DEFAULT 'tentative',
    fee_amount NUMERIC(10,2),
    deposit_paid BOOLEAN NOT NULL DEFAULT FALSE,
    contract_url VARCHAR(500),
    production_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS availability_slots (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'available',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS case_studies (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(120) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    event_context VARCHAR(150) NOT NULL,
    challenge TEXT NOT NULL,
    solution TEXT NOT NULL,
    client_name VARCHAR(200),
    hero_image_url VARCHAR(500),
    video_url VARCHAR(500),
    featured_artist_slugs JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS service_pages (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(120) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    summary TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_events (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
