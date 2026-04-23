"use client";

import { useEffect, useMemo, useState } from "react";
import {
  apiGet,
  apiPost,
  ODD_METADATA,
  calculateKPI,
} from "@/lib/api";
import { Alert, Card, PageHeader, Select, Textarea } from "@/components/ui";

type UnalignedProject = {
  id: number;
  title: string;
  chapitre: string | null;
  suggested_sdg_codes: string[];
  commune?: string;
  department?: string;
};

const SECTOR_TO_ODD: Record<string, number[]> = {
  "MINSANTE": [3], "SANTE": [3],
  "MINEDUB": [4], "MINESEC": [4], "EDUCATION": [4],
  "MINEE": [6, 7], "EAU": [6], "ASSAINISSEMENT": [6],
  "MINADER": [2], "AGRICULTURE": [2, 15], "ELEVAGE": [2],
  "MINEPDED": [13, 15], "ENVIRONNEMENT": [13, 15],
  "MINTP": [9, 11], "INFRASTRUCTURE": [9, 11], "URBANISME": [11],
  "MINAT": [16], "GOUVERNANCE": [16],
  "MINCOMMERCE": [8], "ECONOMIE": [8], "EMPLOI": [8], "TRAVAIL": [8],
  "MINEE_ENERGIE": [7], "ENERGIE": [7],
};

