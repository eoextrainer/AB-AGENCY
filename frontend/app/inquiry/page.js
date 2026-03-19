import { InquiryPageView } from "@/components/InquiryPageView";
import { getArtists } from "@/lib/api";

export default async function InquiryPage({ searchParams }) {
  const artists = await getArtists();
  const resolvedParams = await searchParams;
  const initialArtist = resolvedParams?.artist || "";

  return <InquiryPageView artists={artists} initialArtist={initialArtist} />;
}