import { AdminPageView } from "@/components/AdminPageView";
import { getAdminAccessToken, getDashboardSnapshot } from "@/lib/api";

export default async function AdminPage() {
  const token = await getAdminAccessToken({
    username: process.env.ADMIN_API_USERNAME || "admin",
    password: process.env.ADMIN_API_PASSWORD || "admin123"
  });
  const dashboard = await getDashboardSnapshot(token || "");
  return <AdminPageView dashboard={dashboard} />;
}