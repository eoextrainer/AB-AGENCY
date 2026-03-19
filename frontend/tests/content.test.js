import { navigation, servicePillars } from "@/lib/content";

describe("content constants", () => {
  it("defines navigation links", () => {
    expect(navigation.map((item) => item.href)).toContain("/artists");
  });

  it("defines service pillars", () => {
    expect(servicePillars).toHaveLength(3);
  });
});