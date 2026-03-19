import { render, screen } from "@testing-library/react";

import { HomePage } from "@/components/HomePage";

describe("HomePage", () => {
  it("renders homepage and spotlight content", () => {
    render(
      <HomePage
        homepage={{
          hero_title: "Gravity-defying performance.",
          hero_subtitle: "Luxury event performance.",
          featured_artists: [{ slug: "luna", discipline: "Aerial", name: "Luna", headline: "Suspended duet.", group_size: "Duo", mood: "Ethereal" }],
          trust_markers: ["Safe", "Touring-ready"],
          featured_services: ["Representation"]
        }}
        spotlight={{ title: "Spotlight", body: "Body", highlights: ["One"] }}
      />
    );

    expect(screen.getByText("Gravity-defying performance.")).toBeInTheDocument();
    expect(screen.getByText("Luna")).toBeInTheDocument();
  });
});