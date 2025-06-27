import React from "react";
import { GiBackpack } from "react-icons/gi";

const SectionHeader = ({ icon: Icon, title }) => (
  <div className="flex items-center text-2xl font-bold pb-1 mb-2">
    <Icon className="mr-2 text-[#3E2713]" size={28} />
    <span className="uppercase tracking-wide">{title}</span>
  </div>
);

const CurrencyDisplay = ({ currency }) => (
  <p>
    <strong>Currency:</strong> {currency} gold
  </p>
);

const CarriedItemsList = ({ carriedItems }) => {
  if (!carriedItems || carriedItems.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold text-[#3E2713]">Carried Items</h3>
      {carriedItems.map((item, index) => (
        <p key={index} className="ml-4">
          <strong>{item.name}</strong> (x{item.quantity}): {item.description}
        </p>
      ))}
    </div>
  );
};

const ConsumablesList = ({ consumables }) => {
  if (!consumables || consumables.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold text-[#3E2713]">Consumables</h3>
      {consumables.map((consumable, index) => (
        <p key={index} className="ml-4">
          <strong>{consumable.name}</strong> (x{consumable.quantity}):{" "}
          {consumable.effect}
        </p>
      ))}
    </div>
  );
};

const QuestItemsList = ({ questItems }) => {
  if (!questItems || questItems.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold text-[#3E2713]">Quest Items</h3>
      {questItems.map((questItem, index) => (
        <p key={index} className="ml-4">
          <strong>{questItem.name}</strong> (Quest: {questItem.quest}):{" "}
          {questItem.description}
        </p>
      ))}
    </div>
  );
};

const InventorySection = ({ inventory }) => {
  if (!inventory) return null;

  return (
    <section>
      <SectionHeader icon={GiBackpack} title="Inventory" />
      <div className="space-y-4">
        <CurrencyDisplay currency={inventory.currency} />
        <CarriedItemsList carriedItems={inventory.carriedItems} />
        <ConsumablesList consumables={inventory.consumables} />
        <QuestItemsList questItems={inventory.questItems} />
      </div>
    </section>
  );
};

export default InventorySection;
