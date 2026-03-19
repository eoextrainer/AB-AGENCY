import { fireEvent, render, screen } from "@testing-library/react";

import { ArtistsPageView } from "@/components/ArtistsPageView";

const artists = [
  { slug: "luna", name: "Luna", headline: "Suspended duet", discipline: "Aerial", group_size: "Duo", mood: "Ethereal", bio: "Aerial act", travel_ready: true },
  { slug: "volt", name: "Volt", headline: "Cyr wheel", discipline: "Ground", group_size: "Solo", mood: "Dramatic", bio: "Ground act", travel_ready: true }
];

describe("ArtistsPageView", () => {
  it("filters artists by search", () => {
    render(<ArtistsPageView artists={artists} />);

    fireEvent.change(screen.getByLabelText("Search artists"), { target: { value: "Volt" } });

    expect(screen.getByText("Volt")).toBeInTheDocument();
    expect(screen.queryByText("Luna")).not.toBeInTheDocument();
  });

  it("adds artists to the comparison tray", () => {
    render(<ArtistsPageView artists={artists} />);

    fireEvent.click(screen.getAllByText("Compare")[0]);

    expect(screen.getAllByText("Luna").length).toBeGreaterThan(0);
  });
});