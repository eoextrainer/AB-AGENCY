import "./globals.css";

import { SiteLayout } from "@/components/SiteLayout";

export const metadata = {
  title: "AB Agency",
  description: "A performance booking platform for luxury events, festivals, and brand experiences.",
  icons: {
    icon: "/logo.png",
    shortcut: "/logo.png",
    apple: "/logo.png"
  }
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <SiteLayout>{children}</SiteLayout>
      </body>
    </html>
  );
}