export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/+$/, "") ?? "http://127.0.0.1:8000";

export async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
  const res = await fetch(url, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API ${res.status} ${res.statusText}: ${text}`);
  }
  return (await res.json()) as T;
}

export async function apiPost<T>(path: string, body: unknown, init?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
  const res = await fetch(url, {
    method: "POST",
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API ${res.status} ${res.statusText}: ${text}`);
  }
  return (await res.json()) as T;
}

// ============= ODD MATCHING & ALIGNMENT UTILITIES (from Rapport_Comprehension_sujet_ODD.pdf) =============

/**
 * Sector-to-ODD Mapping (Extracted from PDF)
 * Basis: Aligning project sectors to UN Sustainable Development Goals
 */
export const SECTOR_TO_ODD_MAPPING: Record<string, number[]> = {
  "santé": [3],
  "health": [3],
  "éducation": [4],
  "education": [4],
  "eau": [6],
  "water": [6],
  "infrastructure": [9, 11],
  "infrastructures": [9, 11],
  "énergie": [7],
  "energy": [7],
  "économie": [8, 5],
  "economy": [8, 5],
  "agriculture": [2, 15],
  "environnement": [13, 15],
  "environment": [13, 15],
};

/**
 * ODD Metadata
 */
export const ODD_METADATA: Record<number, { fr: string; en: string; color: string }> = {
  1: { fr: "Pas de Pauvreté", en: "No Poverty", color: "red" },
  2: { fr: "Faim Zéro", en: "Zero Hunger", color: "yellow" },
  3: { fr: "Bonne Santé", en: "Good Health", color: "emerald" },
  4: { fr: "Éducation Qualité", en: "Quality Education", color: "red" },
  5: { fr: "Égalité Genres", en: "Gender Equality", color: "pink" },
  6: { fr: "Eau & Sains.", en: "Clean Water", color: "blue" },
  7: { fr: "Énergie Propre", en: "Affordable Energy", color: "yellow" },
  8: { fr: "Emplois Décents", en: "Decent Work", color: "red" },
  9: { fr: "Industrie 4.0", en: "Industry 4.0", color: "yellow" },
  10: { fr: "Réduire Inégalit.", en: "Reduced Inequality", color: "red" },
  11: { fr: "Villes Durables", en: "Sustainable Cities", color: "yellow" },
  12: { fr: "Consom. Respon.", en: "Responsible Consumption", color: "yellow" },
  13: { fr: "Climat", en: "Climate Action", color: "green" },
  14: { fr: "Vie Aquatique", en: "Life Below Water", color: "blue" },
  15: { fr: "Vie Terrestre", en: "Life On Land", color: "green" },
  16: { fr: "Paix Justice", en: "Peace & Justice", color: "blue" },
  17: { fr: "Partenariats", en: "Partnerships", color: "gray" },
};

/**
 * Recommended KPIs for each ODD (from PDF: Sector-KPI Recommendations)
 */
export const RECOMMENDED_KPIS: Record<number, { label: string; unit: string; formula: string }[]> = {
  3: [
    { label: "Taux de vaccination (%)", unit: "%", formula: "(vaccinated / total) × 100" },
    { label: "Couverture soins prénataux (%)", unit: "%", formula: "(prenatal / eligible) × 100" },
    { label: "Réduction mortalité (%)", unit: "%", formula: "((baseline - actual) / baseline) × 100" },
  ],
  4: [
    { label: "Taux inscription scolaire (%)", unit: "%", formula: "(enrolled / eligible) × 100" },
    { label: "Ratio enseignant/élève", unit: "ratio", formula: "students / teachers" },
    { label: "Taux achèvement (%)", unit: "%", formula: "(completed / started) × 100" },
  ],
  6: [
    { label: "Population accès eau (%)", unit: "%", formula: "(with_access / total) × 100" },
    { label: "Taux fonctionnalité forages (%)", unit: "%", formula: "(functional / total) × 100" },
    { label: "Réduction temps collecte (h)", unit: "h", formula: "baseline - actual" },
  ],
  8: [
    { label: "Emplois créés", unit: "nombre", formula: "direct_jobs + indirect_jobs" },
    { label: "Taux emploi jeunesse (%)", unit: "%", formula: "(employed_youth / total_youth) × 100" },
  ],
  9: [
    { label: "Km routes construites", unit: "km", formula: "sum(length_per_segment)" },
    { label: "Taux fonctionnalité (%)", unit: "%", formula: "(maintained / total) × 100" },
  ],
};

