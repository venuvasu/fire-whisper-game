import React from "react";
import { GiBackpack } from "react-icons/gi";

const SectionHeader = ({ icon: Icon, title }) => (
  <div className="flex items-center text-2xl font-bold pb-1 mb-2">
    <Icon className="mr-2 text-[#3E2713]" size={28} />
    <span className="uppercase tracking-wide">{title}</span>
  </div>
);

const WeaponDisplay = ({ weapon }) => {
  if (!weapon) return null;

  return (
    <p>
      <strong>Weapon:</strong> {weapon.name} – {weapon.effect} (DMG:{" "}
      {weapon.damage}, Durability: {weapon.durability})
    </p>
  );
};

const ArmorDisplay = ({ armor }) => {
  if (!armor) return null;

  return (
    <p>
      <strong>Armor:</strong> {armor.name} (Protection: {armor.protection},
      Durability: {armor.durability})
    </p>
  );
};

const AccessoriesList = ({ accessories }) => {
  if (!accessories || accessories.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold text-[#3E2713]">Accessories</h3>
      {accessories.map((accessory, index) => (
        <p key={index} className="ml-4">
          <strong>{accessory.name}</strong>: {accessory.effect}
        </p>
      ))}
    </div>
  );
};

const ToolsList = ({ tools }) => {
  if (!tools || tools.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold text-[#3E2713]">Tools</h3>
      {tools.map((tool, index) => (
        <p key={index} className="ml-4">
          <strong>{tool.name}</strong>: {tool.use}
        </p>
      ))}
    </div>
  );
};

const MagicalItemsList = ({ magicalItems }) => {
  if (!magicalItems || magicalItems.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold text-[#3E2713]">Magical Items</h3>
      {magicalItems.map((item, index) => (
        <p key={index} className="ml-4">
          <strong>{item.name}</strong>: {item.power}
          {item.charges > 0 && (
            <span className="text-blue-600 font-semibold">
              {" "}
              (Charges: {item.charges})
            </span>
          )}
        </p>
      ))}
    </div>
  );
};

const EquipmentSection = ({ equipment }) => {
  if (!equipment) return null;

  return (
    <section>
      <SectionHeader icon={GiBackpack} title="Equipment" />
      <div className="space-y-4">
        <WeaponDisplay weapon={equipment.weapon} />
        <ArmorDisplay armor={equipment.armor} />
        <AccessoriesList accessories={equipment.accessories} />
        <ToolsList tools={equipment.tools} />
        <MagicalItemsList magicalItems={equipment.magicalItems} />
      </div>
    </section>
  );
};

export default EquipmentSection;
