import { render, screen } from "@testing-library/react";

import { SiteLayout } from "@/components/SiteLayout";

describe("SiteLayout", () => {
  it("renders navigation and children", () => {
    render(
      <SiteLayout>
        <div>Inner content</div>
      </SiteLayout>
    );

    expect(screen.getByText("AB Agency")).toBeInTheDocument();
    expect(screen.getByText("Connexion")).toBeInTheDocument();
    expect(screen.getByText("Inner content")).toBeInTheDocument();
  });
});