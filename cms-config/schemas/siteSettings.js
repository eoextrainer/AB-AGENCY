export const siteSettingsSchema = {
  name: "siteSettings",
  title: "Site Settings",
  type: "document",
  fields: [
    { name: "heroTitle", title: "Hero title", type: "string" },
    { name: "heroSubtitle", title: "Hero subtitle", type: "text" },
    { name: "trustMarkers", title: "Trust markers", type: "array", of: [{ type: "string" }] }
  ]
};