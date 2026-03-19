import { render, screen } from "@testing-library/react";

import AdminPage from "@/app/admin/page";

vi.mock("@/lib/api", () => ({
  getAdminAccessToken: vi.fn().mockResolvedValue("token-123"),
  getDashboardSnapshot: vi.fn().mockResolvedValue(null)
}));

describe("admin page", () => {
  it("renders the admin fallback when no token is configured", async () => {
    const element = await AdminPage();
    render(element);

    expect(screen.getByText("Les donnees administratives sont indisponibles.")).toBeInTheDocument();
  });
});