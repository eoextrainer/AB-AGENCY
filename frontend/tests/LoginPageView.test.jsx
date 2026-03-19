import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { LoginPageView } from "@/components/LoginPageView";

const push = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push })
}));

vi.mock("@/lib/api", () => ({
  SESSION_TOKEN_KEY: "abAgencySessionToken",
  getAdminAccessToken: vi.fn().mockResolvedValue("token-123"),
  getCurrentUser: vi.fn().mockResolvedValue({ username: "admin", role: "admin", is_active: true })
}));

describe("LoginPageView", () => {
  it("redirects an admin after successful login", async () => {
    render(<LoginPageView />);

    fireEvent.change(screen.getByLabelText("Nom d'utilisateur"), { target: { value: "admin" } });
    fireEvent.change(screen.getByLabelText("Mot de passe"), { target: { value: "admin123" } });
    fireEvent.click(screen.getByText("Se connecter"));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/admin"));
  });
});