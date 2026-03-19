export function AdminPageView({ dashboard }) {
  if (!dashboard) {
    return (
      <section className="panel">
        <p className="eyebrow">Admin preview</p>
        <h2>Admin API token missing.</h2>
        <p className="muted">Set `NEXT_PUBLIC_ADMIN_TOKEN` after authenticating against the backend to surface live dashboard metrics in the frontend.</p>
      </section>
    );
  }

  return (
    <div className="page-stack">
      <section className="panel stats-grid">
        <article>
          <span>Total artists</span>
          <strong>{dashboard.stats.total_artists}</strong>
        </article>
        <article>
          <span>Featured artists</span>
          <strong>{dashboard.stats.featured_artists}</strong>
        </article>
        <article>
          <span>Open inquiries</span>
          <strong>{dashboard.stats.open_inquiries}</strong>
        </article>
        <article>
          <span>Booked inquiries</span>
          <strong>{dashboard.stats.booked_inquiries}</strong>
        </article>
      </section>
      <section className="content-grid">
        <div className="panel">
          <p className="eyebrow">Recent inquiries</p>
          <ul>
            {dashboard.inquiries.slice(0, 5).map((inquiry) => (
              <li key={inquiry.id}>{inquiry.company_name} · {inquiry.event_type} · score {inquiry.lead_score}</li>
            ))}
          </ul>
        </div>
        <div className="panel">
          <p className="eyebrow">Availability slots</p>
          <ul>
            {dashboard.availability.slice(0, 5).map((slot) => (
              <li key={slot.id}>Artist #{slot.artist_id} · {slot.status}</li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}