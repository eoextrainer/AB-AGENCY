import { render, screen } from "@testing-library/react";

import ArtistsPage from "@/app/artists/page";

vi.mock("@/lib/api", () => ({
  getArtists: vi.fn().mockResolvedValue([{ slug: "luna", name: "Luna", headline: "Suspended duet", discipline: "Aerial", group_size: "Duo", mood: "Ethereal", bio: "Aerial act", travel_ready: true }])
}));

describe("artists page", () => {
  it("renders roster data", async () => {
    const element = await ArtistsPage();
    render(element);

    expect(screen.getByText("Luna")).toBeInTheDocument();
  });
});