import { render, screen } from "@testing-library/react";

import AdminPage from "@/app/admin/page";

vi.mock("@/lib/api", () => ({
  getDashboardSnapshot: vi.fn().mockResolvedValue(null)
}));

describe("admin page", () => {
  it("renders the admin fallback when no token is configured", async () => {
    const element = await AdminPage();
    render(element);

    expect(screen.getByText("Admin API token missing.")).toBeInTheDocument();
  });
});