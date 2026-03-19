"use client";

import { startTransition, useDeferredValue, useMemo, useState } from "react";

import { MediaLightboxGallery } from "@/components/MediaLightboxGallery";

function matchesArtist(artist, filters) {
  const search = filters.search.trim().toLowerCase();
  const matchesSearch = !search || [artist.name, artist.headline, artist.discipline, artist.mood].join(" ").toLowerCase().includes(search);
  const matchesDiscipline = !filters.discipline || artist.discipline === filters.discipline;
  const matchesMood = !filters.mood || artist.mood === filters.mood;
  return matchesSearch && matchesDiscipline && matchesMood;
}

export function ArtistsPageView({ artists }) {
  const [filters, setFilters] = useState({ search: "", discipline: "", mood: "" });
  const deferredFilters = useDeferredValue(filters);

  const filteredArtists = useMemo(() => artists.filter((artist) => matchesArtist(artist, deferredFilters)), [artists, deferredFilters]);
  const disciplines = [...new Set(artists.map((artist) => artist.discipline))];
  const moods = [...new Set(artists.map((artist) => artist.mood))];

  function updateFilter(key, value) {
    startTransition(() => {
      setFilters((current) => ({ ...current, [key]: value }));
    });
  }

  return (
    <div className="page-stack">
      <section className="panel filter-panel">
        <div>
          <p className="eyebrow">Catalogue artistes</p>
          <h2>Parcourez la selection par discipline, ambiance et langage visuel.</h2>
        </div>
        <div className="filter-grid">
          <input
            aria-label="Rechercher un artiste"
            placeholder="Rechercher un artiste"
            value={filters.search}
            onChange={(event) => updateFilter("search", event.target.value)}
          />
          <select
            aria-label="Filtrer par discipline"
            value={filters.discipline}
            onChange={(event) => updateFilter("discipline", event.target.value)}
          >
            <option value="">Toutes les disciplines</option>
            {disciplines.map((discipline) => (
              <option key={discipline} value={discipline}>
                {discipline}
              </option>
            ))}
          </select>
          <select
            aria-label="Filtrer par ambiance"
            value={filters.mood}
            onChange={(event) => updateFilter("mood", event.target.value)}
          >
            <option value="">Toutes les ambiances</option>
            {moods.map((mood) => (
              <option key={mood} value={mood}>
                {mood}
              </option>
            ))}
          </select>
        </div>
        <p className="muted">{filteredArtists.length} artiste(s) affiché(s) instantanément selon vos choix.</p>
      </section>

      <section className="artist-roster">
        {filteredArtists.map((artist) => (
          <article key={artist.slug} className="artist-row panel">
            <div className="artist-profile-pane">
              <div className="artist-identity-block">
                <img className="artist-portrait" src={artist.portrait_image_url || artist.media_assets?.[0]?.thumbnail_url || "/logo.png"} alt={artist.name} />
                <div>
                  <div className="card-meta">
                    <span>{artist.discipline}</span>
                    <span>{artist.group_size}</span>
                    <span>{artist.mood}</span>
                  </div>
                  <h3>{artist.name}</h3>
                  <p>{artist.headline}</p>
                </div>
              </div>
              <table className="info-table compact-table">
                <tbody>
                  <tr>
                    <th>Discipline</th>
                    <td>{artist.discipline}</td>
                  </tr>
                  <tr>
                    <th>Experience</th>
                    <td>{artist.years_experience || 0} ans</td>
                  </tr>
                  <tr>
                    <th>Base</th>
                    <td>{artist.location}</td>
                  </tr>
                  <tr>
                    <th>Langues</th>
                    <td>{artist.spoken_languages?.length ? artist.spoken_languages.join(", ") : "Selon projet"}</td>
                  </tr>
                </tbody>
              </table>
              <p className="muted">{artist.bio}</p>
              <div className="card-actions">
                <a className="button button-primary" href={`/inquiry?artist=${artist.slug}`}>
                  Demander cet artiste
                </a>
              </div>
            </div>
            <div className="artist-media-pane">
              <p className="eyebrow">Photos et videos</p>
              <MediaLightboxGallery assets={artist.media_assets || []} />
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}