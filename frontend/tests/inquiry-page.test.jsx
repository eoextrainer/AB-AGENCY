import { render, screen } from "@testing-library/react";

import InquiryPage from "@/app/inquiry/page";

vi.mock("@/lib/api", () => ({
  getArtists: vi.fn().mockResolvedValue([{ slug: "luna", name: "Luna" }])
}));

describe("inquiry page", () => {
  it("passes query-selected artist into the form", async () => {
    const element = await InquiryPage({ searchParams: Promise.resolve({ artist: "luna" }) });
    render(element);

    expect(screen.getByText("Submit inquiry")).toBeInTheDocument();
  });
});