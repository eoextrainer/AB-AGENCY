import { buildApiUrl, getArtists, getDashboardSnapshot, getHomepageData, submitInquiry } from "@/lib/api";

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

  it("returns null dashboard snapshot when token is missing", async () => {
    await expect(getDashboardSnapshot("")).resolves.toBeNull();
  });
});