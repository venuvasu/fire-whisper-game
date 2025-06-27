import React from "react";
import { GiMagicGate } from "react-icons/gi";

const SectionHeader = ({ icon: Icon, title }) => (
  <div className="flex items-center text-2xl font-bold pb-1 mb-2">
    <Icon className="mr-2 text-[#3E2713]" size={28} />
    <span className="uppercase tracking-wide">{title}</span>
  </div>
);

const SkillsList = ({ skills }) => {
  if (!skills || skills.length === 0) return null;

  return (
    <div>
      {skills.map((skill, index) => (
        <p key={index}>
          <strong>{skill.name}</strong> ({skill.proficiency}):{" "}
          {skill.description}
        </p>
      ))}
    </div>
  );
};

const TalentsList = ({ talents }) => {
  if (!talents || talents.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold">Talents</h3>
      {talents.map((talent, index) => (
        <p key={index}>
          <strong>{talent.name}</strong> – {talent.description} (Cooldown:{" "}
          {talent.cooldown})
        </p>
      ))}
    </div>
  );
};

const SpellsTechniquesList = ({ spellsTechniques }) => {
  if (!spellsTechniques || spellsTechniques.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold">Spells & Techniques</h3>
      {spellsTechniques.map((st, index) => (
        <p key={index}>
          <strong>{st.name}</strong> [{st.type}, {st.energyCost} energy]:{" "}
          {st.effect}
        </p>
      ))}
    </div>
  );
};

const PassiveAbilitiesList = ({ passiveAbilities }) => {
  if (!passiveAbilities || passiveAbilities.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold">Passives</h3>
      {passiveAbilities.map((passive, index) => (
        <p key={index}>
          <strong>{passive.name}</strong>: {passive.effect}
        </p>
      ))}
    </div>
  );
};

const CapabilitiesSection = ({ capabilities }) => {
  if (!capabilities) return null;

  return (
    <section>
      <SectionHeader icon={GiMagicGate} title="Capabilities" />
      <div className="space-y-2">
        <SkillsList skills={capabilities.skills} />
        <TalentsList talents={capabilities.talents} />
        <SpellsTechniquesList
          spellsTechniques={capabilities.spellsTechniques}
        />
        <PassiveAbilitiesList
          passiveAbilities={capabilities.passiveAbilities}
        />
      </div>
    </section>
  );
};

export default CapabilitiesSection;
