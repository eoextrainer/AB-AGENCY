export function HomePage({ homepage, spotlight }) {
  return (
    <div className="page-stack">
      <section className="hero-panel">
        <div className="hero-copy">
          <p className="eyebrow">Aerien. Precis. Reservable.</p>
          <h2>{homepage.hero_title}</h2>
          <p>{homepage.hero_subtitle}</p>
          <div className="cta-row">
            <a className="button button-primary" href="/inquiry">
              Demarrer une demande
            </a>
            <a className="button button-secondary" href="/artists">
              Decouvrir les artistes
            </a>
          </div>
        </div>
        <div className="hero-card">
          <p className="card-title">Reperes de confiance</p>
          <ul>
            {homepage.trust_markers.map((marker) => (
              <li key={marker}>{marker}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="content-grid">
        <div className="panel">
          <p className="eyebrow">Artistes en avant</p>
          <div className="artist-list">
            {homepage.featured_artists.map((artist) => (
              <article key={artist.slug} className="artist-card compact">
                <div className="featured-artist-card">
                  <div>
                    <span className="tag">{artist.discipline}</span>
                    <h3>{artist.name}</h3>
                    <p>{artist.headline}</p>
                  </div>
                  <div className="video-tile">
                    <video autoPlay muted loop playsInline poster={artist.portrait_image_url || artist.media_assets?.[0]?.thumbnail_url || undefined}>
                      <source src={artist.teaser_video_url || artist.hero_video_url} />
                    </video>
                    <span className="video-tile-label">Extrait video</span>
                  </div>
                </div>
                <div className="card-meta">
                  <span>{artist.group_size}</span>
                  <span>{artist.mood}</span>
                </div>
              </article>
            ))}
          </div>
        </div>

        <div className="panel spotlight-panel">
          <p className="eyebrow">Focus contenu</p>
          <h3>{spotlight.title}</h3>
          <p>{spotlight.body}</p>
          <div className="video-tile spotlight-video">
            <video autoPlay muted loop playsInline poster={spotlight.videoPoster}>
              <source src={spotlight.videoUrl} />
            </video>
            <span className="video-tile-label">Capsule curatoriale</span>
          </div>
          <ul>
            {spotlight.highlights.map((highlight) => (
              <li key={highlight}>{highlight}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="panel services-panel">
        <p className="eyebrow">Axes de service</p>
        <div className="pill-grid">
          {homepage.featured_services.map((service) => (
            <span key={service} className="pill">
              {service}
            </span>
          ))}
        </div>
      </section>
    </div>
  );
}