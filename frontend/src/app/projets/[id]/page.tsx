'use client';

import Link from "next/link";
import { Card, PageHeader, SectionTitle, Badge, Stat } from "@/components/ui";

interface PageProps {
  params: {
    id: string;
  };
}

export default function ProjectDetailPage({ params }: PageProps) {
  const projectId = params.id;

  // Fake data - remplace par une vraie requête API
  const project = {
    name: "Réhabilitation de l'Axe Principal Sud-Ouest",
    region: "Extrême-Nord",
    department: "Diamaré",
    sector: "Infrastructures",
    status: "actif",
    budget: 450000000,
    spent: 292500000,
    startDate: "2024-01-15",
    endDate: "2025-12-31",
    description:
      "Amélioration stratégique de l'infrastructure de transport pour stimuler le commerce régional et faciliter les exportations agricoles vers les centres urbains.",
    oddAlignments: [
      { code: "09", title: "Industrie, Innovation et Infrastructures", impact: 65 },
      { code: "11", title: "Villes et Communautés Durables", impact: 45 },
    ],
    beneficiaries: "12 Coopératives Locales",
    keyIndicators: [
      { label: "Taux d'exécution", value: "65%", icon: "📊" },
      { label: "Bénéficiaires Directs", value: "4,250", icon: "👥" },
      { label: "Communes Couvertes", value: "7", icon: "🗺️" },
    ],
    activities: [
      {
        id: 1,
        name: "Réfection du revêtement bitumé",
        status: "en-cours",
        progress: 75,
      },
      {
        id: 2,
        name: "Installation de bornes kilométriques",
        status: "en-cours",
        progress: 45,
      },
      {
        id: 3,
        name: "Mise en place de zones de repos",
        status: "planifié",
        progress: 0,
      },
    ],
  };

  return (
    <div className="space-y-10">
      <PageHeader
        title={project.name}
        subtitle={`${project.region}, ${project.department}`}
        actions={
          <Link
            href="/projets"
            className="inline-flex items-center rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)]"
          >
            ← Retour
          </Link>
        }
      />

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Overview */}
          <Card title="Informations Générales">
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <div className="text-xs font-medium uppercase text-[color:var(--muted)]">
                  Secteur d'Activité
                </div>
                <div className="mt-1 text-sm font-semibold text-[color:var(--foreground)]">
                  {project.sector}
                </div>
              </div>
              <div>
                <div className="text-xs font-medium uppercase text-[color:var(--muted)]">
                  Statut
                </div>
                <div className="mt-1">
                  <span className="inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700">
                    ✓ {project.status}
                  </span>
                </div>
              </div>
              <div>
                <div className="text-xs font-medium uppercase text-[color:var(--muted)]">
                  Date de Début
                </div>
                <div className="mt-1 text-sm font-semibold text-[color:var(--foreground)]">
                  {new Date(project.startDate).toLocaleDateString("fr-FR")}
                </div>
              </div>
              <div>
                <div className="text-xs font-medium uppercase text-[color:var(--muted)]">
                  Date de Fin
                </div>
                <div className="mt-1 text-sm font-semibold text-[color:var(--foreground)]">
                  {new Date(project.endDate).toLocaleDateString("fr-FR")}
                </div>
              </div>
            </div>
          </Card>

          {/* Budget */}
          <Card title="Budget & Exécution">
            <div className="space-y-4">
              <div>
                <div className="flex items-end justify-between">
                  <span className="text-sm font-medium text-[color:var(--muted)]">Exécution</span>
                  <span className="text-lg font-bold text-[color:var(--primary)]">
                    {Math.round((project.spent / project.budget) * 100)}%
                  </span>
                </div>
                <div className="mt-2 h-3 rounded-full bg-[color:var(--border)]">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-[color:var(--primary)] to-[color:var(--primary)]/70"
                    style={{
                      width: `${Math.round((project.spent / project.budget) * 100)}%`,
                    }}
                  />
                </div>
              </div>
              <div className="grid gap-3 pt-3 sm:grid-cols-2">
                <div className="rounded-lg bg-[color:var(--surface-2)] p-3">
                  <div className="text-xs font-medium text-[color:var(--muted)]">Budget Total</div>
                  <div className="mt-1 text-lg font-bold text-[color:var(--foreground)]">
                    {(project.budget / 1000000).toFixed(0)}M FCFA
                  </div>
                </div>
                <div className="rounded-lg bg-emerald-50 p-3 border border-emerald-200">
                  <div className="text-xs font-medium text-emerald-700">Montant Dépensé</div>
                  <div className="mt-1 text-lg font-bold text-emerald-700">
                    {(project.spent / 1000000).toFixed(0)}M FCFA
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* ODD Alignments */}
          <Card title="Alignements ODD">
            <div className="space-y-3">
              {project.oddAlignments.map((odd) => (
                <div key={odd.code} className="flex items-end justify-between rounded-lg border border-[color:var(--border)] p-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <Badge label={`ODD ${odd.code}`} oddCode={odd.code} />
                      <span className="text-sm font-medium text-[color:var(--foreground)]">
                        {odd.title}
                      </span>
                    </div>
                  </div>
                  <div className="ml-3 text-right">
                    <div className="text-sm font-bold text-[color:var(--primary)]">{odd.impact}%</div>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Activities */}
          <Card title="Activités Principales">
            <div className="space-y-3">
              {project.activities.map((activity) => (
                <div key={activity.id} className="border-l-2 border-[color:var(--primary)] pl-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="font-semibold text-[color:var(--foreground)]">
                        {activity.name}
                      </h4>
                      <span
                        className={`inline-block mt-1 text-xs font-medium px-2 py-1 rounded-full ${
                          activity.status === "en-cours"
                            ? "bg-blue-100 text-blue-700"
                            : "bg-gray-100 text-gray-700"
                        }`}
                      >
                        {activity.status === "en-cours" ? "En Cours" : "Planifié"}
                      </span>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-bold text-[color:var(--primary)]">
                        {activity.progress}%
                      </div>
                    </div>
                  </div>
                  <div className="mt-2 h-2 rounded-full bg-[color:var(--border)]">
                    <div
                      className="h-full rounded-full bg-[color:var(--primary)]"
                      style={{ width: `${activity.progress}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Key Stats */}
          <div className="space-y-3">
            <SectionTitle title="Indicateurs Clés" />
            {project.keyIndicators.map((indicator, idx) => (
              <Stat
                key={idx}
                label={indicator.label}
                value={indicator.value}
                icon={indicator.icon}
              />
            ))}
          </div>

          {/* Beneficiaries */}
          <Card title="Bénéficiaires">
            <div className="space-y-2">
              <p className="text-sm text-[color:var(--muted)]">
                Directement Concernés
              </p>
              <div className="text-2xl font-bold text-[color:var(--primary)]">
                {project.beneficiaries}
              </div>
            </div>
          </Card>

          {/* Quick Actions */}
          <Card title="Actions">
            <div className="space-y-2">
              <button className="w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                📋 Voir Preuves
              </button>
              <button className="w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                ✏️ Modifier
              </button>
              <button className="w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                📊 Générer Rapport
              </button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
