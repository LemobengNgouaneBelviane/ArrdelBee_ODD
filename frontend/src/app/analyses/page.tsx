'use client';

import { Card, PageHeader, SectionTitle, Stat } from "@/components/ui";

export default function AnalysesPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        title="Analyses & Statistiques"
        subtitle="Suivi en temps réel de la performance ODD et des projets"
      />

      {/* KPIs Principaux */}
      <div className="space-y-3">
        <SectionTitle title="Indicateurs de Performance" />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Stat label="Taux d'Alignement Global" value="72%" color="success" icon="📊" />
          <Stat label="Couverture ODD" value="12/17" color="primary" icon="🎯" />
          <Stat label="Projets Actifs" value="687" color="default" icon="📁" />
          <Stat label="Indicateurs Saisis" value="1,240" color="default" icon="📈" />
        </div>
      </div>

      {/* Vue ODD */}
      <Card title="Performance par ODD">
        <div className="space-y-3">
          {[
            { code: "01", title: "Pas de Pauvreté", progress: 68, projects: 45 },
            { code: "03", title: "Santé et Bien-être", progress: 82, projects: 67 },
            { code: "04", title: "Éducation de Qualité", progress: 75, projects: 52 },
            { code: "06", title: "Eau Propre et Assainissement", progress: 45, projects: 28 },
            { code: "07", title: "Énergie Propre", progress: 59, projects: 34 },
            { code: "09", title: "Industrie et Infrastructures", progress: 65, projects: 41 },
          ].map((odd) => (
            <div key={odd.code} className="flex items-end justify-between rounded-lg border border-[color:var(--border)] p-3">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <div className="text-sm font-bold text-[color:var(--primary)]">ODD {odd.code}</div>
                  <div className="text-sm font-medium text-[color:var(--foreground)]">
                    {odd.title}
                  </div>
                </div>
                <div className="mt-2 h-2 rounded-full bg-[color:var(--border)]">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-[color:var(--primary)] to-[color:var(--primary)]/70"
                    style={{ width: `${odd.progress}%` }}
                  />
                </div>
              </div>
              <div className="ml-3 text-right">
                <div className="text-sm font-bold text-[color:var(--primary)]">{odd.progress}%</div>
                <div className="text-xs text-[color:var(--muted)]">{odd.projects} projets</div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Analyse par Secteur */}
      <Card title="Distribution par Secteur d'Activité">
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {[
            { sector: "Santé", projects: 124, allocation: "14.8M FCFA", progress: 72 },
            { sector: "Éducation", projects: 98, allocation: "9.5M FCFA", progress: 68 },
            { sector: "Infrastructures", projects: 156, allocation: "28.3M FCFA", progress: 65 },
            { sector: "Eau", projects: 67, allocation: "5.2M FCFA", progress: 78 },
            { sector: "Énergie", projects: 42, allocation: "3.9M FCFA", progress: 59 },
            { sector: "Agriculture", projects: 58, allocation: "2.8M FCFA", progress: 45 },
          ].map((item) => (
            <div key={item.sector} className="rounded-lg border border-[color:var(--border)] p-4">
              <div className="text-sm font-semibold text-[color:var(--foreground)]">
                {item.sector}
              </div>
              <div className="mt-3 space-y-2">
                <div className="flex justify-between text-xs text-[color:var(--muted)]">
                  <span>Projets</span>
                  <span className="font-semibold text-[color:var(--foreground)]">
                    {item.projects}
                  </span>
                </div>
                <div className="flex justify-between text-xs text-[color:var(--muted)]">
                  <span>Budget</span>
                  <span className="font-semibold text-[color:var(--foreground)]">
                    {item.allocation}
                  </span>
                </div>
                <div>
                  <div className="text-xs text-[color:var(--muted)]">Avancement</div>
                  <div className="mt-1 h-2 rounded-full bg-[color:var(--border)]">
                    <div
                      className="h-full rounded-full bg-[color:var(--primary)]"
                      style={{ width: `${item.progress}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Analyse Géographique */}
      <Card title="Couverture Géographique">
        <div className="space-y-3">
          {[
            { region: "Extrême-Nord", communes: 8, projects: 124, budget: 45.2, align: 68 },
            { region: "Nord", communes: 6, projects: 89, budget: 32.1, align: 72 },
            { region: "Adamaoua", communes: 5, projects: 67, budget: 24.5, align: 65 },
            { region: "Centre", communes: 3, projects: 156, budget: 67.8, align: 78 },
            { region: "Littoral", communes: 2, projects: 98, budget: 41.2, align: 71 },
          ].map((item) => (
            <div
              key={item.region}
              className="flex items-center justify-between rounded-lg border border-[color:var(--border)] p-3"
            >
              <div className="flex-1">
                <div className="font-semibold text-[color:var(--foreground)]">
                  {item.region}
                </div>
                <div className="mt-1 text-xs text-[color:var(--muted)]">
                  {item.communes} communes • {item.projects} projets
                </div>
              </div>
              <div className="text-right text-sm font-semibold text-[color:var(--primary)]">
                {item.align}%
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Timeline Exécution */}
      <Card title="Chronologie Exécution (2024-2025)">
        <div className="space-y-4">
          {[
            { period: "Q1 2024", progress: 42, status: "Achevé" },
            { period: "Q2 2024", progress: 65, status: "En Cours" },
            { period: "Q3 2024 (Prévu)", progress: 0, status: "Planifié" },
            { period: "Q4 2024 (Prévu)", progress: 0, status: "Planifié" },
          ].map((item) => (
            <div key={item.period}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-[color:var(--foreground)]">
                  {item.period}
                </span>
                <span
                  className={`text-xs font-semibold px-2 py-1 rounded-full ${
                    item.status === "Achevé"
                      ? "bg-emerald-100 text-emerald-700"
                      : item.status === "En Cours"
                        ? "bg-blue-100 text-blue-700"
                        : "bg-gray-100 text-gray-700"
                  }`}
                >
                  {item.status}
                </span>
              </div>
              <div className="h-3 rounded-full bg-[color:var(--border)]">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-[color:var(--primary)] to-[color:var(--primary)]/70 transition-all"
                  style={{ width: `${item.progress}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Données d'Export */}
      <Card title="Exporter les Données">
        <p className="mb-4 text-sm text-[color:var(--muted)]">
          Téléchargez les analyses en différents formats pour intégration externe
        </p>
        <div className="flex flex-wrap gap-3">
          <button className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
            📊 Exporter Excel
          </button>
          <button className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
            📈 Exporter CSV
          </button>
          <button className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
            📄 Générer PDF
          </button>
          <button className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
            🔗 API JSON
          </button>
        </div>
      </Card>
    </div>
  );
}
