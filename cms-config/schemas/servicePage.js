export const servicePageSchema = {
  name: "servicePage",
  title: "Service Page",
  type: "document",
  fields: [
    { name: "title", title: "Title", type: "string" },
    { name: "slug", title: "Slug", type: "slug", options: { source: "title" } },
    { name: "summary", title: "Summary", type: "text" },
    { name: "body", title: "Body", type: "array", of: [{ type: "block" }] }
  ]
};