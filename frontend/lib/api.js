const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

export function buildApiUrl(path) {
  return `${API_BASE_URL}${path}`;
}

async function fetchJson(path, options = {}) {
  const response = await fetch(buildApiUrl(path), {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    cache: options.cache || "no-store"
  });

  if (!response.ok) {
    throw new Error(`API request failed for ${path}`);
  }

  return response.json();
}

export async function getHomepageData() {
  try {
    return await fetchJson("/public/homepage");
  } catch {
    return {
      hero_title: "Performance that suspends disbelief.",
      hero_subtitle: "AB Agency curates aerial, acrobatic, and immersive acts for luxury, festival, and brand events.",
      featured_artists: [],
      trust_markers: ["International touring support", "Rigging-aware production planning", "Fast response for event planners"],
      featured_services: ["Talent Representation", "Production Support", "Creative Consulting"]
    };
  }
}

export async function getArtists() {
  try {
    return await fetchJson("/artists");
  } catch {
    return [];
  }
}

export async function submitInquiry(payload) {
  return fetchJson("/inquiries", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function getDashboardSnapshot(token) {
  if (!token) {
    return null;
  }

  try {
    const [stats, inquiries, bookings, availability] = await Promise.all([
      fetchJson("/dashboard/stats", { headers: { Authorization: `Bearer ${token}` } }),
      fetchJson("/inquiries", { headers: { Authorization: `Bearer ${token}` } }),
      fetchJson("/bookings", { headers: { Authorization: `Bearer ${token}` } }),
      fetchJson("/availability", { headers: { Authorization: `Bearer ${token}` } })
    ]);

    return { stats, inquiries, bookings, availability };
  } catch {
    return null;
  }
}