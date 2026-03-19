import { AdminPageView } from "@/components/AdminPageView";
import { getDashboardSnapshot } from "@/lib/api";

export default async function AdminPage() {
  const dashboard = await getDashboardSnapshot(process.env.NEXT_PUBLIC_ADMIN_TOKEN || "");
  return <AdminPageView dashboard={dashboard} />;
}