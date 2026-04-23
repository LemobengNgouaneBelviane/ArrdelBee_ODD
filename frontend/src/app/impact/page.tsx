"use client";

import { useEffect, useState } from "react";
import { jsPDF } from "jspdf";
import { apiGet } from "@/lib/api";

type ImpactRow = {
  project: {
    id: number;
    code?: string | null;
    title: string;
    chapitre?: string | null;
    commune?: string | null;
    department?: string | null;
  };
  sdg_goal_code: string | null;
  un_indicator_code: string | null;
  success_pct: number | null;
  color: string;
  proofs: string | null;
  sdg_logo_ref: string | null;
};

export default function Page() {
  const [rows, setRows] = useState<ImpactRow[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    apiGet<ImpactRow[]>("/tableau-de-bord/impact?limit=200")
      .then(setRows)
      .catch((e) => setErr(String(e)));
  }, []);

  function exportPdf() {
    const doc = new jsPDF({ unit: "pt", format: "a4" });
    const margin = 40;
    let y = margin;

    doc.setFontSize(16);
    doc.text("Rapport ODD — Impact (prototype)", margin, y);
    y += 24;

    doc.setFontSize(10);
    doc.text(`Généré le ${new Date().toLocaleString()}`, margin, y);
    y += 20;

    const maxRows = Math.min(rows.length, 30);
    doc.setFontSize(9);
    for (let i = 0; i < maxRows; i++) {
      const r = rows[i];
      const line = [
        `#${r.project.id}`,
        r.project.title.slice(0, 60),
        r.sdg_goal_code ? `ODD ${r.sdg_goal_code}` : "ODD —",
        r.success_pct != null ? `${r.success_pct.toFixed(1)}%` : "—",
        r.color,
      ].join(" | ");
      doc.text(line, margin, y);
      y += 14;
      if (y > 770) {
        doc.addPage();
        y = margin;
      }
    }

    doc.save("rapport-impact-odd.pdf");
  }

  return (
    <div className="space-y-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold">Impact / Rapports</h1>
          <p className="mt-1 text-sm text-zinc-600">
            Restitution des alignements validés + score/couleur (si KPI disponible) + export PDF.
          </p>
        </div>
        <button
          onClick={exportPdf}
          className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800"
          disabled={!rows.length}
        >
          Export PDF (prototype)
        </button>
      </div>

      {err && <div className="rounded-lg bg-rose-50 p-3 text-sm text-rose-800">{err}</div>}

      <div className="rounded-xl border overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-zinc-50 text-left">
            <tr>
              <th className="px-3 py-2">Projet</th>
              <th className="px-3 py-2">ODD</th>
              <th className="px-3 py-2">Indicateur</th>
              <th className="px-3 py-2">Score</th>
              <th className="px-3 py-2">Couleur</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={`${r.project.id}-${r.un_indicator_code ?? "x"}`} className="border-t">
                <td className="px-3 py-2">
                  <div className="font-medium">{r.project.title}</div>
                  <div className="text-xs text-zinc-500">
                    #{r.project.id} {r.project.commune ? `— ${r.project.commune}` : ""}{" "}
                    {r.project.department ? `(${r.project.department})` : ""}
                  </div>
                </td>
                <td className="px-3 py-2">{r.sdg_goal_code ? `ODD ${r.sdg_goal_code}` : "—"}</td>
                <td className="px-3 py-2">{r.un_indicator_code ?? "—"}</td>
                <td className="px-3 py-2">{r.success_pct != null ? `${r.success_pct.toFixed(1)}%` : "—"}</td>
                <td className="px-3 py-2">
                  <span
                    className={[
                      "inline-flex rounded-full px-2 py-0.5 text-xs font-medium",
                      r.color === "VERT"
                        ? "bg-emerald-50 text-emerald-700"
                        : r.color === "ORANGE"
                          ? "bg-amber-50 text-amber-700"
                          : r.color === "ROUGE"
                            ? "bg-rose-50 text-rose-700"
                            : "bg-zinc-100 text-zinc-700",
                    ].join(" ")}
                  >
                    {r.color}
                  </span>
                </td>
              </tr>
            ))}
            {!rows.length && (
              <tr>
                <td colSpan={5} className="px-3 py-10 text-center text-zinc-500">
                  Aucun alignement validé trouvé. Va sur “Alignements” pour en valider un.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

