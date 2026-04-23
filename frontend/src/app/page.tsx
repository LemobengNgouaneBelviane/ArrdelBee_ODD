import Link from "next/link";
import { Card, SectionTitle, Badge } from "@/components/ui";

export default function Home() {
  const priorityODD = [
    { num: "3", label: "Bonne Santé", color: "bg-emerald-500", icon: "💚" },
    { num: "4", label: "Éducation de Qualité", color: "bg-red-600", icon: "📚" },
    { num: "6", label: "Eau & Assainissement", color: "bg-blue-500", icon: "💧" },
    { num: "9", label: "Industrie & Innovation", color: "bg-orange-500", icon: "🏭" },
    { num: "11", label: "Villes Durables", color: "bg-yellow-500", icon: "🏙️" },
  ];

  const stats = [
    { label: "Projets Actifs", value: "127", subtext: "En pilotage" },
    { label: "ODD Alignés", value: "2,340", subtext: "Liens validés" },
    { label: "Bénéficiaires", value: "45,892", subtext: "Touchés" },
    { label: "Communes", value: "12", subtext: "Engagées" },
  ];

  const workflows = [
    { step: 1, label: "Saisie", desc: "Enregistrement initial du projet", icon: "📝" },
    { step: 2, label: "Vérification", desc: "Contrôle qualité des données", icon: "✓" },
    { step: 3, label: "Validation CTD", desc: "Approbation district", icon: "🔍" },
    { step: 4, label: "Certification ARRDEL", desc: "Publication officielle", icon: "" },
  ];

  const features = [
    {
      title: "🧠 Moteur d'Alignement Automatique",
      desc: "Liaison intelligente entre projets, secteurs et ODD—éliminant les connexions manuelles et non standardisées.",
    },
    {
      title: "📸 Vérification Basée sur les Preuves",
      desc: "Géolocalisation, photos et rapports techniques obligatoires avant publication—traçabilité complète.",
    },
    {
      title: "🔄 Interopérabilité en Temps Réel",
      desc: "Intégration transparente avec S&E, authentification, cartographie SIG et gestion documentaire existantes.",
    },
    {
      title: "📊 Rapports Multi-Audiences",
      desc: "Une source unique : tableaux de bord interactifs pour décideurs, PDF pour partenaires, portails publics anonymisés.",
    },
    {
      title: "🔐 Gouvernance Intégrée",
      desc: "Flux de travail multi-secteurs avec accès granulaire assurant l'intégrité et la traçabilité des données.",
    },
    {
      title: "🌍 Alignement Camerounais",
      desc: "Adapter les ODD au contexte local : communes d'arrondissement, PCD, PRD, réalités territoriales.",
    },
  ];

  const quickActions = [
    { title: "Nouveau Projet", icon: "🚀", href: "/projets/creer", color: "from-blue-500 to-blue-600", desc: "Enregistrer un nouveau projet" },
    { title: "Aligner aux ODD", icon: "🎯", href: "/alignements", color: "from-green-500 to-green-600", desc: "Lier projets et objectifs" },
    { title: "Collecter Preuves", icon: "📸", href: "/collecte-preuves", color: "from-purple-500 to-purple-600", desc: "Fournir des preuves d'impact" },
    { title: "Cartographie", icon: "🗺️", href: "/cartographie", color: "from-teal-500 to-teal-600", desc: "Voir les projets géolocalisés" },
  ];

  return (
    <div className="space-y-12">
      {/* HERO SECTION */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-amber-600 via-amber-700 to-amber-900 p-12 text-white">
        <div className="absolute -top-20 -right-20 w-64 h-64 bg-white opacity-5 rounded-full blur-3xl"></div>
        <div className="relative z-10 max-w-3xl">
          <h1 className="text-5xl font-bold mb-4 leading-tight">
            De l'Action Locale au Changement Global Mesurable
          </h1>
          <p className="text-lg text-amber-50 mb-8">
            Alignez vos projets de développement aux Objectifs de Développement Durable, toutes les preuves d'impact en un seul endroit.
          </p>
          <div className="flex gap-4 flex-wrap">
            <Link href="/projets/creer" className="px-8 py-3 bg-white text-amber-900 font-semibold rounded-lg hover:bg-amber-50 transition-all shadow-lg">
              Créer un Projet
            </Link>
            <Link href="/referentiel-odd" className="px-8 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white/10 transition-all">
              En Savoir Plus
            </Link>
          </div>
        </div>
      </div>

      {/* KEY METRICS */}
      <div>
        <SectionTitle title="Vue d'Ensemble" description="État actuel de la plateforme ArrdelBee ODD" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
          {stats.map((stat) => (
            <Card key={stat.label} hoverable className="p-6 border-l-4 border-amber-500">
              <div className="text-3xl font-bold text-amber-700 mb-2">{stat.value}</div>
              <div className="font-semibold text-gray-900">{stat.label}</div>
              <div className="text-xs text-gray-500 mt-1">{stat.subtext}</div>
            </Card>
          ))}
        </div>
      </div>

      {/* PRIORITY ODD SECTION */}
      <div>
        <SectionTitle title="ODD Prioritaires" description="Phase MVP : Focus sur 5 objectifs clés pour l'impact maximal" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mt-6">
          {priorityODD.map((odd) => (
            <Card key={odd.num} hoverable className="p-6 text-center border-2 border-transparent hover:border-amber-300 transition-all">
              <div className={`${odd.color} w-16 h-16 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4`}>
                {odd.icon}
              </div>
              <div className="text-yellow-600 font-bold text-lg mb-1">ODD {odd.num}</div>
              <h3 className="font-semibold text-gray-900">{odd.label}</h3>
            </Card>
          ))}
        </div>
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-sm text-blue-900">
            <strong>+ ODD 1, 7, 8, 12:</strong> Intégration partielle par retombées de projets (accès eau potable, énergie, création d'emplois locaux, infrastructures durables)
          </p>
        </div>
      </div>

      {/* 4-LEVEL WORKFLOW */}
      <div>
        <SectionTitle title="Flux de Validation en 4 Étapes" description="Garantir la qualité, la traçabilité et la certification officielle des données" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
          {workflows.map((wf, idx) => (
            <div key={wf.step} className="relative">
              <Card hoverable className="p-6 h-full">
                <div className="flex items-start justify-between mb-4">
                  <div className="text-3xl">{wf.icon}</div>
                  <div className="w-8 h-8 bg-amber-100 text-amber-700 rounded-full flex items-center justify-center text-sm font-bold">
                    {wf.step}
                  </div>
                </div>
                <h3 className="text-base font-bold text-gray-900 mb-1">{wf.label}</h3>
                <p className="text-sm text-gray-600">{wf.desc}</p>
              </Card>
              {idx < 3 && (
                <div className="hidden lg:flex absolute top-1/2 -right-2 w-4 h-1 bg-amber-400 transform -translate-y-1/2 z-10"></div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* QUICK ACTION BUTTONS */}
      <div>
        <SectionTitle title="Actions Rapides" description="Accédez aux principales fonctionnalités" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
          {quickActions.map((action) => (
            <Link key={action.title} href={action.href}>
              <Card hoverable className={`p-6 text-white bg-gradient-to-br ${action.color} cursor-pointer transition-all transform hover:scale-105 h-full`}>
                <div className="text-4xl mb-3">{action.icon}</div>
                <h3 className="font-bold text-lg">{action.title}</h3>
                <p className="text-xs mt-1 text-white/80">{action.desc}</p>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* KEY FEATURES */}
      <div>
        <SectionTitle title="Caractéristiques Clés" description="Ce qui rend ArrdelBee ODD unique et efficace" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
          {features.map((feature, idx) => (
            <Card key={idx} className="p-6 border-l-4 border-amber-500 hover:border-amber-700 transition-all">
              <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
              <p className="text-sm text-gray-600 leading-relaxed">{feature.desc}</p>
            </Card>
          ))}
        </div>
      </div>

      {/* CTA SECTION */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-green-600 to-teal-700 p-12 text-white text-center">
        <div className="absolute -top-20 -right-20 w-64 h-64 bg-white opacity-5 rounded-full blur-3xl"></div>
        <div className="relative z-10">
          <h2 className="text-3xl font-bold mb-4">Prêt à Transformer Votre Impact Local ?</h2>
          <p className="text-lg text-green-50 mb-8 max-w-2xl mx-auto">
            Rejoignez les 12 communes pilotes et les partenaires techniques qui alignent déjà leurs projets aux Objectifs de Développement Durable.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link href="/projets/creer" className="px-8 py-3 bg-white text-green-700 font-semibold rounded-lg hover:bg-green-50 transition-all shadow-lg">
              Commencer Maintenant
            </Link>
            <Link href="/aide" className="px-8 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white/10 transition-all">
              Support & FAQ
            </Link>
          </div>
        </div>
      </div>

      {/* INFO TIP */}
      <div className="p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-l-4 border-blue-500">
        <p className="text-sm text-gray-800 mb-3">
          <strong>💡 Conseil:</strong> Consultez <Link href="/projets" className="underline font-semibold text-blue-700 hover:text-blue-900">tous les projets</Link> pour des exemples d'alignement réussis, explorez la <Link href="/cartographie" className="underline font-semibold text-blue-700 hover:text-blue-900">cartographie interactive</Link> pour voir les initiatives dans votre région, ou accédez à la <Link href="/referentiel-odd" className="underline font-semibold text-blue-700 hover:text-blue-900">documentation ODD</Link> complète.
        </p>
      </div>

      {/* ALL ODD REFERENCE */}
      <div>
        <SectionTitle title="Les 17 Objectifs de Développement Durable" description="Référence complète de tous les ODD et leur contexte Camerounais" />
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-9 mt-6">
          {[
            { code: "01", label: "Pas de Pauvreté" },
            { code: "02", label: "Faim Zéro" },
            { code: "03", label: "Bonne Santé" },
            { code: "04", label: "Éducation de Qualité" },
            { code: "05", label: "Égalité des Genres" },
            { code: "06", label: "Eau Propre" },
            { code: "07", label: "Énergie Propre" },
            { code: "08", label: "Travail Décent" },
            { code: "09", label: "Innovation" },
            { code: "10", label: "Réduction des Inégalités" },
            { code: "11", label: "Villes Durables" },
            { code: "12", label: "Consommation Responsable" },
            { code: "13", label: "Climat" },
            { code: "14", label: "Vie Aquatique" },
            { code: "15", label: "Vie Terrestre" },
            { code: "16", label: "Paix & Justice" },
            { code: "17", label: "Partenariats" },
          ].map((odd) => (
            <div key={odd.code} className="rounded-lg border border-gray-200 bg-white p-3 text-center hover:border-amber-300 hover:shadow-md transition-all">
              <Badge label={`ODD ${odd.code}`} oddCode={odd.code} variant="solid" />
              <p className="text-xs text-gray-600 mt-2">{odd.label}</p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}

function QuickAccessCard({
  title,
  desc,
  href,
  color,
}: {
  title: string;
  desc: string;
  href: string;
  color: string;
}) {
  return (
    <Link href={href} className="block">
      <Card hoverable className="overflow-hidden transition">
        <div className={`bg-gradient-to-r ${color} to-transparent h-1 -m-6 mb-3`} />
        <h3 className="text-base font-semibold text-[color:var(--foreground)]">{title}</h3>
        <p className="mt-2 text-xs text-[color:var(--muted)] leading-relaxed">{desc}</p>
        <div className="mt-4 inline-flex items-center gap-2 text-xs font-medium text-[color:var(--primary)]">
          Accéder <span>→</span>
        </div>
      </Card>
    </Link>
  );
}
