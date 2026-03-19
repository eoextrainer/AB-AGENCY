import { renderToStaticMarkup } from "react-dom/server";

import RootLayout from "@/app/layout";

describe("RootLayout", () => {
  it("wraps children in the html shell", () => {
    const markup = renderToStaticMarkup(RootLayout({ children: <div>Page body</div> }));

    expect(markup).toContain("Page body");
    expect(markup).toContain("AB Agency");
  });
});