export default function Page() {
  const [projects, setProjects] = useState<UnalignedProject[]>([]);
  const [projectId, setProjectId] = useState<number | "">("");
  const [selectedODDs, setSelectedODDs] = useState<number[]>([]);
  const [validatedBy, setValidatedBy] = useState("CTD");
  const [justification, setJustification] = useState("");
  const [baseline, setBaseline] = useState("");
  const [target, setTarget] = useState("");
  const [msg, setMsg] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [kpiResult, setKpiResult] = useState<any>(null);
  const [step, setStep] = useState<1 | 2 | 3 | 4>(1);

  useEffect(() => {
    setLoading(true);
    apiGet<UnalignedProject[]>("/projets/non-alignes?limit=500")
      .then(setProjects)
      .catch(() => {
        apiGet<UnalignedProject[]>("/projets?limit=500").then(setProjects);
      })
      .finally(() => setLoading(false));
  }, []);

  const selectedProject = useMemo(() => projects.find((p) => p.id === projectId), [projects, projectId]);

  const suggestedODDs = useMemo(() => {
    if (!selectedProject?.chapitre) return [];
    const sector = (selectedProject.chapitre || "").toUpperCase();
    return SECTOR_TO_ODD[sector] || [];
  }, [selectedProject]);

  const handleCalculateKPI = () => {
    if (!baseline || !target) {
      setErr("Veuillez entrer la baseline et la cible.");
      return;
    }
    try {
      const result = calculateKPI(parseFloat(baseline), parseFloat(target));
      setKpiResult(result);
      setErr(null);
    } catch (e) {
      setErr("Erreur calcul KPI");
    }
  };

  const handleToggleODD = (oddNum: number) => {
    setSelectedODDs((prev) =>
      prev.includes(oddNum) ? prev.filter((o) => o !== oddNum) : [...prev, oddNum]
    );
  };

  async function submit() {
    setMsg(null);
    setErr(null);
    if (!projectId || selectedODDs.length === 0) {
      setErr("Sélectionnez un projet et au moins un ODD.");
      return;
    }
    setSubmitting(true);
    try {
      await apiPost("/alignements/valider", {
        project_id: projectId,
        selected_odds: selectedODDs,
        validated_by: validatedBy,
        justification: justification || null,
        baseline: baseline ? parseFloat(baseline) : null,
        target: target ? parseFloat(target) : null,
        status: "VALIDATED",
      });
      setMsg("Alignement enregistré avec succès!");
      setTimeout(() => {
        setProjectId("");
        setSelectedODDs([]);
        setJustification("");
        setBaseline("");
        setTarget("");
        setKpiResult(null);
        setStep(1);
      }, 2000);
    } catch (e) {
      setErr(String(e));
    } finally {
      setSubmitting(false);
    }
  }

  const stepConfig = [
    { num: 1, icon: "", label: "Projet" },
    { num: 2, icon: "", label: "ODD" },
    { num: 3, icon: "", label: "KPI" },
    { num: 4, icon: "", label: "Validation" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 py-12">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <PageHeader
          title="Alignement aux Objectifs de Développement Durable"
          subtitle="Processus guidé pour aligner vos projets aux ODD"
        />

        {/* Messages */}
        {msg && (
          <div className="mb-6 rounded-lg border-l-4 border-emerald-500 bg-emerald-50 p-4">
            <p className="text-sm font-medium text-emerald-800">{msg}</p>
          </div>
        )}
        {err && (
          <div className="mb-6 rounded-lg border-l-4 border-red-500 bg-red-50 p-4">
            <p className="text-sm font-medium text-red-800">{err}</p>
          </div>
        )}

        {/* Progress Steps */}
        <div className="mb-8 mt-8">
          <div className="flex justify-between mb-4">
            {stepConfig.map((s) => (
              <button
                key={s.num}
                onClick={() => s.num <= step && setStep(s.num as any)}
                className="flex flex-col items-center flex-1 group cursor-pointer"
              >
                <div
                  className={`flex h-14 w-14 items-center justify-center rounded-full font-bold text-lg transition-all transform ${
                    step >= s.num
                      ? "bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-lg scale-105"
                      : "bg-gray-200 text-gray-600 group-hover:bg-gray-300"
                  }`}
                >
                  {step > s.num ? "✓" : s.icon}
                </div>
                <div className="mt-2 text-xs font-semibold text-gray-700 group-hover:text-gray-900">{s.label}</div>
              </button>
            ))}
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-500"
              style={{ width: `${((step - 1) / 3) * 100}%` }}
            />
          </div>
        </div>

        {/* STEP 1: Project Selection */}
        {step >= 1 && (
          <Card title="Étape 1 : Sélection du Projet" description="Choisissez le projet à aligner">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">Projet</label>
                <Select
                  value={projectId}
                  onChange={(e) => {
                    setProjectId(e.target.value ? Number(e.target.value) : "");
                    setSelectedODDs([]);
                    setJustification("");
                    setBaseline("");
                    setTarget("");
                    setKpiResult(null);
                  }}
                >
                  <option value="">— Sélectionner un projet —</option>
                  {loading ? (
                    <option disabled>Chargement...</option>
                  ) : projects.length === 0 ? (
                    <option disabled>Aucun projet trouvé</option>
                  ) : (
                    projects.map((p) => (
                      <option key={p.id} value={p.id}>
                        #{p.id} • {p.title.substring(0, 60)}
                      </option>
                    ))
                  )}
                </Select>
              </div>

              {selectedProject && (
                <div className="rounded-lg border-2 border-emerald-300 bg-emerald-50/80 p-4 space-y-3">
                  <div>
                    <p className="text-xs font-bold text-emerald-600 uppercase tracking-wide">Projet</p>
                    <p className="text-base font-semibold text-emerald-900 mt-1">{selectedProject.title}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <p className="text-xs font-bold text-emerald-600 uppercase tracking-wide">Secteur</p>
                      <p className="text-sm text-emerald-800 mt-1">{selectedProject.chapitre || "—"}</p>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-emerald-600 uppercase tracking-wide">Localité</p>
                      <p className="text-sm text-emerald-800 mt-1">{selectedProject.commune || "—"}</p>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => selectedProject && setStep(2)}
                  disabled={!selectedProject}
                  className={`w-full py-3 rounded-lg font-semibold transition-all ${
                    selectedProject
                      ? "bg-gradient-to-r from-blue-500 to-indigo-600 text-white hover:shadow-lg"
                      : "bg-gray-200 text-gray-400 cursor-not-allowed"
                  }`}
                >
                  Continuer → ODD
                </button>
              </div>
            </div>
          </Card>
        )}

        {/* STEP 2: ODD Selection */}
        {step >= 2 && selectedProject && (
          <Card title="Étape 2 : Sélection des Objectifs" description="Choisissez les ODD pertinents">
            <div className="space-y-5">
              {suggestedODDs.length > 0 && (
                <div className="rounded-lg bg-blue-50/80 border-2 border-blue-300 p-4">
                  <p className="text-xs font-bold text-blue-600 uppercase tracking-wide mb-3">💡 Suggestions automatiques</p>
                  <div className="flex flex-wrap gap-2">
                    {suggestedODDs.map((odd) => (
                      <button
                        key={odd}
                        onClick={() => handleToggleODD(odd)}
                        className={`px-4 py-2 rounded-full text-sm font-semibold transition-all ${
                          selectedODDs.includes(odd)
                            ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md"
                            : "bg-white text-blue-700 border border-blue-300 hover:bg-blue-100"
                        }`}
                      >
                        ODD {odd}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <div>
                <p className="text-xs font-bold text-gray-600 mb-3 uppercase tracking-wide">Tous les objectifs</p>
                <div className="grid grid-cols-3 gap-3 sm:grid-cols-4 md:grid-cols-6">
                  {Array.from({ length: 17 }, (_, i) => i + 1).map((oddNum) => (
                    <button
                      key={oddNum}
                      onClick={() => handleToggleODD(oddNum)}
                      className={`p-3 rounded-lg border-2 transition-all transform hover:scale-105 ${
                        selectedODDs.includes(oddNum)
                          ? "border-blue-600 bg-gradient-to-br from-blue-50 to-indigo-50 shadow-md"
                          : "border-gray-200 bg-white hover:border-blue-300 hover:shadow-sm"
                      }`}
                    >
                      <div className="text-lg font-bold text-gray-900">{oddNum}</div>
                      <div className="text-xs text-gray-500 leading-tight mt-1">
                        {ODD_METADATA[oddNum]?.fr.split(" ")[0] || "ODD"}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => setStep(1)}
                  className="flex-1 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50"
                >
                  ← Retour
                </button>
                <button
                  onClick={() => setStep(3)}
                  disabled={selectedODDs.length === 0}
                  className={`flex-1 py-3 rounded-lg font-semibold transition-all ${
                    selectedODDs.length > 0
                      ? "bg-gradient-to-r from-blue-500 to-indigo-600 text-white hover:shadow-lg"
                      : "bg-gray-200 text-gray-400 cursor-not-allowed"
                  }`}
                >
                  Continuer → KPI
                </button>
              </div>
            </div>
          </Card>
        )}

        {/* STEP 3: KPI Calculation */}
        {step >= 3 && selectedProject && (
          <Card title="Étape 3 : Indicateurs de Performance" description="Entrez les valeurs de base et cible">
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">Baseline (État actuel)</label>
                  <input
                    type="number"
                    placeholder="ex: 45"
                    value={baseline}
                    onChange={(e) => setBaseline(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                  />
                  <p className="text-xs text-gray-500 mt-2">Situation actuelle / valeur de départ</p>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">Target (Objectif)</label>
                  <input
                    type="number"
                    placeholder="ex: 80"
                    value={target}
                    onChange={(e) => setTarget(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                  />
                  <p className="text-xs text-gray-500 mt-2">Objectif à atteindre</p>
                </div>
              </div>

              <button
                onClick={handleCalculateKPI}
                className="w-full py-3 bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
              >
                🔄 Calculer l'indicateur
              </button>

              {kpiResult && (
                <div
                  className={`p-4 rounded-lg border-l-4 space-y-3 ${
                    kpiResult.status === "red"
                      ? "bg-red-50 border-red-500"
                      : kpiResult.status === "yellow"
                      ? "bg-yellow-50 border-yellow-500"
                      : "bg-green-50 border-green-500"
                  }`}
                >
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <p className="text-xs font-bold text-gray-600 mb-1">RÉALISATION</p>
                      <p className="text-3xl font-bold text-gray-900">{kpiResult.percentage.toFixed(1)}%</p>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-gray-600 mb-1">ÉCART</p>
                      <p
                        className={`text-3xl font-bold ${
                          kpiResult.status === "red"
                            ? "text-red-600"
                            : kpiResult.status === "yellow"
                            ? "text-yellow-600"
                            : "text-green-600"
                        }`}
                      >
                        {kpiResult.variancePercent > 0 ? "+" : ""}{kpiResult.variancePercent.toFixed(1)}%
                      </p>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-gray-600 mb-1">STATUT</p>
                      <div
                        className={`inline-block px-3 py-1 rounded-full text-sm font-bold ${
                          kpiResult.status === "red"
                            ? "bg-red-200 text-red-800"
                            : kpiResult.status === "yellow"
                            ? "bg-yellow-200 text-yellow-800"
                            : "bg-green-200 text-green-800"
                        }`}
                      >
                        {kpiResult.status === "red" ? "CRITIQUE" : kpiResult.status === "yellow" ? "ALERTE" : "BON"}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => setStep(2)}
                  className="flex-1 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50"
                >
                  ← Retour
                </button>
                <button
                  onClick={() => setStep(4)}
                  className="flex-1 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
                >
                  Continuer → Validation
                </button>
              </div>
            </div>
          </Card>
        )}

        {/* STEP 4: Final Validation */}
        {step >= 4 && selectedProject && (
          <Card title="Étape 4 : Validation Finale" description="Finalisez l'alignement">
            <div className="space-y-5">
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">Justification</label>
                <Textarea
                  placeholder="Expliquez comment ce projet contribue aux ODD sélectionnés..."
                  value={justification}
                  onChange={(e) => setJustification(e.target.value)}
                  rows={4}
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">Validé par</label>
                  <Select value={validatedBy} onChange={(e) => setValidatedBy(e.target.value)}>
                    <option value="CTD">CTD (Collectivité)</option>
                    <option value="ADMIN">Administration Locale</option>
                    <option value="DREF">DREF</option>
                    <option value="FIELD">Responsable Terrain</option>
                  </Select>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">ODD Sélectionnés</label>
                  <div className="flex flex-wrap gap-2 p-3 bg-blue-50 rounded-lg border border-blue-200">
                    {selectedODDs.length === 0 ? (
                      <span className="text-sm text-gray-500">Aucun ODD sélectionné</span>
                    ) : (
                      selectedODDs.map((odd) => (
                        <span key={odd} className="inline-block bg-blue-200 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                          ODD {odd}
                        </span>
                      ))
                    )}
                  </div>
                </div>
              </div>

              <div className="rounded-lg bg-gradient-to-br from-indigo-50 to-blue-50 border-2 border-indigo-200 p-5">
                <h4 className="font-bold text-indigo-900 mb-3">📋 Résumé de l'alignement</h4>
                <ul className="space-y-2 text-sm text-indigo-800">
                  <li className="flex items-start">
                    <span className="mr-2 text-lg">✓</span>
                    <div>
                      <p className="font-semibold">Projet</p>
                      <p className="text-indigo-700">{selectedProject.title.substring(0, 70)}</p>
                    </div>
                  </li>
                  <li className="flex items-start">
                    <span className="mr-2 text-lg">✓</span>
                    <div>
                      <p className="font-semibold">ODD alignés</p>
                      <p className="text-indigo-700">{selectedODDs.join(", ")}</p>
                    </div>
                  </li>
                  {kpiResult && (
                    <li className="flex items-start">
                      <span className="mr-2 text-lg">✓</span>
                      <div>
                        <p className="font-semibold">Performance</p>
                        <p className="text-indigo-700">{kpiResult.percentage.toFixed(1)}% (écart: {kpiResult.variancePercent.toFixed(1)}%)</p>
                      </div>
                    </li>
                  )}
                </ul>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setStep(3)}
                  className="flex-1 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50"
                >
                  ← Retour
                </button>
                <button
                  onClick={submit}
                  disabled={submitting}
                  className="flex-1 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {submitting ? "Enregistrement..." : "Valider l'alignement"}
                </button>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
