import { cmsConfig, getCmsSpotlight } from "@/lib/cms";

describe("cms helpers", () => {
  it("exposes the CMS provider metadata", () => {
    expect(cmsConfig.provider).toBe("sanity");
  });

  it("returns spotlight content", async () => {
    const spotlight = await getCmsSpotlight();

    expect(spotlight.highlights).toHaveLength(3);
  });
});