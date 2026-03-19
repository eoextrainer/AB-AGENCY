import { render, screen } from "@testing-library/react";

import { AdminPageView } from "@/components/AdminPageView";

describe("admin page tables", () => {
  it("renders budget targets and contact rows", () => {
    render(
      <AdminPageView
        dashboard={{
          stats: { total_artists: 1, featured_artists: 1, open_inquiries: 1, booked_inquiries: 0 },
          inquiries: [
            {
              id: 7,
              company_name: "Northstar Events",
              contact_name: "Evelyn Hart",
              email: "evelyn@example.com",
              phone: null,
              created_at: "2026-03-19T12:00:00Z",
              event_type: "Corporate Gala",
              location: "Manchester",
              venue_type: "Ballroom",
              budget_min: 8000,
              budget_max: 16000,
              preferred_artist_slugs: [],
              lead_score: 85,
              status: "new",
              ceiling_height_meters: null,
              message: "Need a centerpiece act"
            }
          ],
          bookings: [],
          availability: []
        }}
      />
    );

    expect(screen.getByText("Evelyn Hart")).toBeInTheDocument();
    expect(screen.getByText("8,000 to 16,000")).toBeInTheDocument();
  });
});