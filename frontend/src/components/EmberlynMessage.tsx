import React, { ReactNode } from "react";

interface EmberlynMessageProps {
  title: string;
  children: ReactNode;
  className?: string;
}

const EmberlynMessage: React.FC<EmberlynMessageProps> = ({
  title,
  children,
  className = "",
}) => {
  return (
    <div
      className={`bg-containerBackground text-primaryText rounded-2xl shadow-lg p-6 w-full max-w-6xl mx-auto flex flex-col sm:flex-row items-center gap-2 ${className}`}
    >
      <picture>
        <source srcSet="/emberlyn.webp" type="image/webp" />
        <img
          src="/emberlyn.png"
          alt="Emberlyn the Fairy"
          className="w-24 h-24 sm:w-auto sm:h-[90%] sm:max-h-40 object-contain mb-4 sm:mb-0 sm:mr-8"
        />
      </picture>
      <div className="flex flex-col justify-center items-center sm:items-start text-center sm:text-left">
        <h2 className="text-2xl font-bold mb-2">{title}</h2>
        {children}
      </div>
    </div>
  );
};

export default EmberlynMessage;
