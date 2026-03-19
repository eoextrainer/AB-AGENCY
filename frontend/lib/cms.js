export const cmsConfig = {
  provider: "sanity",
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID || "replace-me",
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET || "production",
  apiVersion: process.env.NEXT_PUBLIC_SANITY_API_VERSION || "2025-01-01"
};

export async function getCmsSpotlight() {
  return {
    title: "The dream team behind every booking.",
    body: "AB Agency aligns artistry, technical planning, and buyer confidence so event planners can move from inspiration to booking without friction.",
    highlights: [
      "Creative direction that frames each act with luxury editorial clarity.",
      "Sales-aware inquiry design that captures venue dimensions, production needs, and budget intent.",
      "Headless CMS-ready content modeling for video-heavy artist pages and service storytelling."
    ]
  };
}