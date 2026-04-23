import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { NavLink } from "@/components/NavLink";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ARRDEL — ODD (Test)",
  description: "Interfaces de test ARRDEL ODD",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="fr"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="app-shell min-h-screen text-[color:var(--foreground)]">
        <div className="flex min-h-screen w-full">
          <aside className="hidden w-72 shrink-0 border-r border-[color:var(--border)] bg-white/60 backdrop-blur lg:flex lg:flex-col overflow-y-auto">
            <div className="sticky top-0 space-y-8 bg-white/80 p-8 backdrop-blur border-b border-[color:var(--border)]">
              <div>
                <div className="text-base font-bold tracking-tight text-[color:var(--primary)]">ArrdelBee</div>
                <div className="mt-1 text-xs font-medium text-[color:var(--muted)]">ODD — Alignement & Suivi</div>
              </div>
              <nav className="space-y-1">
                <NavLink href="/" label="Tableau de Bord" />
                <NavLink href="/projets" label="Projets" />
                <NavLink href="/projets/non-alignes" label="Non Alignés" />
                <NavLink href="/alignements" label="Alignements" />
                <NavLink href="/collecte-preuves" label="Collecte & Preuves" />
                <NavLink href="/cartographie" label="Cartographie" />
                <NavLink href="/rapports" label="Rapports" />
                <NavLink href="/analyses" label="Analyses" />
                <NavLink href="/validation" label="Validation" />
              </nav>
              
              <nav className="space-y-1 border-t border-[color:var(--border)] pt-6 mt-6">
                <div className="px-2 text-xs font-bold uppercase tracking-wider text-[color:var(--muted)]">Administration</div>
                <NavLink href="/utilisateurs" label="Utilisateurs" />
                <NavLink href="/parametres" label="Paramètres" />
                <NavLink href="/archive" label="Archive" />
                <NavLink href="/aide" label="Aide & Support" />
              </nav>
            </div>
            
            <div className="flex-1 space-y-4 p-8">
              <div className="rounded-xl border border-[color:var(--border)] bg-gradient-to-br from-[color:var(--primary)]/5 to-[color:var(--primary)]/10 p-4 text-xs text-[color:var(--muted)]">
                <div className="font-semibold text-[color:var(--primary)]">API Backend</div>
                <div className="mt-2 font-mono text-[10px] text-[color:var(--foreground)]">
                  {process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000"}
                </div>
              </div>
            </div>
          </aside>

          <main className="flex-1 overflow-auto">
            <div className="mx-auto max-w-7xl space-y-8 px-6 py-10 lg:px-10 lg:py-12">
              <div className="rounded-2xl border border-[color:var(--border)] bg-white/80 p-8 shadow-sm backdrop-blur lg:p-10">
                {children}
              </div>
              <footer className="text-center text-xs text-[color:var(--muted)]/70 pb-8">
                <p>« ArrdelBee ODD » — Prototype 2026 | Les données du terrain au service du développement durable</p>
              </footer>
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}
