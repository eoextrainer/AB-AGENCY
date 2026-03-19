import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { InquiryPageView } from "@/components/InquiryPageView";

vi.mock("@/lib/api", () => ({
  submitInquiry: vi.fn().mockResolvedValue({ lead_score: 88 })
}));

describe("InquiryPageView", () => {
  it("submits the inquiry form", async () => {
    render(<InquiryPageView artists={[{ slug: "luna", name: "Luna" }]} initialArtist="luna" />);

    fireEvent.change(screen.getByLabelText("Company"), { target: { value: "Acme" } });
    fireEvent.change(screen.getByLabelText("Contact name"), { target: { value: "Jordan" } });
    fireEvent.change(screen.getByLabelText("Email"), { target: { value: "jordan@example.com" } });
    fireEvent.change(screen.getByLabelText("Location"), { target: { value: "London" } });
    fireEvent.change(screen.getByLabelText("Message"), { target: { value: "Need an act" } });
    fireEvent.click(screen.getByText("Submit inquiry"));

    await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent("lead score 88"));
  });
});