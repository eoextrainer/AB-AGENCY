import { AdminPageView } from "@/components/AdminPageView";
import { getAdminAccessToken, getDashboardSnapshot } from "@/lib/api";

export default async function AdminPage() {
  const token = await getAdminAccessToken({
    email: process.env.ADMIN_API_EMAIL || "admin@ab-agency.com",
    password: process.env.ADMIN_API_PASSWORD || "admin12345"
  });
  const dashboard = await getDashboardSnapshot(token || "");
  return <AdminPageView dashboard={dashboard} />;
}