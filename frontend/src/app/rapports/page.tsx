'use client';

import Link from "next/link";
import { Card, PageHeader, SectionTitle, Stat } from "@/components/ui";

interface Report {
  id: string;
  title: string;
  type: "trimestriel" | "annuel" | "strategique";
  date: string;
  status: "finalize" | "draft" | "archived";
  author: string;
}

const reports: Report[] = [
  {
    id: "1",
    title: "Rapport Trimestriel Q1 2024",
    type: "trimestriel",
    date: "2024-03-31",
    status: "finalize",
    author: "Admin Institutionnel",
  },
  {
    id: "2",
    title: "Note de Synthèse Décisionnelle CMR-ODD-2024",
    type: "strategique",
    date: "2024-06-15",
    status: "finalize",
    author: "Mandel In",
  },
  {
    id: "3",
    title: "Rapport Annuel 2023 - Impacts & Performance",
    type: "annuel",
    date: "2024-01-20",
    status: "archived",
    author: "Ebolo Awa",
  },
  {
    id: "4",
    title: "Rapport Trimestriel Q2 2024",
    type: "trimestriel",
    date: "2024-06-30",
    status: "draft",
    author: "Admin Institutionnel",
  },
];

export default function ReportsPage() {
  const typeLabels = {
    trimestriel: "Trimestriel",
    annuel: "Annuel",
    strategique: "Stratégique",
  };

  const statusLabels = {
    finalize: "Finalisé",
    draft: "Brouillon",
    archived: "Archivé",
  };

  const statusColors = {
    finalize: "bg-emerald-50 border-emerald-200 text-emerald-700",
    draft: "bg-amber-50 border-amber-200 text-amber-700",
    archived: "bg-slate-50 border-slate-200 text-slate-700",
  };

  return (
    <div className="space-y-10">
      <PageHeader
        title="Rapports"
        subtitle="Génération et archive des rapports institutionnels ODD"
        actions={
          <button className="inline-flex items-center rounded-lg bg-[color:var(--primary)] px-4 py-2 text-sm font-semibold text-white shadow-sm hover:shadow-md transition">
            + Générer Rapport
          </button>
        }
      />

      {/* Sections Principales */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Rapports Finalisés" value="8" color="success" icon="✓" />
        <Stat label="Rapports en Brouillon" value="1" color="default" icon="📝" />
        <Stat label="Archivés" value="15" color="default" icon="📦" />
        <Stat label="Dernière Mise à Jour" value="06 Jun" color="default" icon="📅" />
      </div>

      {/* Onglets/Filtres */}
      <div className="flex flex-wrap gap-3 border-b border-[color:var(--border)] pb-4">
        <button className="px-4 py-2 text-sm font-semibold text-[color:var(--primary)] border-b-2 border-[color:var(--primary)]">
          Tous
        </button>
        <button className="px-4 py-2 text-sm font-semibold text-[color:var(--muted)] hover:text-[color:var(--foreground)]">
          Finalisés
        </button>
        <button className="px-4 py-2 text-sm font-semibold text-[color:var(--muted)] hover:text-[color:var(--foreground)]">
          Brouillons
        </button>
        <button className="px-4 py-2 text-sm font-semibold text-[color:var(--muted)] hover:text-[color:var(--foreground)]">
          Archivés
        </button>
      </div>

      {/* Liste des Rapports */}
      <div className="space-y-3">
        <SectionTitle 
          title={`Rapports (${reports.length})`}
          description="Cliquez pour consulter, télécharger ou modifier un rapport"
        />
        <div className="space-y-3">
          {reports.map((report) => (
            <Card key={report.id} hoverable className="p-5">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div className="flex-1">
                  <div className="flex flex-wrap items-center gap-3">
                    <h3 className="text-base font-semibold text-[color:var(--foreground)]">
                      {report.title}
                    </h3>
                    <span
                      className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${statusColors[report.status]}`}
                    >
                      {statusLabels[report.status]}
                    </span>
                  </div>
                  <div className="mt-2 text-xs text-[color:var(--muted)]">
                    {typeLabels[report.type]} • {new Date(report.date).toLocaleDateString("fr-FR")} • Par {report.author}
                  </div>
                </div>
                <div className="flex shrink-0 gap-2">
                  <button className="rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                    👁️ Consulter
                  </button>
                  <button className="rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                    ⬇️ Télécharger
                  </button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Générateur de Rapports */}
      <Card title="Générateur de Rapports">
        <div className="space-y-4">
          <p className="text-sm text-[color:var(--muted)]">
            Créez un rapport personnalisé en sélectionnant les critères ci-dessous
          </p>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-[color:var(--foreground)]">
                Type de Rapport
              </label>
              <select className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-sm text-[color:var(--foreground)]">
                <option>Rapport Trimestriel</option>
                <option>Rapport Annuel</option>
                <option>Note Décisionnelle</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-[color:var(--foreground)]">
                Période
              </label>
              <select className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-sm text-[color:var(--foreground)]">
                <option>Q1 2024</option>
                <option>Q2 2024</option>
                <option>2024</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-[color:var(--foreground)]">
                Secteur Focus
              </label>
              <select className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-sm text-[color:var(--foreground)]">
                <option>Tous les Secteurs</option>
                <option>Santé</option>
                <option>Éducation</option>
                <option>Infrastructures</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-[color:var(--foreground)]">
                Région
              </label>
              <select className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-sm text-[color:var(--foreground)]">
                <option>Toutes les Régions</option>
                <option>Extrême-Nord</option>
                <option>Nord</option>
                <option>Adamaoua</option>
              </select>
            </div>
          </div>
          <button className="w-full rounded-lg bg-[color:var(--primary)] px-4 py-3 text-sm font-semibold text-white shadow-sm hover:shadow-md transition">
            📊 Générer le Rapport
          </button>
        </div>
      </Card>
    </div>
  );
}
