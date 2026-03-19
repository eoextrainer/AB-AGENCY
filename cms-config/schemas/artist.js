export const artistSchema = {
  name: "artist",
  title: "Artist",
  type: "document",
  fields: [
    { name: "name", title: "Name", type: "string" },
    { name: "slug", title: "Slug", type: "slug", options: { source: "name" } },
    { name: "discipline", title: "Discipline", type: "string" },
    { name: "mood", title: "Mood", type: "string" },
    { name: "headline", title: "Headline", type: "text" },
    { name: "bio", title: "Bio", type: "text" },
    { name: "heroVideoUrl", title: "Hero video URL", type: "url" }
  ]
};