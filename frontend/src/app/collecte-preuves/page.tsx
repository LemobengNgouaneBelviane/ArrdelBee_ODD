"use client";

import { useState } from "react";
import { apiGet, apiPost } from "@/lib/api";
import { PageHeader, Alert, Card, Select } from "@/components/ui";

type Evidence = {
  id: number;
  project_id: number;
  alignment_id: number | null;
  required_list: string | null;
  provided_list: string | null;
  workflow_level: "SAISIE" | "VERIFICATION" | "VALIDATION_CTD" | "CERTIFICATION_ARRDEL";
  updated_at: string;
  updated_by: string | null;
};

const WORKFLOW_LEVELS = [
  { value: "SAISIE", label: "Saisie Agent Terrain", color: "blue" },
  { value: "VERIFICATION", label: "Vérification QC", color: "yellow" },
  { value: "VALIDATION_CTD", label: "Validation CTD", color: "green" },
  { value: "CERTIFICATION_ARRDEL", label: "Certification ARRDEL", color: "purple" },
];

export default function Page() {
  const [projectId, setProjectId] = useState<number | "">("");
  const [evidence, setEvidence] = useState<Evidence | null>(null);
  const [provided, setProvided] = useState("");
  const [level, setLevel] = useState<Evidence["workflow_level"]>("SAISIE");
  const [updatedBy, setUpdatedBy] = useState("Agent Terrain");
  const [msg, setMsg] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  async function loadEvidence() {
    setMsg(null);
    setErr(null);
    setEvidence(null);
    if (!projectId) {
      setErr("Veuillez saisir un identifiant de projet.");
      return;
    }
    setLoading(true);
    try {
      const ev = await apiPost<Evidence>(`/projets/${projectId}/preuves`, {});
      setEvidence(ev);
      setProvided(ev.provided_list ?? "");
      setLevel(ev.workflow_level);
      setMsg(`✓ Preuve chargée pour le projet ${projectId}`);
    } catch (e) {
      setErr(String(e));
    } finally {
      setLoading(false);
    }
  }

  async function saveEvidence() {
    setMsg(null);
    setErr(null);
    if (!evidence) return;
    setSaving(true);
    try {
      const ev = await apiPost<Evidence>(`/preuves/${evidence.id}`, {
        provided_list: provided || null,
        workflow_level: level,
        updated_by: updatedBy || null,
      });
      setEvidence(ev);
      setProvided(ev.provided_list ?? "");
      setLevel(ev.workflow_level);
      setMsg("Preuve mise à jour avec succès!");
    } catch (e) {
      setErr(String(e));
    } finally {
      setSaving(false);
    }
  }

  const levelConfig = WORKFLOW_LEVELS.find((l) => l.value === level);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-indigo-50 py-8">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <PageHeader
          title="Collecte des Preuves"
          subtitle="Gérez les pièces justificatives et le workflow de validation"
        />

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

        {/* Chargement de preuve */}
        <Card title="Étape 1 : Charger une Preuve" description="Sélectionnez un projet pour gérer ses preuves">
          <div className="space-y-4">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="sm:col-span-2">
                <label className="block text-sm font-semibold text-gray-900 mb-2">Identifiant du Projet</label>
                <input
                  type="number"
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                  value={projectId}
                  onChange={(e) => setProjectId(e.target.value ? Number(e.target.value) : "")}
                  placeholder="Ex: 1, 42, 128..."
                />
              </div>
              <div className="flex items-end">
                <button
                  onClick={loadEvidence}
                  disabled={loading || !projectId}
                  className={`w-full py-3 rounded-lg font-semibold transition-all ${
                    loading || !projectId
                      ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                      : "bg-gradient-to-r from-blue-500 to-indigo-600 text-white hover:shadow-lg"
                  }`}
                >
                  {loading ? "⏳ Chargement..." : "📂 Charger"}
                </button>
              </div>
            </div>
          </div>
        </Card>

        {/* Formulaire de gestion des preuves */}
        {evidence && (
          <div className="mt-8 space-y-6">
            {/* Pièces requises */}
            <Card title="Pièces Requises" description="Documents obligatoires pour ce projet">
              <div className="rounded-lg bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-300 p-4">
                {evidence.required_list ? (
                  <div className="text-sm text-gray-700 whitespace-pre-wrap">{evidence.required_list}</div>
                ) : (
                  <p className="text-sm text-gray-600 italic">Aucune pièce requise définie pour ce projet</p>
                )}
              </div>
            </Card>

            {/* Workflow de validation */}
            <Card title="Workflow de Validation" description="Progression du processus de validation">
              <div className="space-y-4">
                <div className="flex gap-2 overflow-x-auto">
                  {WORKFLOW_LEVELS.map((wlevel) => (
                    <button
                      key={wlevel.value}
                      onClick={() => setLevel(wlevel.value as any)}
                      className={`py-2 px-3 rounded-lg text-xs font-semibold transition-all whitespace-nowrap ${
                        level === wlevel.value
                          ? wlevel.color === "blue"
                            ? "bg-blue-500 text-white shadow-lg"
                            : wlevel.color === "yellow"
                            ? "bg-yellow-500 text-white shadow-lg"
                            : wlevel.color === "green"
                            ? "bg-green-500 text-white shadow-lg"
                            : "bg-purple-500 text-white shadow-lg"
                          : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                      }`}
                    >
                      {wlevel.label}
                    </button>
                  ))}
                </div>

                {/* Progress bar */}
                <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-500 via-yellow-500 via-green-500 to-purple-500 transition-all"
                    style={{
                      width: `${((WORKFLOW_LEVELS.findIndex((l) => l.value === level) + 1) / WORKFLOW_LEVELS.length) * 100}%`,
                    }}
                  />
                </div>
              </div>
            </Card>

            {/* Pièces fournies */}
            <Card title="Pièces Fournies" description="Téléchargement ou copie des documents justificatifs">
              <div className="space-y-3">
                <div className="relative">
                  <textarea
                    placeholder="Collez ici:"
                    value={provided}
                    onChange={(e) => setProvided(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 min-h-32 resize-none"
                  />
                  <div className="mt-2 text-xs text-gray-500">
                    {provided.length} caractères • Accepte liens, références, ou contenu copié
                  </div>
                </div>

                {/* Uploads suggérés */}
                <div className="rounded-lg border-2 border-dashed border-gray-300 p-4 text-center">
                  <p className="text-sm text-gray-600">📎 Vous pouvez aussi</p>
                  <div className="flex gap-2 justify-center mt-2 flex-wrap">
                    <button className="px-3 py-1 bg-gray-100 text-gray-700 rounded text-xs hover:bg-gray-200">
                      📷 Capture d'écran
                    </button>
                    <button className="px-3 py-1 bg-gray-100 text-gray-700 rounded text-xs hover:bg-gray-200">
                      📄 Télécharger fichier
                    </button>
                    <button className="px-3 py-1 bg-gray-100 text-gray-700 rounded text-xs hover:bg-gray-200">
                      🔗 Lien URL
                    </button>
                  </div>
                </div>
              </div>
            </Card>

            {/* Informations complémentaires */}
            <Card title="Informations de Mise à Jour" description="Métadonnées de validation">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">Responsable</label>
                  <input
                    type="text"
                    value={updatedBy}
                    onChange={(e) => setUpdatedBy(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    placeholder="Nom ou rôle"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">Dernière mise à jour</label>
                  <input
                    type="text"
                    disabled
                    value={new Date(evidence.updated_at).toLocaleString("fr-FR")}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg bg-gray-50 text-gray-600"
                  />
                </div>
              </div>
            </Card>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={() => {
                  setEvidence(null);
                  setProvided("");
                  setProjectId("");
                  setLevel("SAISIE");
                }}
                className="flex-1 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-all"
              >
                ↺ Nouvelle Preuve
              </button>
              <button
                onClick={saveEvidence}
                disabled={saving}
                className={`flex-1 py-3 rounded-lg font-semibold transition-all ${
                  saving
                    ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                    : "bg-gradient-to-r from-green-500 to-emerald-600 text-white hover:shadow-lg"
                }`}
              >
                {saving ? "⏳ Sauvegarde..." : "💾 Enregistrer la Preuve"}
              </button>
            </div>

            {/* Résumé */}
            <div className="rounded-lg bg-gradient-to-r from-indigo-50 to-blue-50 border-2 border-indigo-300 p-5">
              <h4 className="font-bold text-indigo-900 mb-3">📊 Résumé du Dossier</h4>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-indigo-600 font-semibold">Projet ID</p>
                  <p className="text-indigo-900">{evidence.project_id}</p>
                </div>
                <div>
                  <p className="text-indigo-600 font-semibold">Étape Actuelle</p>
                  <p className="text-indigo-900">{levelConfig?.label}</p>
                </div>
                <div>
                  <p className="text-indigo-600 font-semibold">État</p>
                  <p className="text-indigo-900">{provided.length > 0 ? "Complet" : "Incomplet"}</p>
                </div>
                <div>
                  <p className="text-indigo-600 font-semibold">Progression</p>
                  <p className="text-indigo-900">
                    {Math.round(
                      ((WORKFLOW_LEVELS.findIndex((l) => l.value === level) + 1) / WORKFLOW_LEVELS.length) * 100
                    )}%
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {!evidence && !loading && projectId && (
          <div className="mt-8 text-center py-12">
            <p className="text-gray-500">Cliquez sur "Charger" pour commencer</p>
          </div>
        )}
      </div>
    </div>
  );
}
