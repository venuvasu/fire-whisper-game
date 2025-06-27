import React from "react";
import { GiFurnace } from "react-icons/gi";

const SectionHeader = ({ icon: Icon, title }) => (
  <div className="flex items-center text-2xl font-bold pb-1 mb-2">
    <Icon className="mr-2 text-[#3E2713]" size={28} />
    <span className="uppercase tracking-wide">{title}</span>
  </div>
);

const CraftingAbilitiesDisplay = ({ craftingAbilities }) => {
  const displayValue =
    craftingAbilities && craftingAbilities.length > 0
      ? craftingAbilities.join(", ")
      : "None";

  return (
    <p>
      <strong>Crafting Abilities:</strong> {displayValue}
    </p>
  );
};

const KnowledgeAreasDisplay = ({ knowledgeAreas }) => {
  const displayValue =
    knowledgeAreas && knowledgeAreas.length > 0
      ? knowledgeAreas.join(", ")
      : "None";

  return (
    <p>
      <strong>Knowledge Areas:</strong> {displayValue}
    </p>
  );
};

const CulturalTraitsDisplay = ({ culturalTraits }) => {
  const displayValue =
    culturalTraits && culturalTraits.length > 0
      ? culturalTraits.join(", ")
      : "None";

  return (
    <p>
      <strong>Cultural Traits:</strong> {displayValue}
    </p>
  );
};

const KnowledgeSection = ({ additional }) => {
  if (!additional) return null;

  return (
    <section>
      <SectionHeader icon={GiFurnace} title="Knowledge" />
      <div className="space-y-2">
        <CraftingAbilitiesDisplay
          craftingAbilities={additional.craftingAbilities}
        />
        <KnowledgeAreasDisplay knowledgeAreas={additional.knowledgeAreas} />
        <CulturalTraitsDisplay culturalTraits={additional.culturalTraits} />
      </div>
    </section>
  );
};

export default KnowledgeSection;
