import "./globals.css";

import { SiteLayout } from "@/components/SiteLayout";

export const metadata = {
  title: "AB Agency",
  description: "Une plateforme de reservation artistique pour les evenements de luxe, les festivals et les experiences de marque.",
  icons: {
    icon: "/logo.png",
    shortcut: "/logo.png",
    apple: "/logo.png"
  }
};

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body>
        <SiteLayout>{children}</SiteLayout>
      </body>
    </html>
  );
}