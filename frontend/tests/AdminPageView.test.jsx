import { render, screen } from "@testing-library/react";

import { AdminPageView } from "@/components/AdminPageView";

describe("AdminPageView", () => {
  it("renders fallback state without dashboard data", () => {
    render(<AdminPageView dashboard={null} />);

    expect(screen.getByText("Les donnees administratives sont indisponibles.")).toBeInTheDocument();
  });

  it("renders dashboard metrics", () => {
    render(
      <AdminPageView
        dashboard={{
          stats: { total_artists: 2, featured_artists: 2, open_inquiries: 3, booked_inquiries: 1 },
          inquiries: [{ id: 1, company_name: "Acme", contact_name: "Jordan Vale", email: "jordan@example.com", phone: "12345", created_at: "2026-03-19T12:00:00Z", event_type: "Festival", location: "London", venue_type: "Indoor", budget_min: 5000, budget_max: 12000, preferred_artist_slugs: ["luna-silk-duo"], lead_score: 80, status: "qualified", ceiling_height_meters: 9, message: "Need a standout opener" }],
          bookings: [{ id: 1 }],
          availability: [{ id: 1, artist_id: 1, status: "available" }]
        }}
      />
    );

    expect(screen.getByText("Artistes au catalogue")).toBeInTheDocument();
    expect(screen.getByText("Contacts recus")).toBeInTheDocument();
    expect(screen.getByText("Evenements demandes et budgets cibles")).toBeInTheDocument();
    expect(screen.getAllByText(/Acme/).length).toBeGreaterThan(0);
    expect(screen.getByText(/Jordan Vale/)).toBeInTheDocument();
  });
});