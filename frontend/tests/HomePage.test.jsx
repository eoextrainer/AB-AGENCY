import { render, screen } from "@testing-library/react";

import { HomePage } from "@/components/HomePage";

describe("HomePage", () => {
  it("renders homepage and spotlight content", () => {
    render(
      <HomePage
        homepage={{
          hero_title: "Performance vertigineuse.",
          hero_subtitle: "Performance pour evenement premium.",
          featured_artists: [{ slug: "luna", discipline: "Danse aerienne", name: "Luna", headline: "Duo suspendu.", group_size: "Duo", mood: "Ethere", teaser_video_url: "https://example.com/luna.mp4", media_assets: [] }],
          trust_markers: ["Safe", "Touring-ready"],
          featured_services: ["Representation"]
        }}
        spotlight={{ title: "Focus", body: "Body", videoUrl: "https://example.com/spotlight.mp4", videoPoster: "https://example.com/poster.jpg", highlights: ["One"] }}
      />
    );

    expect(screen.getByText("Performance vertigineuse.")).toBeInTheDocument();
    expect(screen.getByText("Luna")).toBeInTheDocument();
    expect(screen.getByText("Rythme production")).toBeInTheDocument();
    expect(screen.getByText("Extrait video")).toBeInTheDocument();
    expect(screen.getByText("Capsule curatoriale")).toBeInTheDocument();
    expect(screen.getByText("Perspective studio")).toBeInTheDocument();
    expect(screen.getAllByTitle(/video/i).length).toBeGreaterThan(0);
  });
});