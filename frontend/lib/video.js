const DEFAULT_ARTIST_VIDEO_IDS = ["zreMvcHghP8", "X4nEnyLoOcU", "fEZdmgHNa10", "ZWS6K_8N9E0", "4sXCTnk0yfs"];

export const FEATURED_ARTIST_VIDEO_IDS = {
  "ambre-acrobatique": "zreMvcHghP8",
  "celeste-aerienne": "X4nEnyLoOcU",
  "santiago-salsa": "fEZdmgHNa10",
  "luna-silk-duo": "ZWS6K_8N9E0",
  "volt-cyr": "4sXCTnk0yfs"
};

export function getYouTubeVideoId(url = "") {
  if (!url) {
    return null;
  }

  const normalizedUrl = url.trim();
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtube\.com\/embed\/|youtu\.be\/)([A-Za-z0-9_-]{11})/,
    /(?:youtube-nocookie\.com\/embed\/)([A-Za-z0-9_-]{11})/
  ];

  for (const pattern of patterns) {
    const match = normalizedUrl.match(pattern);
    if (match) {
      return match[1];
    }
  }

  return null;
}

export function getYouTubeEmbedUrl(videoId) {
  return `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&mute=1&loop=1&playlist=${videoId}&controls=0&modestbranding=1&rel=0&playsinline=1`;
}

export function getArtistVideoId(artist, index = 0) {
  if (!artist) {
    return DEFAULT_ARTIST_VIDEO_IDS[index % DEFAULT_ARTIST_VIDEO_IDS.length];
  }

  const directVideoId = FEATURED_ARTIST_VIDEO_IDS[artist.slug];
  if (directVideoId) {
    return directVideoId;
  }

  const candidates = [artist.teaser_video_url, artist.hero_video_url, ...(artist.media_assets || []).filter((asset) => asset.asset_type === "video").map((asset) => asset.url)];
  for (const candidate of candidates) {
    const videoId = getYouTubeVideoId(candidate);
    if (videoId) {
      return videoId;
    }
  }

  return DEFAULT_ARTIST_VIDEO_IDS[index % DEFAULT_ARTIST_VIDEO_IDS.length];
}

export function isYouTubeAsset(url = "") {
  return Boolean(getYouTubeVideoId(url));
}