import { VideoTile } from "@/components/VideoTile";
import { getArtistVideoId } from "@/lib/video";

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
          <VideoTile label="Rythme production" videoId="miEl69BgVIU" className="trust-video-tile" />
        </div>
      </section>

      <section className="panel spotlight-panel">
        <p className="eyebrow">Focus contenu</p>
        <h3>{spotlight.title}</h3>
        <p>{spotlight.body}</p>
        <VideoTile label="Capsule curatoriale" videoId="8D9IBNEASYw" className="spotlight-video" />
        <ul>
          {spotlight.highlights.map((highlight) => (
            <li key={highlight}>{highlight}</li>
          ))}
        </ul>
      </section>

      <section className="panel featured-artists-panel">
        <p className="eyebrow">Artistes en avant</p>
        <div className="artist-list featured-artist-grid">
          {homepage.featured_artists.map((artist, index) => (
            <article key={artist.slug} className="artist-card compact featured-artist-tile">
              <div className="featured-artist-card">
                <div>
                  <span className="tag">{artist.discipline}</span>
                  <h3>{artist.name}</h3>
                  <p>{artist.headline}</p>
                </div>
                <VideoTile
                  label="Extrait video"
                  videoId={getArtistVideoId(artist, index)}
                />
              </div>
              <div className="card-meta">
                <span>{artist.group_size}</span>
                <span>{artist.mood}</span>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="panel services-panel">
        <div className="services-layout">
          <div>
            <p className="eyebrow">Axes de service</p>
            <div className="services-pill-grid">
              {homepage.featured_services.map((service) => (
                <span key={service} className="pill pill-small">
                  {service}
                </span>
              ))}
            </div>
          </div>
          <VideoTile label="Perspective studio" videoId="TazDN6D9pl4" className="service-video-tile" />
        </div>
      </section>
    </div>
  );
}