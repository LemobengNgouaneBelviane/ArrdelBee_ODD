"use client";

import dynamic from "next/dynamic";
import { useEffect, useMemo, useState } from "react";
import { apiGet } from "@/lib/api";
import { PageHeader, Alert, Card } from "@/components/ui";

const DynamicMapView = dynamic(
  () => import("@/components/MapView").then((mod) => ({ default: mod.MapView })),
  { ssr: false, loading: () => <div className="h-96 bg-gray-200 rounded-lg flex items-center justify-center">Carte en cours de chargement...</div> }
);

type Department = { id: number; name: string };
type Commune = { id: number; name: string; department_id: number; department_name?: string | null };
type Project = {
  id: number;
  title: string;
  chapitre: string | null;
  commune_id: number | null;
  commune: string | null;
  department: string | null;
};

export default function Page() {
  const [deps, setDeps] = useState<Department[]>([]);
  const [communes, setCommunes] = useState<Commune[]>([]);
  const [selectedDep, setSelectedDep] = useState<number | "">("");
  const [selectedCommune, setSelectedCommune] = useState<number | "">("");
  const [communeQuery, setCommuneQuery] = useState("");
  const [projects, setProjects] = useState<Project[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    Promise.all([
      apiGet<Department[]>("/territoire/departements"),
      apiGet<Commune[]>("/territoire/communes"),
    ])
      .then(([deps, comms]) => {
        setDeps(deps);
        setCommunes(comms);
      })
      .catch((e) => setErr(String(e)));
  }, []);

  const filteredCommunes = useMemo(() => {
    if (!selectedDep) return communes;
    return communes.filter((c) => c.department_id === selectedDep);
  }, [communes, selectedDep]);

  const visibleCommunes = useMemo(() => {
    const q = communeQuery.trim().toLowerCase();
    const base = q ? filteredCommunes.filter((c) => c.name.toLowerCase().includes(q)) : filteredCommunes;
    return base.slice(0, 500);
  }, [filteredCommunes, communeQuery]);

  useEffect(() => {
    setProjects([]);
    setErr(null);
    if (!selectedCommune) return;
    setLoading(true);
    apiGet<Project[]>(`/projets?commune_id=${selectedCommune}&limit=500`)
      .then(setProjects)
      .catch((e) => setErr(String(e)))
      .finally(() => setLoading(false));
  }, [selectedCommune]);

  const sectorStats = useMemo(() => {
    const stats: Record<string, number> = {};
    projects.forEach((p) => {
      const sector = p.chapitre || "Autre";
      stats[sector] = (stats[sector] || 0) + 1;
    });
    return Object.entries(stats).sort((a, b) => b[1] - a[1]);
  }, [projects]);

  const selectedCommuneName = useMemo(() => {
    return communes.find((c) => c.id === selectedCommune)?.name || "";
  }, [communes, selectedCommune]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-blue-50 py-8">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <PageHeader
          title="Cartographie Territoriale"
          subtitle="Visualisez la distribution géographique des projets alignés aux ODD"
        />

        {err && <Alert tone="danger" title="Erreur">{err}</Alert>}

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-4 mt-8">
          {/* Filtres */}
          <div className="lg:col-span-1">
            <Card title="Filtres" description="Navigation territoriale">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">Région</label>
                  <select
                    className="w-full rounded-lg border-2 border-gray-300 px-3 py-2 text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                    value={selectedDep}
                    onChange={(e) => {
                      setSelectedDep(e.target.value ? Number(e.target.value) : "");
                      setSelectedCommune("");
                      setCommuneQuery("");
                    }}
                  >
                    <option value="">— Sélectionner —</option>
                    {deps.map((d) => (
                      <option key={d.id} value={d.id}>
                        {d.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">Commune</label>
                  {selectedDep ? (
                    <>
                      <input
                        type="text"
                        placeholder="Chercher..."
                        className="mb-2 w-full rounded-lg border-2 border-gray-300 px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                        value={communeQuery}
                        onChange={(e) => setCommuneQuery(e.target.value)}
                      />
                      <select
                        className="w-full rounded-lg border-2 border-gray-300 px-3 py-2 text-sm max-h-48 focus:outline-none focus:border-blue-500"
                        value={selectedCommune}
                        onChange={(e) => setSelectedCommune(e.target.value ? Number(e.target.value) : "")}
                      >
                        <option value="">— Sélectionner —</option>
                        {visibleCommunes.map((c) => (
                          <option key={c.id} value={c.id}>
                            {c.name}
                          </option>
                        ))}
                      </select>
                    </>
                  ) : (
                    <p className="text-sm text-gray-500 py-2 px-3">Sélectionnez d'abord une région</p>
                  )}
                </div>

                {selectedCommune && (
                  <div className="rounded-lg border-2 border-blue-300 bg-blue-50 p-3">
                    <p className="text-xs font-bold text-blue-600 uppercase">Commune active</p>
                    <p className="mt-2 font-semibold text-blue-900">{selectedCommuneName}</p>
                  </div>
                )}

                {selectedCommune && sectorStats.length > 0 && (
                  <div className="rounded-lg border-2 border-purple-200 bg-purple-50 p-3">
                    <p className="text-xs font-bold text-purple-600 uppercase mb-3">Secteurs</p>
                    <div className="space-y-2">
                      {sectorStats.slice(0, 5).map(([sector, count]) => (
                        <div key={sector} className="flex justify-between items-center text-sm">
                          <span className="text-gray-700">{sector || "Autre"}</span>
                          <span className="inline-block bg-purple-200 text-purple-800 px-2 py-1 rounded-full font-bold text-xs">
                            {count}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </Card>
          </div>

          {/* Carte et projets */}
          <div className="lg:col-span-3 space-y-6">
            {/* Carte */}
            <Card title="Carte Géographique" description="Vue cartographique de la zone">
              <div className="rounded-lg overflow-hidden border-2 border-gray-300">
                {selectedCommune ? (
                  <DynamicMapView communes={communes} selectedCommuneId={selectedCommune as number} />
                ) : (
                  <div className="h-96 bg-gray-100 rounded flex items-center justify-center text-gray-500">
                    Sélectionnez une commune pour afficher la carte
                  </div>
                )}
              </div>
            </Card>

            {/* Statistiques */}
            {selectedCommune && (
              <Card title="Statistiques de la Commune" description={selectedCommuneName}>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  <div className="rounded-lg bg-blue-50 border border-blue-300 p-4 text-center">
                    <div className="text-3xl font-bold text-blue-600">{projects.length}</div>
                    <p className="text-xs font-semibold text-blue-800 mt-2 uppercase">Projets</p>
                  </div>
                  <div className="rounded-lg bg-purple-50 border border-purple-300 p-4 text-center">
                    <div className="text-3xl font-bold text-purple-600">{sectorStats.length}</div>
                    <p className="text-xs font-semibold text-purple-800 mt-2 uppercase">Secteurs</p>
                  </div>
                  <div className="rounded-lg bg-emerald-50 border border-emerald-300 p-4 text-center">
                    <div className="text-3xl font-bold text-emerald-600">
                      {Math.round((projects.filter((p) => p.chapitre).length / Math.max(projects.length, 1)) * 100)}%
                    </div>
                    <p className="text-xs font-semibold text-emerald-800 mt-2 uppercase">Catégorisés</p>
                  </div>
                  <div className="rounded-lg bg-amber-50 border border-amber-300 p-4 text-center">
                    <div className="text-3xl font-bold text-amber-600">0</div>
                    <p className="text-xs font-semibold text-amber-800 mt-2 uppercase">Alignés</p>
                  </div>
                </div>
              </Card>
            )}

            {/* Projets */}
            {selectedCommune && (
              <Card 
                title="Projets de la Commune" 
                description={`${projects.length} projet${projects.length !== 1 ? 's' : ''} trouvé${projects.length !== 1 ? 's' : ''}`}
              >
                {loading ? (
                  <p className="text-center py-8 text-gray-600">⏳ Chargement des projets...</p>
                ) : projects.length === 0 ? (
                  <p className="text-center py-8 text-gray-600">Aucun projet dans cette commune</p>
                ) : (
                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {projects.map((p) => (
                      <div key={p.id} className="p-3 rounded-lg border border-gray-200 hover:border-blue-400 hover:bg-blue-50 transition-all">
                        <div className="flex justifybetween gap-2">
                          <div className="flex-1">
                            <p className="font-semibold text-gray-900 text-sm">{p.title.substring(0, 60)}</p>
                            <p className="text-xs text-gray-600 mt-1">
                              {p.chapitre && <span className="inline-block bg-gray-200 px-2 py-0.5 rounded mr-2">{p.chapitre}</span>}
                              <span className="text-gray-500">ID: {p.id}</span>
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
