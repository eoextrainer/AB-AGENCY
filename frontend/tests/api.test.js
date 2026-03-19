import { buildApiUrl, getArtists, getDashboardSnapshot, getHomepageData, submitInquiry } from "@/lib/api";
import { getAdminAccessToken } from "@/lib/api";

describe("api helpers", () => {
  it("builds API urls", () => {
    expect(buildApiUrl("/artists")).toContain("/api/artists");
  });

  it("returns homepage fallback when fetch fails", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("boom"));

    const homepage = await getHomepageData();

    expect(homepage.hero_title).toContain("Performance");
  });

  it("returns artists from the backend", async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => [{ slug: "luna" }] });

    await expect(getArtists()).resolves.toEqual([{ slug: "luna" }]);
  });

  it("submits inquiries to the backend", async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ id: 1, lead_score: 90 }) });

    const response = await submitInquiry({ company_name: "Acme" });

    expect(response.lead_score).toBe(90);
  });

  it("returns an admin access token when login succeeds", async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ access_token: "token-123" }) });

    await expect(getAdminAccessToken({ email: "admin@ab-agency.com", password: "admin12345" })).resolves.toBe("token-123");
  });

  it("returns null dashboard snapshot when token is missing", async () => {
    await expect(getDashboardSnapshot("")).resolves.toBeNull();
  });

  it("returns dashboard overview from the backend", async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ stats: { total_artists: 2 }, inquiries: [], bookings: [], availability: [] }) });

    const dashboard = await getDashboardSnapshot("token-123");

    expect(dashboard.stats.total_artists).toBe(2);
  });
});