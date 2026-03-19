import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { InquiryPageView } from "@/components/InquiryPageView";

vi.mock("@/lib/api", () => ({
  submitInquiry: vi.fn().mockResolvedValue({ lead_score: 88 })
}));

describe("InquiryPageView", () => {
  it("submits the inquiry form", async () => {
    render(<InquiryPageView artists={[{ slug: "luna", name: "Luna" }]} initialArtist="luna" />);

    fireEvent.change(screen.getByLabelText("Societe"), { target: { value: "Acme" } });
    fireEvent.change(screen.getByLabelText("Nom du contact"), { target: { value: "Jordan" } });
    fireEvent.change(screen.getByLabelText("Email"), { target: { value: "jordan@example.com" } });
    fireEvent.change(screen.getByLabelText("Date de l'evenement"), { target: { value: "2026-07-12T18:00" } });
    fireEvent.change(screen.getByLabelText("Lieu"), { target: { value: "London" } });
    fireEvent.change(screen.getByLabelText("Disciplines souhaitees"), { target: { value: "Aerial, Duo" } });
    fireEvent.change(screen.getByLabelText("Message"), { target: { value: "Need an act" } });
    fireEvent.click(screen.getByText("Envoyer la demande"));

    await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent("88"));
  });
});