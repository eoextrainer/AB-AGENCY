import { ArtistsPageView } from "@/components/ArtistsPageView";
import { getArtists } from "@/lib/api";

export default async function ArtistsPage() {
  const artists = await getArtists();
  return <ArtistsPageView artists={artists} />;
}