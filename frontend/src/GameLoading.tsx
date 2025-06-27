import React, { useState, useEffect } from "react";

const flavorTexts = [
  "Stoking the flames of adventure...",
  "Gathering kindling...",
  "Sharpening blades...",
  "Listening for wolves...",
  "Checking spell components...",
  "Brewing mead...",
  "Rolling for initiative...",
  "Warding the campsite...",
];

const GameLoading = () => {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % flavorTexts.length);
    }, 3000); // Rotate every 3 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-screen h-screen bg-[#0d0d0d] text-white flex flex-col justify-center items-center relative overflow-hidden font-serif">
      {/* Background image */}
      <picture>
        <source srcSet="/background-loading.webp" type="image/webp" />
        <img
          src="/background-loading.png"
          alt=""
          className="absolute inset-0 w-full h-full object-cover object-center opacity-20 blur-sm pointer-events-none"
          aria-hidden="true"
          style={{ zIndex: 0 }}
        />
      </picture>

      {/* Flickering emoji */}
      <div className="text-6xl animate-pulse z-10 mb-4">🔥</div>

      {/* Title */}
      <h1 className="text-4xl md:text-5xl font-bold text-amber-200 z-10">
        Fire Whisper
      </h1>

      {/* Rotating loading text */}
      <p className="mt-3 text-sm text-gray-300 italic z-10 transition-opacity duration-500">
        {flavorTexts[index]}
      </p>

      {/* Optional particle overlay */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="w-full h-full bg-[radial-gradient(circle,_rgba(255,153,51,0.1)_0%,_transparent_70%)] animate-pulse" />
      </div>
    </div>
  );
};

export default GameLoading;
