import React from "react";

const VitalitySection = ({ vitality }) => {
  return (
    <div className="flex gap-4">
      <div className="bg-[#EBDDCB] border-4 border-[#3E2713] rounded-xl shadow-md px-6 py-5 text-center w-36">
        <p className="font-bold text-lg text-[#3E2713] mb-1">Hit Points</p>
        <p className="text-3xl font-extrabold text-red-600 leading-snug">
          {vitality.hitPoints}
        </p>
        <p className="text-sm text-[#3E2713] italic">
          (Max {vitality.maxHitPoints})
        </p>
      </div>
      <div className="bg-[#EBDDCB] border-4 border-[#3E2713] rounded-xl shadow-md px-6 py-5 text-center w-36">
        <p className="font-bold text-lg text-[#3E2713] mb-1">Mana</p>
        <p className="text-3xl font-extrabold text-blue-600 leading-snug">
          {vitality.mana}
        </p>
        <p className="text-sm text-[#3E2713] italic">
          (Max {vitality.maxMana})
        </p>
      </div>
    </div>
  );
};

export default VitalitySection;
