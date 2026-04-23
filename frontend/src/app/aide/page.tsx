'use client';

import { Card, PageHeader, SectionTitle } from "@/components/ui";
import { useState } from "react";

interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category: "general" | "projets" | "rapports" | "validation" | "technique";
}

const faqs: FAQItem[] = [
  {
    id: "1",
    category: "general",
    question: "Qu'est-ce qu'ArrdelBee?",
    answer:
      "ArrdelBee est une plateforme de suivi et d'alignement des projets de développement local avec les Objectifs de Développement Durable (ODD) de l'ONU.",
  },
  {
    id: "2",
    category: "projets",
    question: "Comment créer un nouveau projet?",
    answer:
      "Allez à la section Projets et cliquez sur '+ Nouveau Projet'. Remplissez le formulaire d'information du projet, puis validez. Le projet sera créé et prêt à être aligné avec les ODD.",
  },
  {
    id: "3",
    category: "projets",
    question: "Comment aligner un projet aux ODD?",
    answer:
      "Depuis la page Alignements, sélectionnez un projet. Choisissez les ODD pertinents et décrivez l'impact du projet pour chaque ODD. Attachez les preuves (documents, photos, vidéos).",
  },
  {
    id: "4",
    category: "rapports",
    question: "Comment générer un rapport?",
    answer:
      "Allez à Rapports > Générateur de Rapports. Sélectionnez le type (Trimestriel, Annuel, etc.), la période, le secteur et la région. Cliquez sur 'Générer le Rapport'.",
  },
  {
    id: "5",
    category: "validation",
    question: "Qu'est-ce que la validation de données?",
    answer:
      "La validation vérifie que les alignements ODD, les rapports et indicateurs respectent les normes de qualité avant archivage. Les alertes critiques doivent être corrigées.",
  },
  {
    id: "6",
    category: "technique",
    question: "Comment signaler un bug ou un problème?",
    answer:
      "Envoyez un email à support@arrdelbee.cm avec une description du problème et des captures d'écran si possible. Notre équipe vous répondra dans les 24 heures.",
  },
];

