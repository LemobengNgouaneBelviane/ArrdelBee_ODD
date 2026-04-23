'use client';

import { Card, PageHeader, SectionTitle, Stat } from "@/components/ui";

interface ArchivedItem {
  id: string;
  name: string;
  type: "rapport" | "projet" | "alignement";
  date: string;
  author: string;
  size: string;
}

const archivedItems: ArchivedItem[] = [
  {
    id: "1",
    name: "Rapport_Annuel_2022_Final.pdf",
    type: "rapport",
    date: "2023-01-15",
    author: "Admin Institutionnel",
    size: "2.4 MB",
  },
  {
    id: "2",
    name: "Alignement_ODD_T3_2022.xlsx",
    type: "alignement",
    date: "2022-09-30",
    author: "Ebolo Awa",
    size: "1.1 MB",
  },
  {
    id: "3",
    name: "Projet_Electrification_2021-2022.docx",
    type: "projet",
    date: "2022-12-20",
    author: "Jean Ebolowa",
    size: "850 KB",
  },
  {
    id: "4",
    name: "Synthese_Performance_2021.pdf",
    type: "rapport",
    date: "2022-02-14",
    author: "Marie Atangana",
    size: "3.2 MB",
  },
];

export default function ArchivePage() {
  const typeLabels = {
    rapport: "📑 Rapport",
    projet: "📁 Projet",
    alignement: "🎯 Alignement",
  };

  const typeIcons = {
    rapport: "📑",
    projet: "📁",
    alignement: "🎯",
  };

  return (
    <div className="space-y-10">
      <PageHeader
        title="Archive Digitale"
        subtitle="Historique et archive de tous les documents et projets archivés"
      />

      {/* Statistiques */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Documents Archivés" value="156" color="default" icon="📦" />
        <Stat label="Projets Terminés" value="42" color="success" icon="✓" />
        <Stat label="Rapports Finalisés" value="38" color="default" icon="📊" />
        <Stat label="Espace Utilisé" value="24.5 GB" color="default" icon="💾" />
      </div>

      {/* Filtres & Recherche */}
      <div className="flex flex-wrap gap-3">
        <select className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] hover:border-[color:var(--primary)]/50">
          <option>Tous les Types</option>
          <option>Rapports</option>
          <option>Projets</option>
          <option>Alignements</option>
        </select>
        <select className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] hover:border-[color:var(--primary)]/50">
          <option>Trier par Date (Plus Récent)</option>
          <option>Trier par Nom (A-Z)</option>
          <option>Trier par Taille</option>
        </select>
        <input
          type="text"
          placeholder="Rechercher dans l'archive..."
          className="flex-1 rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] placeholder-[color:var(--muted)]"
        />
      </div>

      {/* Liste des Éléments Archivés */}
      <div className="space-y-3">
        <SectionTitle 
          title="Documents Archivés"
          description="Consultez et téléchargez les documents archivés"
        />
        <div className="space-y-2">
          {archivedItems.map((item) => (
            <Card key={item.id} hoverable className="p-4">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div className="flex flex-1 items-start gap-4">
                  <div className="text-2xl">{typeIcons[item.type]}</div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-[color:var(--foreground)] truncate">
                      {item.name}
                    </h3>
                    <div className="mt-1 text-xs text-[color:var(--muted)]">
                      {typeLabels[item.type]} • Archivé le {new Date(item.date).toLocaleDateString("fr-FR")} • {item.size}
                    </div>
                    <div className="mt-1 text-xs text-[color:var(--muted)]">
                      Par {item.author}
                    </div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button className="rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-xs font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                    👁️ Consulter
                  </button>
                  <button className="rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-xs font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                    ⬇️ Télécharger
                  </button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Catégories */}
      <div>
        <SectionTitle title="Catégories d'Archive" />
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <Card>
            <div className="text-center">
              <div className="text-3xl">📑</div>
              <div className="mt-3 text-sm font-semibold text-[color:var(--foreground)]">
                Rapports Archivés
              </div>
              <div className="mt-1 text-2xl font-bold text-[color:var(--primary)]">
                38
              </div>
              <p className="mt-2 text-xs text-[color:var(--muted)]">
                Rapports trimestres, annuels et synthèses
              </p>
            </div>
          </Card>
          <Card>
            <div className="text-center">
              <div className="text-3xl">📁</div>
              <div className="mt-3 text-sm font-semibold text-[color:var(--foreground)]">
                Projets Archivés
              </div>
              <div className="mt-1 text-2xl font-bold text-[color:var(--primary)]">
                42
              </div>
              <p className="mt-2 text-xs text-[color:var(--muted)]">
                Projets terminés et fermés
              </p>
            </div>
          </Card>
          <Card>
            <div className="text-center">
              <div className="text-3xl">🎯</div>
              <div className="mt-3 text-sm font-semibold text-[color:var(--foreground)]">
                Alignements Archivés
              </div>
              <div className="mt-1 text-2xl font-bold text-[color:var(--primary)]">
                76
              </div>
              <p className="mt-2 text-xs text-[color:var(--muted)]">
                Fiches d'alignement historiques
              </p>
            </div>
          </Card>
        </div>
      </div>

      {/* Options d'Export en Masse */}
      <Card title="Exportation en Masse">
        <p className="mb-4 text-sm text-[color:var(--muted)]">
          Téléchargez plusieurs documents à la fois
        </p>
        <div className="space-y-3">
          <div className="flex items-center gap-3 rounded-lg border border-[color:var(--border)] p-3">
            <input type="checkbox" className="rounded border-[color:var(--border)]" />
            <span className="text-sm text-[color:var(--foreground)]">
              Tous les rapports de 2022
            </span>
            <span className="ml-auto text-xs text-[color:var(--muted)]">8 fichiers</span>
          </div>
          <div className="flex items-center gap-3 rounded-lg border border-[color:var(--border)] p-3">
            <input type="checkbox" className="rounded border-[color:var(--border)]" />
            <span className="text-sm text-[color:var(--foreground)]">
              Tous les alignements ODD
            </span>
            <span className="ml-auto text-xs text-[color:var(--muted)]">23 fichiers</span>
          </div>
          <div className="flex items-center gap-3 rounded-lg border border-[color:var(--border)] p-3">
            <input type="checkbox" className="rounded border-[color:var(--border)]" />
            <span className="text-sm text-[color:var(--foreground)]">
              Archive complète (2020-2023)
            </span>
            <span className="ml-auto text-xs text-[color:var(--muted)]">156 fichiers</span>
          </div>
          <button className="w-full rounded-lg bg-[color:var(--primary)] px-4 py-3 text-sm font-semibold text-white shadow-sm hover:shadow-md transition">
            ⬇️ Télécharger les Fichiers Sélectionnés
          </button>
        </div>
      </Card>

      {/* Politique de Rétention */}
      <Card title="Politique de Rétention des Données">
        <div className="space-y-3 text-sm text-[color:var(--muted)]">
          <p>
            Les documents archivés sont conservés pendant <strong>7 ans</strong> conformément à la réglementation.
          </p>
          <p>
            Les données sensibles sont chiffrées et sauvegardées sur des serveurs sécurisés.
          </p>
          <p>
            Une suppression automatique intervient après la période de rétention légale.
          </p>
        </div>
      </Card>
    </div>
  );
}
