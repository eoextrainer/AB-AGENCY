const PUBLIC_API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";
const SERVER_API_BASE_URL = process.env.NEXT_SERVER_API_BASE_URL || PUBLIC_API_BASE_URL;
export const SESSION_TOKEN_KEY = "abAgencySessionToken";

function getApiBaseUrl() {
  return typeof window === "undefined" ? SERVER_API_BASE_URL : PUBLIC_API_BASE_URL;
}

export function buildApiUrl(path) {
  return `${getApiBaseUrl()}${path}`;
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
  if (!(credentials?.identity || credentials?.username || credentials?.email) || !credentials?.password) {
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
      hero_title: "Des performances qui suspendent l'incredulite.",
      hero_subtitle: "AB Agency imagine des actes aeriens, acrobatiques et immersifs pour les evenements de luxe, les festivals et les marques exigeantes.",
      featured_artists: [],
      trust_markers: ["Accompagnement international", "Preparation technique anticipee", "Reponse rapide pour les equipes evenementielles"],
      featured_services: ["Representation artistique", "Pilotage de production", "Conseil creatif"]
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

export async function getCurrentUser(token) {
  if (!token) {
    return null;
  }

  try {
    return await fetchJson("/auth/me", { headers: { Authorization: `Bearer ${token}` } });
  } catch {
    return null;
  }
}

export async function getArtistPortal(token) {
  if (!token) {
    return null;
  }

  try {
    return await fetchJson("/artists/me/profile", { headers: { Authorization: `Bearer ${token}` } });
  } catch {
    return null;
  }
}