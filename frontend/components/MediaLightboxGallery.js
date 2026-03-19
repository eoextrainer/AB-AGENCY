"use client";

import { useState } from "react";

import { getYouTubeEmbedUrl, getYouTubeVideoId, isYouTubeAsset } from "@/lib/video";

export function MediaLightboxGallery({ assets = [] }) {
  const [activeAsset, setActiveAsset] = useState(null);

  if (!assets.length) {
    return <p className="muted">Galerie en preparation.</p>;
  }

  return (
    <>
      <div className="gallery-grid">
        {assets.map((asset) => {
          const preview = asset.thumbnail_url || asset.url;
          const isVideo = asset.asset_type === "video";
          return (
            <button key={asset.id || `${asset.asset_type}-${asset.title}`} className="gallery-tile" type="button" onClick={() => setActiveAsset(asset)}>
              <img src={preview} alt={asset.alt_text || asset.title} />
              <span className="gallery-badge">{isVideo ? "Video" : "Photo"}</span>
              <span className="gallery-caption">{asset.title}</span>
            </button>
          );
        })}
      </div>

      {activeAsset ? (
        <div className="lightbox" role="dialog" aria-modal="true" aria-label={activeAsset.title} onClick={() => setActiveAsset(null)}>
          <div className="lightbox-panel" onClick={(event) => event.stopPropagation()}>
            <div className="auth-actions">
              <div>
                <p className="eyebrow">Media</p>
                <h3>{activeAsset.title}</h3>
              </div>
              <button className="button button-secondary" type="button" onClick={() => setActiveAsset(null)}>
                Fermer
              </button>
            </div>
            <div className="lightbox-media">
              {activeAsset.asset_type === "video" ? (
                isYouTubeAsset(activeAsset.url) ? (
                  <iframe
                    src={getYouTubeEmbedUrl(getYouTubeVideoId(activeAsset.url))}
                    title={activeAsset.title}
                    allow="autoplay; encrypted-media; picture-in-picture"
                    referrerPolicy="strict-origin-when-cross-origin"
                    allowFullScreen
                  />
                ) : (
                  <video controls autoPlay src={activeAsset.url} poster={activeAsset.thumbnail_url || undefined} />
                )
              ) : (
                <img src={activeAsset.url} alt={activeAsset.alt_text || activeAsset.title} />
              )}
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}