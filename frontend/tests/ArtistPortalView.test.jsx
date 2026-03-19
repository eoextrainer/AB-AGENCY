import { render, screen, waitFor } from "@testing-library/react";

import { ArtistPortalView } from "@/components/ArtistPortalView";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() })
}));

vi.mock("@/lib/api", () => ({
  SESSION_TOKEN_KEY: "abAgencySessionToken",
  getArtistPortal: vi.fn().mockResolvedValue({
    user: { username: "ambre", full_name: "Ambre Lenoir", email: "ambre@ab-agency.com" },
    artist: {
      name: "Ambre Lenoir",
      headline: "Signature scénique.",
      discipline: "Danse acrobatique",
      years_experience: 11,
      location: "Paris",
      spoken_languages: ["Francais"],
      portrait_image_url: "/portrait.jpg",
      media_assets: [{ id: 1, asset_type: "image", title: "Portrait", url: "/portrait.jpg", thumbnail_url: "/portrait.jpg" }],
      performance_resume: [{ period: "2025", production: "Nocturne", venue: "Paris", role: "Solo" }]
    }
  })
}));

describe("ArtistPortalView", () => {
  it("renders the linked artist profile", async () => {
    window.sessionStorage.setItem("abAgencySessionToken", "token-123");

    render(<ArtistPortalView />);

    await waitFor(() => expect(screen.getAllByText("Ambre Lenoir").length).toBeGreaterThan(0));
    expect(screen.getByText("Resume artistique")).toBeInTheDocument();
    expect(screen.getByText("Galerie curatoriale")).toBeInTheDocument();
    expect(screen.getByText("Reel prive")).toBeInTheDocument();
  });
});