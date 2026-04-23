'use client';

import { Card, PageHeader, SectionTitle, Stat } from "@/components/ui";

interface User {
  id: string;
  initials: string;
  name: string;
  email: string;
  institution: string;
  role: string;
  status: "actif" | "en-attente" | "inactif";
}

const users: User[] = [
  {
    id: "1",
    initials: "JE",
    name: "Jean Ebolowa",
    email: "jebolowa@gov.cm",
    institution: "Commune d'Ebolowa I",
    role: "Point Focal",
    status: "actif",
  },
  {
    id: "2",
    initials: "MA",
    name: "Marie Atangana",
    email: "matangana@douala.cm",
    institution: "C.U.D (Douala)",
    role: "Validateur",
    status: "actif",
  },
  {
    id: "3",
    initials: "PF",
    name: "Paul Fuda",
    email: "p.fuda@projects.cm",
    institution: "Commune de Yaoundé VI",
    role: "Responsable Projet",
    status: "en-attente",
  },
  {
    id: "4",
    initials: "SY",
    name: "Samuel Yvan",
    email: "s.yvan@admin.cm",
    institution: "Administration Centrale",
    role: "Admin",
    status: "actif",
  },
];

const roleColors: Record<string, string> = {
  "Point Focal": "bg-blue-100 text-blue-700",
  Validateur: "bg-emerald-100 text-emerald-700",
  "Responsable Projet": "bg-amber-100 text-amber-700",
  Admin: "bg-red-100 text-red-700",
};

const statusColors = {
  actif: "bg-emerald-50 border-emerald-200 text-emerald-700",
  "en-attente": "bg-amber-50 border-amber-200 text-amber-700",
  inactif: "bg-slate-50 border-slate-200 text-slate-700",
};

export default function UsersPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        title="Gestion des Utilisateurs"
        subtitle="Annuaire institutionnel et accès des utilisateurs"
        actions={
          <button className="inline-flex items-center rounded-lg bg-[color:var(--primary)] px-4 py-2 text-sm font-semibold text-white shadow-sm hover:shadow-md transition">
            + Nouvel Utilisateur
          </button>
        }
      />

      {/* Statistiques */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Administrateurs" value="05" color="default" icon="👤" />
        <Stat label="Points Focaux" value="18" color="success" icon="" />
        <Stat label="Utilisateurs Actifs" value="42" color="primary" icon="✓" />
        <Stat label="En Attente" value="3" color="default" icon="⏳" />
      </div>

      {/* Filtres */}
      <div className="flex flex-wrap gap-3">
        <select className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] hover:border-[color:var(--primary)]/50">
          <option>Tous les Rôles</option>
          <option>Admin</option>
          <option>Point Focal</option>
          <option>Validateur</option>
          <option>Responsable Projet</option>
        </select>
        <select className="rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] hover:border-[color:var(--primary)]/50">
          <option>Tous les Statuts</option>
          <option>Actif</option>
          <option>En Attente</option>
          <option>Inactif</option>
        </select>
        <input
          type="text"
          placeholder="Rechercher un utilisateur..."
          className="flex-1 rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] placeholder-[color:var(--muted)]"
        />
      </div>

      {/* Tableau des Utilisateurs */}
      <div className="space-y-3">
        <SectionTitle 
          title={`Utilisateurs (${users.length})`}
          description="Cliquez sur un utilisateur pour modifier ses permissions ou ses informations"
        />
        <div className="overflow-x-auto rounded-lg border border-[color:var(--border)]">
          <table className="w-full">
            <thead className="border-b border-[color:var(--border)] bg-[color:var(--surface-2)]">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-[color:var(--muted)]">
                  Utilisateur
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-[color:var(--muted)]">
                  Institution
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-[color:var(--muted)]">
                  Rôle
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-[color:var(--muted)]">
                  Statut
                </th>
                <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-[color:var(--muted)]">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[color:var(--border)]">
              {users.map((user) => (
                <tr
                  key={user.id}
                  className="hover:bg-[color:var(--surface-2)]/50 transition"
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-[color:var(--primary)] to-[color:var(--primary)]/70 text-sm font-semibold text-white">
                        {user.initials}
                      </div>
                      <div>
                        <div className="text-sm font-semibold text-[color:var(--foreground)]">
                          {user.name}
                        </div>
                        <div className="text-xs text-[color:var(--muted)]">
                          {user.email}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-[color:var(--foreground)]">
                      {user.institution}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${roleColors[user.role] || "bg-gray-100 text-gray-700"}`}
                    >
                      {user.role}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${statusColors[user.status]}`}
                    >
                      {user.status === "actif" && "✓ Actif"}
                      {user.status === "en-attente" && "⏳ En Attente"}
                      {user.status === "inactif" && "✗ Inactif"}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-sm font-semibold text-[color:var(--primary)] hover:underline">
                      Modifier
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Maîtrise des Accès */}
      <Card title="Contrôle d'Accès & Permissions">
        <div className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-lg border border-[color:var(--border)] p-4">
              <div className="text-sm font-semibold text-[color:var(--foreground)]">
                Administrateurs
              </div>
              <div className="mt-2 text-xs text-[color:var(--muted)]">
                Accès complet · Gestion système · Création utilisateurs
              </div>
              <div className="mt-3 text-2xl font-bold text-[color:var(--primary)]">05</div>
            </div>
            <div className="rounded-lg border border-[color:var(--border)] p-4">
              <div className="text-sm font-semibold text-[color:var(--foreground)]">
                Points Focaux (CTD)
              </div>
              <div className="mt-2 text-xs text-[color:var(--muted)]">
                Collecte données · Saisie indicateurs · Export rapports
              </div>
              <div className="mt-3 text-2xl font-bold text-emerald-600">18</div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
