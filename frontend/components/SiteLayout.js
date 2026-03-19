import { navigation } from "@/lib/content";

export function SiteLayout({ children }) {
  return (
    <div className="shell">
      <header className="site-header">
        <div className="brand-lockup">
          <img className="brand-logo" src="/logo.png" alt="AB Agency logo" />
          <div>
            <p className="eyebrow">AB Agency</p>
            <h1 className="wordmark">La performance de prestige, structuree pour reserver avec confiance.</h1>
          </div>
        </div>
        <nav className="main-nav" aria-label="Primary">
          {navigation.map((item) => (
            <a key={item.href} href={item.href}>
              {item.label}
            </a>
          ))}
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}