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

export async function getAdminAccessToken(credentials) {
  if (!credentials?.email || !credentials?.password) {
    return null;
  }

  try {
    const response = await fetch(buildApiUrl("/auth/login"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
      body: JSON.stringify(credentials)
    });

    if (!response.ok) {
      return null;
    }

    const payload = await response.json();
    return payload.access_token;
  } catch {
    return null;
  }
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
    return await fetchJson("/dashboard/overview", { headers: { Authorization: `Bearer ${token}` } });
  } catch {
    return null;
  }
}