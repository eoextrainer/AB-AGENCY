import { fireEvent, render, screen } from "@testing-library/react";

import { ArtistsPageView } from "@/components/ArtistsPageView";

const artists = [
  { slug: "luna", name: "Luna", headline: "Suspended duet", discipline: "Aerial", group_size: "Duo", mood: "Ethereal", bio: "Aerial act", travel_ready: true, years_experience: 8, location: "Paris", spoken_languages: ["Francais"], media_assets: [{ id: 1, asset_type: "image", title: "Portrait", url: "/portrait.jpg", thumbnail_url: "/portrait.jpg" }] },
  { slug: "volt", name: "Volt", headline: "Cyr wheel", discipline: "Ground", group_size: "Solo", mood: "Dramatic", bio: "Ground act", travel_ready: true, years_experience: 5, location: "Lyon", spoken_languages: ["Francais"], media_assets: [{ id: 2, asset_type: "video", title: "Showreel", url: "/showreel.mp4", thumbnail_url: "/thumb.jpg" }] }
];

describe("ArtistsPageView", () => {
  it("filters artists by search", () => {
    render(<ArtistsPageView artists={artists} />);

    fireEvent.change(screen.getByLabelText("Rechercher un artiste"), { target: { value: "Volt" } });

    expect(screen.getByText("Volt")).toBeInTheDocument();
    expect(screen.queryByText("Luna")).not.toBeInTheDocument();
  });

  it("renders the media gallery and experience row", () => {
    render(<ArtistsPageView artists={artists} />);

    expect(screen.getByText("8 ans")).toBeInTheDocument();
    expect(screen.getByText("Photo")).toBeInTheDocument();
    expect(screen.getAllByText("Bande demo").length).toBeGreaterThan(0);
  });
});