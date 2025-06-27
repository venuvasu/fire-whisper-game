import React from "react";
import { GiSpellBook } from "react-icons/gi";

const SectionHeader = ({ icon: Icon, title }) => (
  <div className="flex items-center text-2xl font-bold pb-1 mb-2">
    <Icon className="mr-2 text-[#3E2713]" size={28} />
    <span className="uppercase tracking-wide">{title}</span>
  </div>
);

const AttributeCard = ({ name, value }) => {
  const shortName = name.slice(0, 3).toUpperCase();
  return (
    <div className="bg-[#EBDDCB] p-2 rounded shadow-inner border border-[#D4C2A3]">
      <p className="font-semibold capitalize block sm:hidden">{shortName}</p>
      <p className="font-semibold capitalize hidden sm:block">{name}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
};

const AttributesSection = ({ attributes }) => {
  if (!attributes) return null;

  return (
    <section>
      <SectionHeader icon={GiSpellBook} title="Attributes" />
      <div className="grid grid-cols-3 gap-4 text-center">
        <AttributeCard name="Strength" value={attributes.strength} />
        <AttributeCard name="Dexterity" value={attributes.dexterity} />
        <AttributeCard name="Constitution" value={attributes.constitution} />
        <AttributeCard name="Intelligence" value={attributes.intelligence} />
        <AttributeCard name="Wisdom" value={attributes.wisdom} />
        <AttributeCard name="Charisma" value={attributes.charisma} />
      </div>
    </section>
  );
};

export default AttributesSection;
