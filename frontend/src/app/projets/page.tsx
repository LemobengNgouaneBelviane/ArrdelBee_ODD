'use client';

import Link from "next/link";
import { Card, PageHeader, SectionTitle, Badge } from "@/components/ui";

interface Project {
  id: string;
  name: string;
  sector: string;
  alignment: "aligned" | "unaligned" | "pending";
  status: "actif" | "en-attente" | "acheve";
  budget: string;
  progress: number;
  oddCodes: string[];
  region: string;
  kpi?: { percentage: number; status: "red" | "yellow" | "green" };
}

const projects: Project[] = [
  {
    id: "1",
    name: "Réhabilitation de l'Axe Principal Sud-Ouest",
    sector: "INFRASTRUCTURES",
    alignment: "aligned",
    status: "actif",
    budget: "450M FCFA",
    progress: 65,
    oddCodes: ["09", "11"],
    region: "Extrême-Nord",
    kpi: { percentage: 78, status: "green" },
  },
  {
    id: "2",
    name: "Modernisation des Écoles Primaires Zone B",
    sector: "EDUCATION",
    alignment: "aligned",
    status: "acheve",
    budget: "312M FCFA",
    progress: 100,
    oddCodes: ["04"],
    region: "Centre",
    kpi: { percentage: 102, status: "green" },
  },
  {
    id: "3",
    name: "Construction Centre de Santé Intégré",
    sector: "SANTE",
    alignment: "pending",
    status: "en-attente",
    budget: "100M FCFA",
    progress: 48,
    oddCodes: ["03"],
    region: "Littoral",
    kpi: { percentage: 64, status: "yellow" },
  },
  {
    id: "4",
    name: "Extension du Réseau Électrique Rural",
    sector: "ENERGIE",
    alignment: "unaligned",
    status: "actif",
    budget: "210M FCFA",
    progress: 32,
    oddCodes: ["07"],
    region: "Adamaoua",
  },
  {
    id: "5",
    name: "Forages Hydrauliques Villageois",
    sector: "EAU",
    alignment: "aligned",
    status: "actif",
    budget: "45M FCFA",
    progress: 89,
    oddCodes: ["06"],
    region: "Nord-Ouest",
    kpi: { percentage: 82, status: "green" },
  },
];

