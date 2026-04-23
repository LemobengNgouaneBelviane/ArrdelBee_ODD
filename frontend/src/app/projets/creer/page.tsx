"use client";

import { useState } from "react";
import { PageHeader, Card, Button, Input, Select, Textarea, Alert, SectionTitle } from "@/components/ui";
import { apiPost } from "@/lib/api";

export default function Page() {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    chapitre: "",
    department: "",
    commune: "",
    budget: "",
    startDate: "",
    endDate: "",
    sector: "",
  });

  const [err, setErr] = useState<string | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setMsg(null);

    if (!formData.title.trim() || !formData.description.trim()) {
      setErr("Le titre et la description sont requis");
      return;
    }

    setIsSubmitting(true);
    try {
      // TODO: Adapter l'endpoint à votre API
      const res = await apiPost("/projets", {
        title: formData.title,
        description: formData.description,
        chapitre: formData.chapitre || null,
        department: formData.department || null,
        commune: formData.commune || null,
        budget: formData.budget ? parseInt(formData.budget) : null,
        start_date: formData.startDate || null,
        end_date: formData.endDate || null,
        sector: formData.sector || null,
      });
      setMsg(`Projet créé avec succès (ID: ${(res as any).id})`);
      setFormData({
        title: "",
        description: "",
        chapitre: "",
        department: "",
        commune: "",
        budget: "",
        startDate: "",
        endDate: "",
        sector: "",
      });
    } catch (e) {
      setErr(String(e));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-8">
      <PageHeader
        title="Enregistrement Nouveau Projet"
        subtitle="Créez un nouveau projet et débutez son alignement aux Objectifs de Développement Durable"
      />

      {err && (
        <Alert tone="danger" title="Erreur">
          {err}
        </Alert>
      )}

      {msg && (
        <Alert tone="success" title="Succès">
          {msg}
        </Alert>
      )}

      <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        {/* Formulaire Principal */}
        <div className="lg:col-span-2 space-y-6">
          {/* Section Identification */}
          <Card title="01. Identification du Projet" description="Informations de base du projet">
            <div className="space-y-4">
              <Input
                label="Nom du Projet"
                placeholder="Ex: Réhabilitation de l'Axe Principal Sud-Ouest"
                value={formData.title}
                onChange={(e) => handleChange("title", e.target.value)}
                required
              />

              <Textarea
                label="Description"
                placeholder="Décrivez les objectifs, activités et bénéficiaires du projet..."
                value={formData.description}
                onChange={(e) => handleChange("description", e.target.value)}
                rows={4}
                required
              />

              <Select
                label="Chapitre / Secteur d'Activité"
                value={formData.chapitre}
                onChange={(e) => handleChange("chapitre", e.target.value)}
              >
                <option value="">— Non spécifié —</option>
                <option value="SANTE">Santé & Bien-être</option>
                <option value="EDUCATION">Éducation</option>
                <option value="INFRASTRUCTURE">Infrastructure & Transport</option>
                <option value="EAU">Eau & Assainissement</option>
                <option value="ENERGIE">Énergie</option>
                <option value="AGRICULTURE">Agriculture & Alimentation</option>
                <option value="ENVIRONNEMENT">Environnement</option>
                <option value="ECONOMIE">Économie & Emploi</option>
              </Select>
            </div>
          </Card>

          {/* Section Localisation */}
          <Card title="02. Localisation Administrative" description="Zone géographique du projet">
            <div className="space-y-4">
              <Select
                label="Région"
                value={formData.department}
                onChange={(e) => handleChange("department", e.target.value)}
              >
                <option value="">— Sélectionner —</option>
                <option value="NORD">Région du Nord</option>
                <option value="NORD-OUEST">Région du Nord-Ouest</option>
                <option value="OUEST">Région du Ouest</option>
                <option value="CENTRE">Région du Centre</option>
                <option value="SUD">Région du Sud</option>
                <option value="EXTREMENORD">Région de l'Extrême-Nord</option>
              </Select>

              <Input
                label="Commune / District"
                placeholder="Ex: Yaoundé, Douala"
                value={formData.commune}
                onChange={(e) => handleChange("commune", e.target.value)}
              />
            </div>
          </Card>

          {/* Section Calendrier & Budget */}
          <Card title="03. Calendrier et Budget" description="Durée et ressources du projet">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <Input
                label="Date de Début"
                type="date"
                value={formData.startDate}
                onChange={(e) => handleChange("startDate", e.target.value)}
              />

              <Input
                label="Date de Fin Prévue"
                type="date"
                value={formData.endDate}
                onChange={(e) => handleChange("endDate", e.target.value)}
              />

              <Input
                label="Budget Prévisionnel (FCFA)"
                type="number"
                placeholder="Ex: 50000000"
                value={formData.budget}
                onChange={(e) => handleChange("budget", e.target.value)}
              />

              <Select
                label="Secteur Prioritaire"
                value={formData.sector}
                onChange={(e) => handleChange("sector", e.target.value)}
              >
                <option value="">— Non spécifié —</option>
                <option value="PUBLIC">Public</option>
                <option value="PRIVATE">Privé</option>
                <option value="NGO">ONG / Société Civile</option>
                <option value="MIXED">Partenariat Public-Privé</option>
              </Select>
            </div>
          </Card>
        </div>

        {/* Résumé & Actions */}
        <div className="lg:col-span-1">
          <div className="sticky top-8 space-y-6">
            {/* Checklist */}
            <Card title="Avant de Valider" hoverable={false}>
              <div className="space-y-2">
                {[
                  { done: !!formData.title.trim(), label: "Nom du projet rempli" },
                  { done: !!formData.description.trim(), label: "Description remplie" },
                  { done: !!formData.chapitre, label: "Secteur sélectionné" },
                  { done: !!formData.department, label: "Région sélectionnée" },
                ].map((item, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-sm">
                    <div className={`w-4 h-4 rounded border ${item.done ? "bg-emerald-500 border-emerald-500" : "border-[color:var(--border)]"}`} />
                    <span className={item.done ? "text-[color:var(--foreground)]" : "text-[color:var(--muted)]"}>{item.label}</span>
                  </div>
                ))}
              </div>
            </Card>

            {/* Actions */}
            <div className="space-y-2">
              <Button onClick={handleSubmit} className="w-full" disabled={isSubmitting}>
                {isSubmitting ? "Enregistrement..." : "✓ Créer le Projet"}
              </Button>
              <Button variant="secondary" className="w-full">
                Annuler
              </Button>
            </div>

            {/* Info */}
            <Card hoverable={false} className="bg-blue-50 border-blue-200">
              <div className="text-xs text-blue-900">
                <div className="font-semibold mb-2">💡 Conseil</div>
                <p>Renseignez au minimum: Nom, Description et Secteur. Les autres champs peuvent être complétés ultérieurement.</p>
              </div>
            </Card>
          </div>
        </div>
      </form>
    </div>
  );
}
