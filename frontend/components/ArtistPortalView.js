"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { getArtistPortal, SESSION_TOKEN_KEY } from "@/lib/api";
import { MediaLightboxGallery } from "@/components/MediaLightboxGallery";

export function ArtistPortalView() {
  const router = useRouter();
  const [portal, setPortal] = useState(null);
  const [status, setStatus] = useState({ type: "loading", message: "Chargement de votre espace artiste..." });

  useEffect(() => {
    let isMounted = true;

    async function loadPortal() {
      const token = window.sessionStorage.getItem(SESSION_TOKEN_KEY);
      if (!token) {
        if (isMounted) {
          setStatus({ type: "error", message: "Aucune session active. Merci de vous connecter." });
        }
        return;
      }

      const profile = await getArtistPortal(token);
      if (!profile) {
        if (isMounted) {
          setStatus({ type: "error", message: "Le profil artiste est indisponible pour ce compte." });
        }
        return;
      }

      if (isMounted) {
        setPortal(profile);
        setStatus({ type: "success", message: "" });
      }
    }

    loadPortal();
    return () => {
      isMounted = false;
    };
  }, []);

  function handleLogout() {
    window.sessionStorage.removeItem(SESSION_TOKEN_KEY);
    window.sessionStorage.removeItem("abAgencyUsername");
    router.push("/login");
  }

  if (!portal) {
    return (
      <section className="panel">
        <p className="eyebrow">Espace artiste</p>
        <h2>{status.type === "loading" ? "Chargement en cours..." : "Connexion requise"}</h2>
        <p className="muted">{status.message}</p>
      </section>
    );
  }

  const { user, artist } = portal;

  return (
    <div className="page-stack portal-stack">
      <section className="panel profile-card">
        <div className="portal-header">
          <div>
            <p className="eyebrow">Espace artiste</p>
            <h2>{artist.name}</h2>
            <p className="muted">{artist.headline}</p>
          </div>
          <button className="button button-secondary" type="button" onClick={handleLogout}>
            Se deconnecter
          </button>
        </div>
        <div className="portal-grid">
          <div className="profile-layout">
            <img className="profile-portrait" src={artist.portrait_image_url || artist.media_assets?.[0]?.thumbnail_url || "/logo.png"} alt={artist.name} />
            <table className="info-table">
              <tbody>
                <tr>
                  <th>Nom</th>
                  <td>{user.full_name}</td>
                </tr>
                <tr>
                  <th>Nom d'utilisateur</th>
                  <td>{user.username}</td>
                </tr>
                <tr>
                  <th>Email</th>
                  <td>{user.email}</td>
                </tr>
                <tr>
                  <th>Discipline</th>
                  <td>{artist.discipline}</td>
                </tr>
                <tr>
                  <th>Experience</th>
                  <td>{artist.years_experience} ans</td>
                </tr>
                <tr>
                  <th>Base</th>
                  <td>{artist.location}</td>
                </tr>
                <tr>
                  <th>Langues</th>
                  <td>{artist.spoken_languages?.join(", ") || "Selon projet"}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="profile-layout">
            <p className="eyebrow">Resume artistique</p>
            <table className="resume-table">
              <thead>
                <tr>
                  <th>Periode</th>
                  <th>Production</th>
                  <th>Lieu</th>
                  <th>Role</th>
                </tr>
              </thead>
              <tbody>
                {(artist.performance_resume || []).map((entry) => (
                  <tr key={`${entry.period}-${entry.production}`}>
                    <td>{entry.period}</td>
                    <td>{entry.production}</td>
                    <td>{entry.venue}</td>
                    <td>{entry.role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="panel">
        <p className="eyebrow">Galerie curatoriale</p>
        <MediaLightboxGallery assets={artist.media_assets || []} />
      </section>
    </div>
  );
}