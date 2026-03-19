"use client";

import { useMemo, useState } from "react";

import { submitInquiry } from "@/lib/api";

const initialState = {
  company_name: "",
  contact_name: "",
  email: "",
  phone: "",
  event_type: "Corporate Gala",
  event_date: "",
  location: "",
  venue_type: "Indoor",
  ceiling_height_meters: "",
  budget_min: "",
  budget_max: "",
  preferred_artist_slugs: [],
  preferred_disciplines: [],
  message: ""
};

export function InquiryPageView({ artists = [], initialArtist = "" }) {
  const [formState, setFormState] = useState({
    ...initialState,
    preferred_artist_slugs: initialArtist ? [initialArtist] : []
  });
  const [status, setStatus] = useState({ type: "idle", message: "" });
  const artistOptions = useMemo(() => artists.map((artist) => ({ slug: artist.slug, label: artist.name })), [artists]);

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus({ type: "loading", message: "Envoi de la demande en cours..." });

    try {
      const payload = {
        ...formState,
        event_date: formState.event_date || null,
        ceiling_height_meters: formState.ceiling_height_meters ? Number(formState.ceiling_height_meters) : null,
        budget_min: formState.budget_min ? Number(formState.budget_min) : null,
        budget_max: formState.budget_max ? Number(formState.budget_max) : null
      };
      const response = await submitInquiry(payload);
      setStatus({ type: "success", message: `Demande enregistree avec un score de priorite de ${response.lead_score}.` });
    } catch {
      setStatus({ type: "error", message: "L'envoi a echoue. Merci de reessayer ou de contacter l'equipe directement." });
    }
  }

  function toggleArtist(slug) {
    setFormState((current) => ({
      ...current,
      preferred_artist_slugs: current.preferred_artist_slugs.includes(slug)
        ? current.preferred_artist_slugs.filter((item) => item !== slug)
        : [...current.preferred_artist_slugs, slug]
    }));
  }

  return (
    <div className="page-stack">
      <section className="panel">
        <p className="eyebrow">Demande</p>
        <h2>Rassemblez les details de production qui font avancer la reservation.</h2>
        <p className="muted">Ce formulaire alimente directement le backend et evalue chaque demande selon le type d'evenement, l'adaptation du lieu et la solidite budgetaire.</p>
      </section>

      <form className="panel inquiry-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          <label>
            Societe
            <input value={formState.company_name} onChange={(event) => setFormState((current) => ({ ...current, company_name: event.target.value }))} required />
          </label>
          <label>
            Nom du contact
            <input value={formState.contact_name} onChange={(event) => setFormState((current) => ({ ...current, contact_name: event.target.value }))} required />
          </label>
          <label>
            Email
            <input type="email" value={formState.email} onChange={(event) => setFormState((current) => ({ ...current, email: event.target.value }))} required />
          </label>
          <label>
            Telephone
            <input value={formState.phone} onChange={(event) => setFormState((current) => ({ ...current, phone: event.target.value }))} />
          </label>
          <label>
            Type d'evenement
            <input value={formState.event_type} onChange={(event) => setFormState((current) => ({ ...current, event_type: event.target.value }))} required />
          </label>
          <label>
            Date de l'evenement
            <input type="datetime-local" value={formState.event_date} onChange={(event) => setFormState((current) => ({ ...current, event_date: event.target.value }))} />
          </label>
          <label>
            Lieu
            <input value={formState.location} onChange={(event) => setFormState((current) => ({ ...current, location: event.target.value }))} required />
          </label>
          <label>
            Type de lieu
            <input value={formState.venue_type} onChange={(event) => setFormState((current) => ({ ...current, venue_type: event.target.value }))} />
          </label>
          <label>
            Hauteur sous plafond (m)
            <input value={formState.ceiling_height_meters} onChange={(event) => setFormState((current) => ({ ...current, ceiling_height_meters: event.target.value }))} />
          </label>
          <label>
            Budget minimum
            <input value={formState.budget_min} onChange={(event) => setFormState((current) => ({ ...current, budget_min: event.target.value }))} />
          </label>
          <label>
            Budget maximum
            <input value={formState.budget_max} onChange={(event) => setFormState((current) => ({ ...current, budget_max: event.target.value }))} />
          </label>
        </div>
        <fieldset>
          <legend>Artistes preferes</legend>
          <div className="pill-grid">
            {artistOptions.map((artist) => (
              <label key={artist.slug} className="pill-checkbox">
                <input
                  checked={formState.preferred_artist_slugs.includes(artist.slug)}
                  type="checkbox"
                  onChange={() => toggleArtist(artist.slug)}
                />
                <span>{artist.label}</span>
              </label>
            ))}
          </div>
        </fieldset>
        <label>
          Disciplines souhaitees
          <input
            value={formState.preferred_disciplines.join(", ")}
            onChange={(event) =>
              setFormState((current) => ({
                ...current,
                preferred_disciplines: event.target.value
                  .split(",")
                  .map((item) => item.trim())
                  .filter(Boolean)
              }))
            }
            placeholder="Danse aerienne, Danse acrobatique, Solo"
          />
        </label>
        <label>
          Message
          <textarea rows="5" value={formState.message} onChange={(event) => setFormState((current) => ({ ...current, message: event.target.value }))} required />
        </label>
        <button className="button button-primary" type="submit">
          Envoyer la demande
        </button>
        <p role="status">{status.message}</p>
      </form>
    </div>
  );
}