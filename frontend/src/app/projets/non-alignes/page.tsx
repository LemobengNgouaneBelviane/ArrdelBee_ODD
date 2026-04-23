import { apiGet } from "@/lib/api";
import { Alert, Badge, PageHeader, Table } from "@/components/ui";

type UnalignedProject = {
  id: number;
  code: string | null;
  title: string;
  chapitre: string | null;
  commune: string | null;
  department: string | null;
  suggested_sdg_codes: string[];
};

export default async function Page() {
  let rows: UnalignedProject[] = [];
  let apiError: string | null = null;
  try {
    rows = await apiGet<UnalignedProject[]>("/projets/non-alignes?limit=200");
  } catch (e) {
    apiError = String(e);
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Projets Non Alignés"
        subtitle="Projets sans alignement ODD validé. Consultez les suggestions pour débuter l'alignement"
      />

      {apiError && (
        <Alert tone="danger" title="Erreur de connexion">
          Le backend API n'est pas accessible à <code className="font-mono text-xs">http://127.0.0.1:8000</code>. 
          Vérifiez que le serveur FastAPI est lancé.
        </Alert>
      )}

      <div className="flex items-center justify-between">
        <div className="text-sm">
          <span className="text-[color:var(--muted)]">Résultats:</span> <span className="font-semibold text-[color:var(--foreground)]">{rows.length}</span>
        </div>
      </div>

      <Table
        columns={[
          { label: "Projet", className: "w-2/5" },
          { label: "Chapitre" },
          { label: "Localisation" },
          { label: "Suggestions ODD" },
        ]}
      >
        {rows.slice(0, 200).map((p) => (
          <tr key={p.id} className="hover:bg-[color:var(--surface-2)] transition">
            <td className="px-4 py-3">
              <div className="font-medium text-[color:var(--foreground)]">{p.title}</div>
              <div className="mt-1 text-xs text-[color:var(--muted)]">ID #{p.id}</div>
            </td>
            <td className="px-4 py-3 text-sm">{p.chapitre ?? "—"}</td>
            <td className="px-4 py-3 text-sm">
              <div className="font-medium">{p.commune ?? "—"}</div>
              {p.department && <div className="text-xs text-[color:var(--muted)]">{p.department}</div>}
            </td>
            <td className="px-4 py-3">
              {p.suggested_sdg_codes.length ? (
                <div className="flex flex-wrap gap-1">
                  {p.suggested_sdg_codes.map((c) => (
                    <Badge key={c} label={`ODD ${c}`} oddCode={c} />
                  ))}
                </div>
              ) : (
                <span className="text-xs text-[color:var(--muted)]">Pas d'suggestions</span>
              )}
            </td>
          </tr>
        ))}
        {!rows.length && (
          <tr>
            <td colSpan={4} className="px-4 py-10 text-center text-[color:var(--muted)]">
              Aucun projet à afficher
            </td>
          </tr>
        )}
      </Table>
    </div>
  );
}
