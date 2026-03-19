export const cmsConfig = {
  provider: "sanity",
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID || "replace-me",
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET || "production",
  apiVersion: process.env.NEXT_PUBLIC_SANITY_API_VERSION || "2025-01-01"
};

export async function getCmsSpotlight() {
  return {
    title: "L'equipe de confiance derriere chaque reservation.",
    body: "AB Agency aligne direction artistique, planification technique et lisibilite commerciale pour faire passer un projet de l'inspiration a la reservation sans friction.",
    videoUrl: "https://cdn.coverr.co/videos/coverr-dance-performance-on-stage-1571730835234?download=1080p",
    videoPoster: "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=900&q=80",
    highlights: [
      "Une direction creative qui donne a chaque acte une presence editoriale nette et premium.",
      "Un formulaire de demande concu pour capter les dimensions, les besoins techniques et l'intention budgetaire.",
      "Une structure de contenu prete pour des pages artistes riches en photo, video et narration de service."
    ]
  };
}