"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { getAdminAccessToken, getCurrentUser, SESSION_TOKEN_KEY } from "@/lib/api";

const demoCredentials = [
  { label: "Administrateur", username: "admin", password: "admin123" },
  { label: "Danse acrobatique", username: "ambre", password: "pass123" },
  { label: "Danse aerienne", username: "celeste", password: "pass123" },
  { label: "Danse salsa", username: "santiago", password: "pass123" }
];

export function LoginPageView() {
  const router = useRouter();
  const [formState, setFormState] = useState({ username: "", password: "" });
  const [status, setStatus] = useState({ type: "idle", message: "" });

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus({ type: "loading", message: "Connexion en cours..." });

    const token = await getAdminAccessToken({ username: formState.username, password: formState.password });
    if (!token) {
      setStatus({ type: "error", message: "Identifiants invalides ou compte non approuve." });
      return;
    }

    const currentUser = await getCurrentUser(token);
    if (!currentUser?.is_active) {
      setStatus({ type: "error", message: "Ce compte n'est pas autorise a acceder a l'espace." });
      return;
    }

    window.sessionStorage.setItem(SESSION_TOKEN_KEY, token);
    window.sessionStorage.setItem("abAgencyUsername", currentUser.username);

    if (currentUser.role === "admin") {
      setStatus({ type: "success", message: "Connexion administrateur reussie." });
      router.push("/admin");
      return;
    }

    setStatus({ type: "success", message: "Connexion artiste reussie." });
    router.push("/espace-artiste");
  }

  return (
    <div className="page-stack">
      <section className="panel auth-shell">
        <div>
          <p className="eyebrow">Connexion</p>
          <h2>Accedez a votre espace en toute discretion.</h2>
          <p className="muted">Les comptes administrateur et artistes sont verifies directement contre le backend et la base de donnees.</p>
        </div>
        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Nom d'utilisateur
            <input value={formState.username} onChange={(event) => setFormState((current) => ({ ...current, username: event.target.value }))} required />
          </label>
          <label>
            Mot de passe
            <input type="password" value={formState.password} onChange={(event) => setFormState((current) => ({ ...current, password: event.target.value }))} required />
          </label>
          <div className="auth-actions">
            <button className="button button-primary" type="submit">
              Se connecter
            </button>
            <p role="status">{status.message}</p>
          </div>
        </form>
        <details className="credentials-drawer">
          <summary>Afficher les identifiants de demonstration</summary>
          <div className="credentials-list">
            {demoCredentials.map((credential) => (
              <div key={credential.username} className="credential-item">
                <strong>{credential.label}</strong>
                <span>Nom d'utilisateur: {credential.username}</span>
                <span>Mot de passe: {credential.password}</span>
              </div>
            ))}
          </div>
        </details>
      </section>
    </div>
  );
}