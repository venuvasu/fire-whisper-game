import React from "react";
import { GiThreeFriends } from "react-icons/gi";

const SectionHeader = ({ icon: Icon, title }) => (
  <div className="flex items-center text-2xl font-bold pb-1 mb-2">
    <Icon className="mr-2 text-[#3E2713]" size={28} />
    <span className="uppercase tracking-wide">{title}</span>
  </div>
);

const RelationshipMeter = ({ value, max = 100 }) => {
  const getColorClass = (value) => {
    if (value === 0) return "text-gray-600";
    return value > 0 ? "text-green-600" : "text-red-600";
  };

  const formatValue = (value) => {
    if (value === undefined || value === null) return "—";
    return value.toString();
  };

  return (
    <span className={`ml-2 font-semibold ${getColorClass(value)}`}>
      (Standing: {formatValue(value)}/{max})
    </span>
  );
};

const CompanionBond = ({ bond }) => (
  <p>
    <strong>Bond with Emberlyn:</strong> <RelationshipMeter value={bond} />
  </p>
);

const PeopleList = ({ people }) => {
  if (!people || people.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold text-[#3E2713]">People</h3>
      {people.map((person, index) => (
        <p key={index} className="ml-4">
          <strong>{person.name}</strong>
          <RelationshipMeter value={person.standing} />
          {person.notes && (
            <span className="text-gray-600"> - {person.notes}</span>
          )}
        </p>
      ))}
    </div>
  );
};

const FactionsList = ({ factions }) => {
  if (!factions || factions.length === 0) return null;

  return (
    <div>
      <h3 className="mt-4 font-bold text-[#3E2713]">Faction Standing</h3>
      {factions.map((faction, index) => (
        <p key={index} className="ml-4">
          <strong>{faction.name}</strong>
          <RelationshipMeter value={faction.standing} />
          {faction.notes && (
            <span className="text-gray-600"> - {faction.notes}</span>
          )}
        </p>
      ))}
    </div>
  );
};

const RelationshipsSection = ({ relationships }) => {
  if (!relationships) return null;

  return (
    <section>
      <SectionHeader icon={GiThreeFriends} title="Relationships" />
      <div className="space-y-4">
        <CompanionBond bond={relationships.companionBond} />
        <PeopleList people={relationships.people} />
        <FactionsList factions={relationships.factions} />
      </div>
    </section>
  );
};

export default RelationshipsSection;