export default function ProjectsPage() {
  const statusColors = {
    actif: "bg-emerald-50 border-emerald-200 text-emerald-700",
    "en-attente": "bg-amber-50 border-amber-200 text-amber-700",
    acheve: "bg-slate-50 border-slate-200 text-slate-700",
  };

  const alignmentColors = {
    aligned: { bg: "bg-green-50", border: "border-green-200", text: "text-green-700", label: "Aligné" },
    pending: { bg: "bg-yellow-50", border: "border-yellow-200", text: "text-yellow-700", label: "En Attente" },
    unaligned: { bg: "bg-red-50", border: "border-red-200", text: "text-red-700", label: "Non Aligné" },
  };

  const sectorColors: Record<string, string> = {
    INFRASTRUCTURES: "#8b6914",
    EDUCATION: "#0f4c75",
    SANTE: "#c6192b",
    ENERGIE: "#fccc0a",
    EAU: "#26bde2",
  };

  return (
    <div className="space-y-10">
      <PageHeader
        title="Projets"
        subtitle="Portefeuille complet des projets de développement"
        actions={
          <Link
            href="/projets/creer"
            className="inline-flex items-center rounded-lg bg-[color:var(--primary)] px-4 py-2 text-sm font-semibold text-white shadow-sm hover:shadow-md transition"
          >
            + Nouveau Projet
          </Link>
        }
      />

      {/* Filtres */}
      <div className="flex flex-wrap gap-3">
        <select className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] hover:border-[color:var(--primary)]/50">
          <option>Tous les Secteurs</option>
          <option>Infrastructure</option>
          <option>Éducation</option>
          <option>Santé</option>
          <option>Énergie</option>
          <option>Eau</option>
        </select>
        <select className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] hover:border-[color:var(--primary)]/50">
          <option>Tous les Statuts</option>
          <option>Actif</option>
          <option>En Attente</option>
          <option>Achevé</option>
        </select>
        <input
          type="text"
          placeholder="Rechercher un projet..."
          className="flex-1 rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] placeholder-[color:var(--muted)]"
        />
      </div>

      {/* Liste des Projets */}
      <div className="space-y-3">
        <SectionTitle 
          title={`Projets (${projects.length})`}
          description="Cliquez sur un projet pour voir les détails et l'alignement ODD"
        />
        <div className="space-y-3">
          {projects.map((project) => (
            <Link key={project.id} href={`/projets/${project.id}`}>
              <Card hoverable className="p-5">
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  <div className="flex-1">
                    <div className="flex flex-wrap items-center gap-3 mb-2">
                      <h3 className="text-base font-semibold text-[color:var(--foreground)]">
                        {project.name}
                      </h3>
                      <span
                        className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${statusColors[project.status]}`}
                      >
                        {project.status === "actif" && "✓ Actif"}
                        {project.status === "en-attente" && "⏳ En Attente"}
                        {project.status === "acheve" && "✓ Achevé"}
                      </span>
                      <span
                        className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${
                          alignmentColors[project.alignment].bg
                        } ${alignmentColors[project.alignment].border} ${alignmentColors[project.alignment].text}`}
                      >
                        {alignmentColors[project.alignment].label}
                      </span>
                    </div>
                    <p className="text-xs text-[color:var(--muted)]">
                      {project.region} • {project.sector}
                    </p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {project.oddCodes.map((code) => (
                        <Badge key={code} label={`ODD ${code}`} oddCode={code} />
                      ))}
                    </div>
                  </div>
                  <div className="flex shrink-0 flex-col items-end gap-3">
                    {project.kpi && (
                      <div className="text-right">
                        <div className={`text-sm font-semibold ${
                          project.kpi.status === "red" ? "text-red-600" :
                          project.kpi.status === "yellow" ? "text-yellow-600" :
                          "text-green-600"
                        }`}>
                          KPI {project.kpi.percentage}%
                        </div>
                        <div className="text-xs text-[color:var(--muted)] mt-1">
                          {project.kpi.status === "red" && "🔴 Alerte"}
                          {project.kpi.status === "yellow" && "🟡 À surveiller"}
                          {project.kpi.status === "green" && "Sur la bonne voie"}
                        </div>
                      </div>
                    )}
                    <div className="text-right">
                      <div className="text-sm font-semibold text-[color:var(--foreground)]">
                        {project.progress}%
                      </div>
                      <div className="mt-1 w-40">
                        <div className="h-2 rounded-full bg-[color:var(--border)]">
                          <div
                            className="h-full rounded-full bg-gradient-to-r from-[color:var(--primary)] to-[color:var(--primary)]/70 transition-all"
                            style={{ width: `${project.progress}%` }}
                          />
                        </div>
                      </div>
                    </div>
                    <div className="text-right text-xs font-medium text-[color:var(--muted)]">
                      {project.budget}
                    </div>
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Statistiques */}
      <div className="space-y-3">
        <SectionTitle title="Statistiques Globales" />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <Card>
            <div className="text-center">
              <div className="text-3xl font-bold text-[color:var(--primary)]">{projects.length}</div>
              <div className="mt-1 text-xs font-medium text-[color:var(--muted)]">Projets Totaux</div>
            </div>
          </Card>
          <Card>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">{projects.filter(p => p.alignment === "aligned").length}</div>
              <div className="mt-1 text-xs font-medium text-[color:var(--muted)]">Alignés</div>
            </div>
          </Card>
          <Card>
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-600">{projects.filter(p => p.alignment === "pending").length}</div>
              <div className="mt-1 text-xs font-medium text-[color:var(--muted)]">En Attente</div>
            </div>
          </Card>
          <Card>
            <div className="text-center">
              <div className="text-3xl font-bold text-red-600">{projects.filter(p => p.alignment === "unaligned").length}</div>
              <div className="mt-1 text-xs font-medium text-[color:var(--muted)]">Non Alignés</div>
            </div>
          </Card>
          <Card>
            <div className="text-center">
              <div className="text-3xl font-bold text-emerald-600">{projects.filter(p => p.status === "actif").length}</div>
              <div className="mt-1 text-xs font-medium text-[color:var(--muted)]">Actifs</div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
