import { fireEvent, render, screen } from "@testing-library/react";

import { MediaLightboxGallery } from "@/components/MediaLightboxGallery";

describe("MediaLightboxGallery", () => {
  it("renders a YouTube iframe for video assets inside the lightbox", () => {
    render(
      <MediaLightboxGallery
        assets={[
          {
            id: 1,
            asset_type: "video",
            title: "Showreel",
            url: "https://www.youtube.com/watch?v=zreMvcHghP8",
            thumbnail_url: "/thumb.jpg",
            alt_text: "Showreel"
          }
        ]}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /showreel/i }));

    expect(screen.getByTitle("Showreel")).toBeInTheDocument();
  });
});