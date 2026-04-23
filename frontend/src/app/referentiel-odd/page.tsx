"use client";

import { useState, useMemo } from "react";
import { PageHeader, SectionTitle, Badge, Card, Input } from "@/components/ui";

const ODDS = [
  { code: "01", name: "Pas de Pauvreté", description: "Éliminer la pauvreté sous toutes ses formes", color: "#e5243b", indicators: 5 },
  { code: "02", name: "Faim Zéro", description: "Éliminer la faim, assurer la sécurité alimentaire", color: "#dda63b", indicators: 8 },
  { code: "03", name: "Bonne Santé et Bien-être", description: "Assurer la santé et le bien-être pour tous", color: "#4c9f38", indicators: 13 },
  { code: "04", name: "Éducation de Qualité", description: "Assurer une éducation inclusive et équitable", color: "#c6192b", indicators: 10 },
  { code: "05", name: "Égalité des Genres", description: "Réaliser l'égalité des genres", color: "#ff3a21", indicators: 9 },
  { code: "06", name: "Eau Propre et Assainissement", description: "Garantir l'accès à l'eau et l'assainissement", color: "#26bde2", indicators: 8 },
  { code: "07", name: "Énergie Propre et D'un Coût Abordable", description: "Assurer l'accès à une énergie fiable et durable", color: "#fccc0a", indicators: 5 },
  { code: "08", name: "Travail Décent et Croissance Économique", description: "Promouvoir le travail décent pour tous", color: "#a21e48", indicators: 12 },
  { code: "09", name: "Industrie, Innovation et Infrastructure", description: "Bâtir une infrastructure résiliente", color: "#dd1c3b", indicators: 8 },
  { code: "10", name: "Réduction des Inégalités", description: "Réduire les inégalités entre les pays et en leur sein", color: "#dd1c3b", indicators: 11 },
  { code: "11", name: "Villes et Communautés Durables", description: "Créer des villes inclusives et durables", color: "#fd6925", indicators: 10 },
  { code: "12", name: "Consommation et Production Responsables", description: "Assurer des modes de consommation durable", color: "#bf8b2e", indicators: 11 },
  { code: "13", name: "Mesures Relatives à la Lutte Contre les Changements Climatiques", description: "Prendre d'urgence des mesures pour lutter contre le climat", color: "#407d52", indicators: 5 },
  { code: "14", name: "Vie Aquatique", description: "Conserver et exploiter océans, mers et ressources marines", color: "#0a97d9", indicators: 10 },
  { code: "15", name: "Vie Terrestre", description: "Préserver et restaurer les écosystèmes terrestres", color: "#56c596", indicators: 12 },
  { code: "16", name: "Paix, Justice et Institutions Efficaces", description: "Promouvoir la paix et l'accès à la justice", color: "#00689d", indicators: 12 },
  { code: "17", name: "Partenariats pour l'Atteinte des Objectifs", description: "Renforcer les moyens de mise en œuvre", color: "#1fbf9b", indicators: 19 },
];

export default function Page() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedOdd, setSelectedOdd] = useState<string | null>(null);

  const filteredOdds = useMemo(() => {
    if (!searchQuery.trim()) return ODDS;
    const q = searchQuery.toLowerCase();
    return ODDS.filter(
      (odd) =>
        odd.name.toLowerCase().includes(q) ||
        odd.description.toLowerCase().includes(q) ||
        odd.code.includes(q)
    );
  }, [searchQuery]);

  const detailedOdd = selectedOdd ? ODDS.find((o) => o.code === selectedOdd) : null;

  return (
    <div className="space-y-8">
      <PageHeader
        title="Référentiel ODD"
        subtitle="Les 17 Objectifs de Développement Durable des Nations Unies — Description complète et indicateurs"
      />

      {/* Recherche */}
      <div>
        <Input
          label="Rechercher un ODD"
          placeholder="Par code (01), nom ou description..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Liste des ODD */}
        <div className="lg:col-span-2">
          <SectionTitle title={`ODD Disponibles (${filteredOdds.length})`} />
          <div className="mt-4 space-y-3">
            {filteredOdds.map((odd) => (
              <button
                key={odd.code}
                onClick={() => setSelectedOdd(odd.code)}
                className={`w-full text-left rounded-xl border transition p-4 ${
                  selectedOdd === odd.code
                    ? "border-[color:var(--primary)] bg-[color:var(--primary)]/5"
                    : "border-[color:var(--border)] bg-white hover:bg-[color:var(--surface-2)]"
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <Badge label={`ODD ${odd.code}`} oddCode={odd.code} />
                      <div className="font-semibold text-[color:var(--foreground)]">{odd.name}</div>
                    </div>
                    <p className="mt-2 text-sm text-[color:var(--muted)] leading-relaxed">{odd.description}</p>
                  </div>
                  <div className="shrink-0 text-xs font-medium text-[color:var(--muted)]">{odd.indicators} indicateurs</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Détail ODD sélectionné */}
        <div className="lg:col-span-1">
          {detailedOdd ? (
            <div className="sticky top-8 space-y-4">
              <SectionTitle title="Détails" />
              <Card>
                <div
                  className="h-2 -m-6 mb-4 rounded-t-2xl"
                  style={{ backgroundColor: detailedOdd.color }}
                />
                <div className="space-y-4">
                  <div>
                    <div className="text-xs font-medium text-[color:var(--muted)] uppercase">Code</div>
                    <div className="mt-1 text-lg font-bold text-[color:var(--foreground)]">ODD {detailedOdd.code}</div>
                  </div>

                  <div>
                    <div className="text-xs font-medium text-[color:var(--muted)] uppercase">Objectif</div>
                    <div className="mt-1 font-semibold text-[color:var(--foreground)]">{detailedOdd.name}</div>
                  </div>

                  <div>
                    <div className="text-xs font-medium text-[color:var(--muted)] uppercase">Indicateurs</div>
                    <div className="mt-2 inline-block rounded-full bg-[color:var(--primary)]/10 px-3 py-1 text-sm font-semibold text-[color:var(--primary)]">
                      {detailedOdd.indicators} au total
                    </div>
                  </div>

                  <div className="pt-4 border-t border-[color:var(--border)]">
                    <div className="text-xs font-medium text-[color:var(--muted)] uppercase">Description</div>
                    <p className="mt-2 text-sm leading-relaxed text-[color:var(--foreground)]">{detailedOdd.description}</p>
                  </div>
                </div>
              </Card>
            </div>
          ) : (
            <Card className="text-center py-8">
              <p className="text-sm text-[color:var(--muted)]">Sélectionnez un ODD pour voir les détails</p>
            </Card>
          )}
        </div>
      </div>

      {/* Palette ODD */}
      <div className="space-y-4">
        <SectionTitle title="Palette Couleurs ODD" description="Les 17 couleurs officielles de l'Agenda 2030" />
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 lg:grid-cols-9">
          {ODDS.map((odd) => (
            <div
              key={odd.code}
              className="rounded-lg border border-[color:var(--border)] overflow-hidden shadow-sm hover:shadow-md transition cursor-pointer"
              onClick={() => setSelectedOdd(odd.code)}
            >
              <div className="h-12" style={{ backgroundColor: odd.color }} />
              <div className="p-2 text-center">
                <div className="text-xs font-semibold text-[color:var(--foreground)]">ODD {odd.code}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