export default function HelpPage() {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const filteredFAQs = faqs.filter((faq) => {
    const matchesSearch =
      faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      faq.answer.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !selectedCategory || faq.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-10">
      <PageHeader
        title="Centre d'Aide"
        subtitle="Documentation, FAQ et support pour utiliser ArrdelBee"
      />

      {/* Contact Support */}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <div className="text-center">
            <div className="text-3xl">📧</div>
            <div className="mt-3 text-sm font-semibold text-[color:var(--foreground)]">
              Support par Email
            </div>
            <div className="mt-1 text-xs text-[color:var(--muted)]">
              support@arrdelbee.cm
            </div>
            <p className="mt-2 text-xs text-[color:var(--muted)]">
              Réponse garantie dans les 24 heures
            </p>
          </div>
        </Card>
        <Card>
          <div className="text-center">
            <div className="text-3xl">🎓</div>
            <div className="mt-3 text-sm font-semibold text-[color:var(--foreground)]">
              Documentation Complète
            </div>
            <div className="mt-1 text-xs text-[color:var(--muted)]">
              Guides utilisateur et tutoriels
            </div>
            <button className="mt-3 rounded-lg bg-[color:var(--primary)] px-3 py-1.5 text-xs font-semibold text-white hover:shadow-md transition">
              Consulter →
            </button>
          </div>
        </Card>
      </div>

      {/* FAQ Section */}
      <div>
        <SectionTitle 
          title="Questions Fréquemment Posées"
          description="Trouvez les réponses à vos questions"
        />

        {/* Recherche & Filtres */}
        <div className="mt-4 space-y-3">
          <input
            type="text"
            placeholder="Rechercher dans les FAQ..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-lg border border-[color:var(--border)] bg-white px-4 py-2 text-sm text-[color:var(--foreground)] placeholder-[color:var(--muted)]"
          />
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
                selectedCategory === null
                  ? "bg-[color:var(--primary)] text-white"
                  : "border border-[color:var(--border)] bg-white text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)]"
              }`}
            >
              Tous
            </button>
            <button
              onClick={() => setSelectedCategory("general")}
              className={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
                selectedCategory === "general"
                  ? "bg-[color:var(--primary)] text-white"
                  : "border border-[color:var(--border)] bg-white text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)]"
              }`}
            >
              Général
            </button>
            <button
              onClick={() => setSelectedCategory("projets")}
              className={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
                selectedCategory === "projets"
                  ? "bg-[color:var(--primary)] text-white"
                  : "border border-[color:var(--border)] bg-white text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)]"
              }`}
            >
              Projets
            </button>
            <button
              onClick={() => setSelectedCategory("rapports")}
              className={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
                selectedCategory === "rapports"
                  ? "bg-[color:var(--primary)] text-white"
                  : "border border-[color:var(--border)] bg-white text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)]"
              }`}
            >
              Rapports
            </button>
            <button
              onClick={() => setSelectedCategory("validation")}
              className={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
                selectedCategory === "validation"
                  ? "bg-[color:var(--primary)] text-white"
                  : "border border-[color:var(--border)] bg-white text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)]"
              }`}
            >
              Validation
            </button>
          </div>
        </div>

        {/* FAQ Items */}
        <div className="mt-4 space-y-2">
          {filteredFAQs.map((faq) => (
            <Card key={faq.id} hoverable={false} className="p-0">
              <button
                onClick={() =>
                  setExpandedId(expandedId === faq.id ? null : faq.id)
                }
                className="flex w-full items-center justify-between p-4 hover:bg-[color:var(--surface-2)]/50 transition text-left"
              >
                <div>
                  <h4 className="font-semibold text-[color:var(--foreground)]">
                    {faq.question}
                  </h4>
                </div>
                <span className="ml-3 shrink-0 text-xl">
                  {expandedId === faq.id ? "−" : "+"}
                </span>
              </button>
              {expandedId === faq.id && (
                <div className="border-t border-[color:var(--border)] bg-white p-4">
                  <p className="text-sm text-[color:var(--muted)]">
                    {faq.answer}
                  </p>
                </div>
              )}
            </Card>
          ))}
        </div>

        {filteredFAQs.length === 0 && (
          <div className="rounded-lg border border-dashed border-[color:var(--border)] bg-[color:var(--surface-2)]/50 p-8 text-center">
            <p className="text-sm text-[color:var(--muted)]">
              Aucune question trouvée. Essayez d'autres termes de recherche.
            </p>
          </div>
        )}
      </div>

      {/* Ressources Utiles */}
      <div>
        <SectionTitle 
          title="Ressources Utiles"
          description="Accédez à la documentation complète"
        />
        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          <Card>
            <div className="space-y-3">
              <div className="text-lg">📖</div>
              <h3 className="font-semibold text-[color:var(--foreground)]">
                Guide de l'Utilisateur
              </h3>
              <p className="text-xs text-[color:var(--muted)]">
                Documentation complète sur toutes les fonctionnalités
              </p>
              <button className="text-xs font-semibold text-[color:var(--primary)] hover:underline">
                Consulter →
              </button>
            </div>
          </Card>
          <Card>
            <div className="space-y-3">
              <div className="text-lg">🎥</div>
              <h3 className="font-semibold text-[color:var(--foreground)]">
                Tutoriels Vidéo
              </h3>
              <p className="text-xs text-[color:var(--muted)]">
                Vidéos pas à pas pour apprendre à utiliser ArrdelBee
              </p>
              <button className="text-xs font-semibold text-[color:var(--primary)] hover:underline">
                Regarder →
              </button>
            </div>
          </Card>
          <Card>
            <div className="space-y-3">
              <div className="text-lg">🎓</div>
              <h3 className="font-semibold text-[color:var(--foreground)]">
                Formation en Ligne
              </h3>
              <p className="text-xs text-[color:var(--muted)]">
                Sessions de formation gratuites pour votre équipe
              </p>
              <button className="text-xs font-semibold text-[color:var(--primary)] hover:underline">
                S'inscrire →
              </button>
            </div>
          </Card>
          <Card>
            <div className="space-y-3">
              <div className="text-lg">📄</div>
              <h3 className="font-semibold text-[color:var(--foreground)]">
                Normes & Standards
              </h3>
              <p className="text-xs text-[color:var(--muted)]">
                Documentation ODD et standards de validation
              </p>
              <button className="text-xs font-semibold text-[color:var(--primary)] hover:underline">
                Consulter →
              </button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
