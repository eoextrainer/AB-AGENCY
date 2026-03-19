import { render, screen } from "@testing-library/react";

import { AdminPageView } from "@/components/AdminPageView";

describe("AdminPageView", () => {
  it("renders fallback state without dashboard data", () => {
    render(<AdminPageView dashboard={null} />);

    expect(screen.getByText("Admin API token missing.")).toBeInTheDocument();
  });

  it("renders dashboard metrics", () => {
    render(
      <AdminPageView
        dashboard={{
          stats: { total_artists: 2, featured_artists: 2, open_inquiries: 3, booked_inquiries: 1 },
          inquiries: [{ id: 1, company_name: "Acme", event_type: "Festival", lead_score: 80 }],
          bookings: [],
          availability: [{ id: 1, artist_id: 1, status: "available" }]
        }}
      />
    );

    expect(screen.getByText("Total artists")).toBeInTheDocument();
    expect(screen.getByText("Featured artists")).toBeInTheDocument();
    expect(screen.getByText(/Acme/)).toBeInTheDocument();
  });
});