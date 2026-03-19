import { render, screen } from "@testing-library/react";

import Page from "@/app/page";

vi.mock("@/lib/api", () => ({
  getHomepageData: vi.fn().mockResolvedValue({
    hero_title: "Hero",
    hero_subtitle: "Subtitle",
    featured_artists: [],
    trust_markers: [],
    featured_services: []
  })
}));

vi.mock("@/lib/cms", () => ({
  getCmsSpotlight: vi.fn().mockResolvedValue({ title: "Spotlight", body: "Copy", highlights: [] })
}));

describe("home page", () => {
  it("renders fetched homepage data", async () => {
    const element = await Page();
    render(element);

    expect(screen.getByText("Hero")).toBeInTheDocument();
  });
});