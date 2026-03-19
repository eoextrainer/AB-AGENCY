"use client";

import { useMemo, useState } from "react";

function matchesArtist(artist, filters) {
  const search = filters.search.trim().toLowerCase();
  const matchesSearch = !search || [artist.name, artist.headline, artist.discipline, artist.mood].join(" ").toLowerCase().includes(search);
  const matchesDiscipline = !filters.discipline || artist.discipline === filters.discipline;
  const matchesMood = !filters.mood || artist.mood === filters.mood;
  return matchesSearch && matchesDiscipline && matchesMood;
}

export function ArtistsPageView({ artists }) {
  const [filters, setFilters] = useState({ search: "", discipline: "", mood: "" });
  const [compare, setCompare] = useState([]);

  const filteredArtists = useMemo(() => artists.filter((artist) => matchesArtist(artist, filters)), [artists, filters]);
  const disciplines = [...new Set(artists.map((artist) => artist.discipline))];
  const moods = [...new Set(artists.map((artist) => artist.mood))];

  function toggleCompare(slug) {
    setCompare((current) => {
      if (current.includes(slug)) {
        return current.filter((item) => item !== slug);
      }
      if (current.length === 3) {
        return current;
      }
      return [...current, slug];
    });
  }

  const comparedArtists = artists.filter((artist) => compare.includes(artist.slug));

  return (
    <div className="page-stack">
      <section className="panel filter-panel">
        <div>
          <p className="eyebrow">Artist roster</p>
          <h2>Filter by discipline, mood, and buyer-fit.</h2>
        </div>
        <div className="filter-grid">
          <input
            aria-label="Search artists"
            placeholder="Search artists"
            value={filters.search}
            onChange={(event) => setFilters((current) => ({ ...current, search: event.target.value }))}
          />
          <select
            aria-label="Filter by discipline"
            value={filters.discipline}
            onChange={(event) => setFilters((current) => ({ ...current, discipline: event.target.value }))}
          >
            <option value="">All disciplines</option>
            {disciplines.map((discipline) => (
              <option key={discipline} value={discipline}>
                {discipline}
              </option>
            ))}
          </select>
          <select
            aria-label="Filter by mood"
            value={filters.mood}
            onChange={(event) => setFilters((current) => ({ ...current, mood: event.target.value }))}
          >
            <option value="">All moods</option>
            {moods.map((mood) => (
              <option key={mood} value={mood}>
                {mood}
              </option>
            ))}
          </select>
        </div>
      </section>

      <section className="artist-list">
        {filteredArtists.map((artist) => (
          <article key={artist.slug} className="artist-card">
            <div>
              <div className="card-meta">
                <span>{artist.discipline}</span>
                <span>{artist.group_size}</span>
                <span>{artist.mood}</span>
              </div>
              <h3>{artist.name}</h3>
              <p>{artist.headline}</p>
              <p className="muted">{artist.bio}</p>
            </div>
            <div className="card-actions">
              <button className="button button-secondary" type="button" onClick={() => toggleCompare(artist.slug)}>
                {compare.includes(artist.slug) ? "Remove from compare" : "Compare"}
              </button>
              <a className="button button-primary" href={`/inquiry?artist=${artist.slug}`}>
                Enquire
              </a>
            </div>
          </article>
        ))}
      </section>

      <section className="panel compare-panel">
        <p className="eyebrow">Comparison tray</p>
        {comparedArtists.length === 0 ? (
          <p>Select up to three acts to compare booking fit, technical demands, and mood.</p>
        ) : (
          <div className="compare-grid">
            {comparedArtists.map((artist) => (
              <article key={artist.slug} className="compare-card">
                <h3>{artist.name}</h3>
                <p>{artist.headline}</p>
                <ul>
                  <li>Discipline: {artist.discipline}</li>
                  <li>Group size: {artist.group_size}</li>
                  <li>Mood: {artist.mood}</li>
                  <li>Travel ready: {artist.travel_ready ? "Yes" : "No"}</li>
                </ul>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}