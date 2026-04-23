'use client';

import { Card, PageHeader, SectionTitle, Badge, Stat } from "@/components/ui";

interface ValidationItem {
  id: string;
  type: "rapport" | "alignement" | "indicateur";
  title: string;
  submitter: string;
  date: string;
  severity: "critique" | "normal" | "info";
  issues: string[];
}

const validationItems: ValidationItem[] = [
  {
    id: "1",
    type: "rapport",
    title: "Rapport Trimestriel Q1 - Santé & Bien-être",
    submitter: "Ebolo Awa",
    date: "2024-06-15",
    severity: "critique",
    issues: [
      "Données manquantes : Santé - 3 communes sans L.I.",
      "Incohérence : Pas de pauvreté - Budget dépassé de 15%",
    ],
  },
  {
    id: "2",
    type: "alignement",
    title: "Alignement ODD - Projet Réseau Électrique",
    submitter: "Jean Ebolowa",
    date: "2024-06-14",
    severity: "normal",
    issues: [
      "ODD 07 & 13 alignés mais preuve documentation insuffisante",
    ],
  },
  {
    id: "3",
    type: "indicateur",
    title: "Saisie Indicateurs - Eau & Assainissement (ODD 6)",
    submitter: "Marie Atangana",
    date: "2024-06-10",
    severity: "normal",
    issues: ["Voleur d'eau potable distribuée - Valeur outlier"],
  },
];

const severityColors = {
  critique: "bg-red-50 border-red-200 text-red-700",
  normal: "bg-amber-50 border-amber-200 text-amber-700",
  info: "bg-blue-50 border-blue-200 text-blue-700",
};

const severityLabels = {
  critique: "🚨 Critique",
  normal: "⚠️ Normal",
  info: "ℹ️ Info",
};

export default function ValidationPage() {
  const criticalCount = validationItems.filter(
    (item) => item.severity === "critique"
  ).length;

  return (
    <div className="space-y-10">
      <PageHeader
        title="Validation & Qualité des Données"
        subtitle="Vérification des rapports et alignements ODD avant archivage"
      />

      {/* Statistiques */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="En Validation" value={validationItems.length.toString()} color="default" icon="⏳" />
        <Stat label="Alertes Critiques" value={criticalCount.toString()} color="danger" icon="🚨" />
        <Stat label="Validés ce Mois" value="12" color="success" icon="✓" />
        <Stat label="Taux de Conformité" value="87%" color="primary" icon="📊" />
      </div>

      {/* Alertes Critiques */}
      {criticalCount > 0 && (
        <div className="rounded-lg border-l-4 border-red-500 bg-red-50 p-4">
          <h3 className="font-semibold text-red-900">⚠️ Alertes Critiques</h3>
          <p className="mt-1 text-sm text-red-700">
            {criticalCount} élément(s) require votre attention immédiate avant validation
          </p>
        </div>
      )}

      {/* Onglets */}
      <div className="flex flex-wrap gap-3 border-b border-[color:var(--border)] pb-4">
        <button className="px-4 py-2 text-sm font-semibold text-[color:var(--primary)] border-b-2 border-[color:var(--primary)]">
          Tous ({validationItems.length})
        </button>
        <button className="px-4 py-2 text-sm font-semibold text-[color:var(--muted)] hover:text-[color:var(--foreground)]">
          Rapports
        </button>
        <button className="px-4 py-2 text-sm font-semibold text-[color:var(--muted)] hover:text-[color:var(--foreground)]">
          Alignements
        </button>
        <button className="px-4 py-2 text-sm font-semibold text-[color:var(--muted)] hover:text-[color:var(--foreground)]">
          Indicateurs
        </button>
      </div>

      {/* Liste des Éléments à Valider */}
      <div className="space-y-3">
        <SectionTitle 
          title="Éléments en Validation"
          description="Examen et approbation des données soumises"
        />
        <div className="space-y-4">
          {validationItems.map((item) => (
            <Card key={item.id} className="p-5">
              <div className="space-y-4">
                <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                  <div className="flex-1">
                    <div className="flex flex-wrap items-center gap-3">
                      <h3 className="text-base font-semibold text-[color:var(--foreground)]">
                        {item.title}
                      </h3>
                      <span
                        className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${severityColors[item.severity]}`}
                      >
                        {severityLabels[item.severity]}
                      </span>
                    </div>
                    <div className="mt-2 text-xs text-[color:var(--muted)]">
                      Soumis par {item.submitter} • {new Date(item.date).toLocaleDateString("fr-FR")}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button className="rounded-lg border border-red-300 bg-red-50 px-3 py-2 text-sm font-semibold text-red-700 hover:bg-red-100 transition">
                      ✓ Rejeter
                    </button>
                    <button className="rounded-lg bg-emerald-500 px-3 py-2 text-sm font-semibold text-white hover:bg-emerald-600 transition">
                      ✓ Approuver
                    </button>
                  </div>
                </div>

                {/* Issues */}
                {item.issues.length > 0 && (
                  <div className="space-y-2 border-t border-[color:var(--border)] pt-4">
                    <div className="text-xs font-semibold uppercase text-[color:var(--muted)]">
                      Problèmes Détectés
                    </div>
                    {item.issues.map((issue, idx) => (
                      <div
                        key={idx}
                        className="flex gap-2 text-sm text-[color:var(--foreground)]"
                      >
                        <span className="mt-0.5 shrink-0">⚠️</span>
                        <span>{issue}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Règles de Validation */}
      <Card title="Règles de Validation Standards">
        <div className="space-y-3">
          <div className="flex gap-3 rounded-lg border border-[color:var(--border)] p-3">
            <span>📋</span>
            <div>
              <div className="text-sm font-semibold text-[color:var(--foreground)]">
                Complétude des Données
              </div>
              <div className="mt-1 text-xs text-[color:var(--muted)]">
                Tous les champs obligatoires doivent être remplis
              </div>
            </div>
          </div>
          <div className="flex gap-3 rounded-lg border border-[color:var(--border)] p-3">
            <span>🎯</span>
            <div>
              <div className="text-sm font-semibold text-[color:var(--foreground)]">
                Cohérence ODD
              </div>
              <div className="mt-1 text-xs text-[color:var(--muted)]">
                Les alignements doivent avoir des preuves attachées
              </div>
            </div>
          </div>
          <div className="flex gap-3 rounded-lg border border-[color:var(--border)] p-3">
            <span>💰</span>
            <div>
              <div className="text-sm font-semibold text-[color:var(--foreground)]">
                Contrôle Budgétaire
              </div>
              <div className="mt-1 text-xs text-[color:var(--muted)]">
                Les dépenses ne doivent pas dépasser le budget alloué
              </div>
            </div>
          </div>
          <div className="flex gap-3 rounded-lg border border-[color:var(--border)] p-3">
            <span>📊</span>
            <div>
              <div className="text-sm font-semibold text-[color:var(--foreground)]">
                Détection Outliers
              </div>
              <div className="mt-1 text-xs text-[color:var(--muted)]">
                Les valeurs anormales sont signalées pour vérification
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