/**
 * Auto-suggest ODD based on project sector
 * Returns array of ODD numbers that align with the sector
 */
export function suggestODDForSector(sector: string | null): number[] {
  if (!sector) return [];
  
  const normalized = sector.toLowerCase().trim();
  
  // Direct mapping lookup
  for (const [key, oddList] of Object.entries(SECTOR_TO_ODD_MAPPING)) {
    if (normalized.includes(key) || key.includes(normalized)) {
      return oddList;
    }
  }
  
  // Fallback: fuzzy matching on ODD keywords
  for (const [oddNum, metadata] of Object.entries(ODD_METADATA)) {
    const keywords = metadata.fr.toLowerCase().split(" ");
    for (const keyword of keywords) {
      if (normalized.includes(keyword) && keyword.length > 3) {
        return [parseInt(oddNum)];
      }
    }
  }
  
  return [];
}

/**
 * Calculate KPI value with variance and status alert
 * Formula from PDF: KPI% = (Actual ÷ Target) × 100
 * Variance: Actual - Target
 * Status: Red (<-20%), Yellow (-20% to 0%), Green (≥0%)
 */
export function calculateKPI(
  actual: number,
  target: number
): {
  percentage: number;
  variance: number;
  variancePercent: number;
  status: "red" | "yellow" | "green";
  statusLabel: string;
} {
  const percentage = (actual / target) * 100;
  const variance = actual - target;
  const variancePercent = (variance / target) * 100;

  let status: "red" | "yellow" | "green" = "green";
  let statusLabel = "✅ Dépassement";
  if (variancePercent < -20) {
    status = "red";
    statusLabel = "🔴 Alerte critique";
  } else if (variancePercent < 0) {
    status = "yellow";
    statusLabel = "🟡 À surveiller";
  }

  return {
    percentage: Math.round(percentage * 10) / 10,
    variance: Math.round(variance * 10) / 10,
    variancePercent: Math.round(variancePercent * 10) / 10,
    status,
    statusLabel,
  };
}

/**
 * Get AI Assistant decision questions for ODD selection
 * (From PDF: 7 Key Questions for ODD Selection)
 */
export const AI_DECISION_QUESTIONS = [
  {
    num: 1,
    fr: "Le secteur du projet correspond-il logiquement au domaine de l'ODD ?",
    en: "Does project sector logically align with ODD domain?",
  },
  {
    num: 2,
    fr: "Qui bénéficie directement et comment cela correspond-il aux cibles ODD ?",
    en: "Who benefits directly and how does this match ODD targets?",
  },
  {
    num: 3,
    fr: "Quelle est la situation actuelle AVANT le projet (baseline) ?",
    en: "What is baseline situation BEFORE the project?",
  },
  {
    num: 4,
    fr: "Peut-on quantifier la contribution avec des indicateurs concrets et mesurables ?",
    en: "Can we quantify contribution with concrete, measurable indicators?",
  },
  {
    num: 5,
    fr: "Quand les résultats doivent-ils être atteints ? Timeline réaliste ?",
    en: "When should results be achieved? Realistic timeline?",
  },
  {
    num: 6,
    fr: "Pouvons-nous réellement collecter et vérifier les preuves ?",
    en: "Can we realistically collect and verify proof/evidence?",
  },
  {
    num: 7,
    fr: "Le projet contribue-t-il à plusieurs ODD ? Cohérence logique ?",
    en: "Does project contribute to multiple ODD? Logical consistency?",
  },
];

