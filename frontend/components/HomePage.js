export function HomePage({ homepage, spotlight }) {
  return (
    <div className="page-stack">
      <section className="hero-panel">
        <div className="hero-copy">
          <p className="eyebrow">Weightless. Precise. Bookable.</p>
          <h2>{homepage.hero_title}</h2>
          <p>{homepage.hero_subtitle}</p>
          <div className="cta-row">
            <a className="button button-primary" href="/inquiry">
              Start Your Inquiry
            </a>
            <a className="button button-secondary" href="/artists">
              Explore Artists
            </a>
          </div>
        </div>
        <div className="hero-card">
          <p className="card-title">Trust markers</p>
          <ul>
            {homepage.trust_markers.map((marker) => (
              <li key={marker}>{marker}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="content-grid">
        <div className="panel">
          <p className="eyebrow">Featured artists</p>
          <div className="artist-list">
            {homepage.featured_artists.map((artist) => (
              <article key={artist.slug} className="artist-card compact">
                <div>
                  <span className="tag">{artist.discipline}</span>
                  <h3>{artist.name}</h3>
                  <p>{artist.headline}</p>
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
          <p className="eyebrow">CMS spotlight</p>
          <h3>{spotlight.title}</h3>
          <p>{spotlight.body}</p>
          <ul>
            {spotlight.highlights.map((highlight) => (
              <li key={highlight}>{highlight}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="panel services-panel">
        <p className="eyebrow">Service focus</p>
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