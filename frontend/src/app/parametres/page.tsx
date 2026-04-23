'use client';

import { Card, PageHeader, SectionTitle } from "@/components/ui";

export default function SettingsPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        title="Paramètres"
        subtitle="Configuration institutionnelle & préférences de la plateforme"
      />

      {/* Profil Institutionnel */}
      <div>
        <SectionTitle title="Profil Institutionnel" />
        <Card title="Informations Générales" className="mt-3">
          <div className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-[color:var(--foreground)]">
                  Nom de l'Institution
                </label>
                <input
                  type="text"
                  defaultValue="Commune d'Arrondissement de Yaoundé VII"
                  className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)]"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-[color:var(--foreground)]">
                  Type d'Institution
                </label>
                <select className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)]">
                  <option>Commune d'Arrondissement</option>
                  <option>Région</option>
                  <option>Ministère</option>
                  <option>Autre</option>
                </select>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-[color:var(--foreground)]">
                  Région
                </label>
                <select className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)]">
                  <option>Centre</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-[color:var(--foreground)]">
                  Département
                </label>
                <select className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)]">
                  <option>Mfoundé</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-[color:var(--foreground)]">
                Logo de l'Institution
              </label>
              <div className="mt-2 flex items-center gap-4">
                <div className="h-16 w-16 rounded-lg border border-dashed border-[color:var(--border)] bg-[color:var(--surface-2)] flex items-center justify-center">
                  🖼️
                </div>
                <button className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                  Télécharger Logo
                </button>
              </div>
            </div>

            <button className="w-full rounded-lg bg-[color:var(--primary)] px-4 py-3 text-sm font-semibold text-white shadow-sm hover:shadow-md transition">
              💾 Enregistrer les Informations
            </button>
          </div>
        </Card>
      </div>

      {/* Coordonnées de Contact */}
      <div>
        <SectionTitle title="Coordonnées de Contact" />
        <Card title="Informations de Contact" className="mt-3">
          <div className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-[color:var(--foreground)]">
                  Email Officiel
                </label>
                <input
                  type="email"
                  defaultValue="contact@yaoundé7.cm"
                  className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)]"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-[color:var(--foreground)]">
                  Téléphone
                </label>
                <input
                  type="tel"
                  defaultValue="+237 222 33 44 5"
                  className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)]"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-[color:var(--foreground)]">
                Site Web
              </label>
              <input
                type="url"
                defaultValue="www.yaoundé7.cn"
                className="mt-1 w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)]"
              />
            </div>

            <button className="w-full rounded-lg bg-[color:var(--primary)] px-4 py-3 text-sm font-semibold text-white shadow-sm hover:shadow-md transition">
              💾 Enregistrer les Coordonnées
            </button>
          </div>
        </Card>
      </div>

      {/* Documents de Programmation */}
      <div>
        <SectionTitle title="Documents de Programmation" />
        <Card title="Documents PCD & Stratégiques" className="mt-3">
          <div className="space-y-3">
            <div className="rounded-lg border border-[color:var(--border)] p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-semibold text-[color:var(--foreground)]">
                    Plan Communal de Développement (PCD)
                  </div>
                  <div className="mt-1 text-xs text-[color:var(--muted)]">
                    Document PCD principal de la programmation
                  </div>
                </div>
                <button className="rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                  📁 Parcourir
                </button>
              </div>
            </div>
            <div className="rounded-lg border border-[color:var(--border)] p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-semibold text-[color:var(--foreground)]">
                    Documents Stratégiques ODD
                  </div>
                  <div className="mt-1 text-xs text-[color:var(--muted)]">
                    Fichiers PDF supplémentaires pour programmation
                  </div>
                </div>
                <button className="rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                  + Ajouter
                </button>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Préférences de Rapport */}
      <div>
        <SectionTitle title="Préférences de Rapport" />
        <Card title="Configuration des Rapports" className="mt-3">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                defaultChecked
                className="rounded border-[color:var(--border)]"
              />
              <label className="text-sm text-[color:var(--foreground)]">
                Inclure les graphiques dans les rapports PDF
              </label>
            </div>
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                defaultChecked
                className="rounded border-[color:var(--border)]"
              />
              <label className="text-sm text-[color:var(--foreground)]">
                Ajouter la cartographie géographique
              </label>
            </div>
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                className="rounded border-[color:var(--border)]"
              />
              <label className="text-sm text-[color:var(--foreground)]">
                Générer rapports automatiques le 15 de chaque mois
              </label>
            </div>
          </div>
        </Card>
      </div>

      {/* Intégrations */}
      <div>
        <SectionTitle title="Intégrations & API" />
        <Card title="Accès API" className="mt-3">
          <div className="space-y-4">
            <p className="text-sm text-[color:var(--muted)]">
              Clé API pour intégrations externes avec votre instance ArrdelBee
            </p>
            <div className="flex items-center gap-2 rounded-lg border border-[color:var(--border)] bg-[color:var(--surface-2)] p-3">
              <code className="flex-1 font-mono text-xs text-[color:var(--foreground)]">
                sk_live_4eC39HqLyjWDarhtT657jxnr...
              </code>
              <button className="rounded-lg border border-[color:var(--border)] bg-white px-3 py-2 text-xs font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)]">
                📋 Copier
              </button>
            </div>
            <button className="w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-3 text-sm font-semibold text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)] transition">
                🔄 Régénérer Clé API
            </button>
          </div>
        </Card>
      </div>
    </div>
  );
}
