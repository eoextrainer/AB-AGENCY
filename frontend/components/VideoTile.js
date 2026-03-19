import { getYouTubeEmbedUrl } from "@/lib/video";

export function VideoTile({ label, videoId, className = "" }) {
  const tileClassName = ["video-tile", className].filter(Boolean).join(" ");

  return (
    <div className={tileClassName}>
      <iframe
        src={getYouTubeEmbedUrl(videoId)}
        title={label}
        allow="autoplay; encrypted-media; picture-in-picture"
        referrerPolicy="strict-origin-when-cross-origin"
        allowFullScreen
      />
      <span className="video-tile-label">{label}</span>
    </div>
  );
}