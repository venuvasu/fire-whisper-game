import React, { useState } from "react";

const IdentityHeaderSection = ({ identity, progression }) => {
  const buildImagePath = (identity) =>
    `/stock/characters/${identity.race
      .toLowerCase()
      .replace(/\s+/g, "")}/${identity.profession
      .toLowerCase()
      .replace(/\s+/g, "")}/${identity.gender
      .toLowerCase()
      .replace(/\s+/g, "")}.webp`;

  const [imgSrc, setImgSrc] = useState(buildImagePath(identity));

  const fallbackImage = "/logo-transparent.png";

  const handleImageError = (e) => {
    if (imgSrc !== fallbackImage) {
      setImgSrc(fallbackImage);
    }
  };

  return (
    <div className="flex gap-2 sm:gap-4 items-stretch">
      <div className="flex items-center justify-center min-w-[96px] sm:min-w-[112px] flex-shrink-0">
        <img
          src={imgSrc}
          alt={`${identity.name}'s avatar`}
          className="w-24 h-24 sm:w-28 sm:h-28 object-contain rounded-md"
          onError={handleImageError}
        />
      </div>
      <div className="flex flex-col justify-center min-w-0 flex-1">
        <h1 className="text-2xl sm:text-4xl lg:text-5xl font-extrabold tracking-wide text-[#3E2713] drop-shadow-md leading-tight break-words">
          {identity.name}
        </h1>
        <p className="italic text-sm sm:text-lg lg:text-xl text-[#6B4A2F] leading-snug mb-2 break-words">
          {identity.race} {identity.profession} ({identity.gender})
        </p>
        <div className="flex gap-4 sm:gap-6 text-[#3E2713] text-xs sm:text-sm font-medium italic flex-wrap">
          <span>Level {progression.level}</span>
          <span>XP: {progression.experience}</span>
        </div>
      </div>
    </div>
  );
};

export default IdentityHeaderSection;
