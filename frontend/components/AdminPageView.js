export function AdminPageView({ dashboard }) {
  if (!dashboard) {
    return (
      <section className="panel">
        <p className="eyebrow">Apercu administrateur</p>
        <h2>Les donnees administratives sont indisponibles.</h2>
        <p className="muted">Verifiez le backend ou les identifiants admin utilises par le rendu serveur du frontend.</p>
      </section>
    );
  }

  return (
    <div className="page-stack">
      <section className="panel stats-grid">
        <article>
          <span>Artistes au catalogue</span>
          <strong>{dashboard.stats.total_artists}</strong>
        </article>
        <article>
          <span>Artistes en avant</span>
          <strong>{dashboard.stats.featured_artists}</strong>
        </article>
        <article>
          <span>Demandes ouvertes</span>
          <strong>{dashboard.stats.open_inquiries}</strong>
        </article>
        <article>
          <span>Demandes confirmees</span>
          <strong>{dashboard.stats.booked_inquiries}</strong>
        </article>
      </section>
      <section className="content-grid">
        <div className="panel">
          <p className="eyebrow">Contacts recus</p>
          <div className="admin-table-wrap">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Contact</th>
                  <th>Societe</th>
                  <th>Email</th>
                  <th>Telephone</th>
                  <th>Recu le</th>
                </tr>
              </thead>
              <tbody>
                {dashboard.inquiries.map((inquiry) => (
                  <tr key={inquiry.id}>
                    <td>{inquiry.contact_name}</td>
                    <td>{inquiry.company_name}</td>
                    <td>{inquiry.email}</td>
                    <td>{inquiry.phone || "Non renseigne"}</td>
                    <td>{new Date(inquiry.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="panel">
          <p className="eyebrow">Evenements demandes et budgets cibles</p>
          <div className="admin-table-wrap">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Evenement</th>
                  <th>Lieu</th>
                  <th>Configuration</th>
                  <th>Budget cible</th>
                  <th>Actes preferes</th>
                </tr>
              </thead>
              <tbody>
                {dashboard.inquiries.map((inquiry) => (
                  <tr key={`event-${inquiry.id}`}>
                    <td>{inquiry.event_type}</td>
                    <td>{inquiry.location}</td>
                    <td>{inquiry.venue_type || "Inconnu"}</td>
                    <td>{formatBudgetTarget(inquiry.budget_min, inquiry.budget_max)}</td>
                    <td>{inquiry.preferred_artist_slugs.length > 0 ? inquiry.preferred_artist_slugs.join(", ") : "Brief ouvert"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="panel">
        <p className="eyebrow">Flux detaille des demandes</p>
        <div className="admin-feed">
          {dashboard.inquiries.map((inquiry) => (
            <article key={`detail-${inquiry.id}`} className="admin-feed-card">
              <h3>{inquiry.company_name}</h3>
              <p>{inquiry.message}</p>
              <div className="card-meta">
                <span>Score {inquiry.lead_score}</span>
                <span>{inquiry.status}</span>
                <span>Plafond {inquiry.ceiling_height_meters || "n/d"}m</span>
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
    return `${Number(minimum).toLocaleString()} a ${Number(maximum).toLocaleString()}`;
  }

  if (maximum) {
    return `Jusqu'a ${Number(maximum).toLocaleString()}`;
  }

  if (minimum) {
    return `A partir de ${Number(minimum).toLocaleString()}`;
  }

  return "Non renseigne";
}