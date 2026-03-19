export function AdminPageView({ dashboard }) {
  if (!dashboard) {
    return (
      <section className="panel">
        <p className="eyebrow">Admin preview</p>
        <h2>Administrative data is unavailable.</h2>
        <p className="muted">Check the backend service or the admin API credentials configured for the frontend server render.</p>
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
          <p className="eyebrow">Submitted contacts</p>
          <div className="admin-table-wrap">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Contact</th>
                  <th>Company</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Submitted</th>
                </tr>
              </thead>
              <tbody>
                {dashboard.inquiries.map((inquiry) => (
                  <tr key={inquiry.id}>
                    <td>{inquiry.contact_name}</td>
                    <td>{inquiry.company_name}</td>
                    <td>{inquiry.email}</td>
                    <td>{inquiry.phone || "Not provided"}</td>
                    <td>{new Date(inquiry.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="panel">
          <p className="eyebrow">Requested events and budget targets</p>
          <div className="admin-table-wrap">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Event</th>
                  <th>Location</th>
                  <th>Venue</th>
                  <th>Budget target</th>
                  <th>Preferred acts</th>
                </tr>
              </thead>
              <tbody>
                {dashboard.inquiries.map((inquiry) => (
                  <tr key={`event-${inquiry.id}`}>
                    <td>{inquiry.event_type}</td>
                    <td>{inquiry.location}</td>
                    <td>{inquiry.venue_type || "Unknown"}</td>
                    <td>{formatBudgetTarget(inquiry.budget_min, inquiry.budget_max)}</td>
                    <td>{inquiry.preferred_artist_slugs.length > 0 ? inquiry.preferred_artist_slugs.join(", ") : "Open brief"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="panel">
        <p className="eyebrow">Inquiry detail feed</p>
        <div className="admin-feed">
          {dashboard.inquiries.map((inquiry) => (
            <article key={`detail-${inquiry.id}`} className="admin-feed-card">
              <h3>{inquiry.company_name}</h3>
              <p>{inquiry.message}</p>
              <div className="card-meta">
                <span>Lead score {inquiry.lead_score}</span>
                <span>{inquiry.status}</span>
                <span>Ceiling {inquiry.ceiling_height_meters || "n/a"}m</span>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

function formatBudgetTarget(minimum, maximum) {
  if (minimum && maximum) {
    return `${Number(minimum).toLocaleString()} to ${Number(maximum).toLocaleString()}`;
  }

  if (maximum) {
    return `Up to ${Number(maximum).toLocaleString()}`;
  }

  if (minimum) {
    return `From ${Number(minimum).toLocaleString()}`;
  }

  return "Not supplied";
}