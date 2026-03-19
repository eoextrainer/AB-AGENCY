import { HomePage } from "@/components/HomePage";
import { getHomepageData } from "@/lib/api";
import { getCmsSpotlight } from "@/lib/cms";

export default async function Page() {
  const [homepage, spotlight] = await Promise.all([getHomepageData(), getCmsSpotlight()]);
  return <HomePage homepage={homepage} spotlight={spotlight} />;
}