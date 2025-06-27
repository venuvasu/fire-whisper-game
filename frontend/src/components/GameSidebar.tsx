import React from "react";
import { Link } from "react-router-dom";
import { FiChevronLeft, FiChevronRight } from "react-icons/fi";

interface GameSidebarProps {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  gameData: any;
}

const GameSidebar: React.FC<GameSidebarProps> = ({
  sidebarOpen,
  toggleSidebar,
  gameData,
}) => {
  return (
    <>
      {/* Mobile toggle button when sidebar is closed */}
      {!sidebarOpen && (
        <button
          id="sidebar-toggle-mobile"
          className="fixed top-20 left-4 z-50 p-2 bg-[#EBDDCB] border border-[#3E2713] rounded-md shadow-lg text-[#3E2713] hover:bg-[#3E2713] hover:bg-opacity-10 transition-colors sm:hidden"
          onClick={toggleSidebar}
        >
          <FiChevronRight />
        </button>
      )}

      <div
        id="game-sidebar"
        className={`
          transition-all duration-300 bg-[#EBDDCB] border-r border-[#3E2713] 
          flex flex-col items-start pt-4
          
          /* Desktop: normal sidebar behavior */
          sm:relative ${sidebarOpen ? "sm:w-64" : "sm:w-12"} sm:transform-none
          
          /* Mobile: fixed positioning with slide animation */
          fixed sm:static
          top-16 left-0
          w-64 h-[calc(100vh-4rem)] sm:h-auto
          z-40
          
          /* Mobile slide animation */
          transform transition-transform duration-300 ease-in-out
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}
          sm:translate-x-0
          
          ${sidebarOpen ? "" : "overflow-hidden"}
        `}
      >
        <button
          id="sidebar-toggle"
          className="p-2 ml-auto mr-2 text-[#3E2713] hover:bg-[#3E2713] hover:bg-opacity-10 rounded transition-colors"
          onClick={toggleSidebar}
        >
          {sidebarOpen ? <FiChevronLeft /> : <FiChevronRight />}
        </button>

        {sidebarOpen && (
          <div className="p-4 w-full overflow-y-auto">
            <div className="flex justify-center mb-4">
              <picture>
                <source srcSet="/emberlyn.webp" type="image/webp" />
                <img
                  src="/emberlyn.png"
                  alt="Emberlyn the Fairy"
                  className="w-20 h-20 object-contain rounded-full shadow"
                />
              </picture>
            </div>

            <div className="bg-containerBackground rounded-2xl shadow-lg p-6 flex flex-col justify-between">
              <div className="text-xl font-bold">{gameData?.game_name}</div>
              <div className="mt-2 text-sm text-[#3E2713] font-medium">
                Turns taken:{" "}
                {Array.isArray(gameData?.messages)
                  ? Math.floor(gameData.messages.length / 2)
                  : 0}
              </div>
            </div>

            <div className="h-4" />

            <div className="bg-containerBackground rounded-2xl shadow-lg p-6 flex flex-col justify-between">
              <div>
                <h2 className="text-2xl font-bold mb-2 text-center">
                  {gameData?.character_profile?.name}
                </h2>
                <p className="text-center text-lg">
                  Level {gameData?.character_profile?.level}{" "}
                  {gameData?.character_profile?.profession}
                </p>
                <div className="flex justify-center mt-2">
                  <Link
                    to={`/character/${gameData?.character_profile?.character_id}`}
                    className="flex flex-col items-center text-[#3E2713] hover:text-orange-700 hover:scale-105 transition-transform"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-8 w-8 mb-1"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path d="M5 4h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm0 2v12h14V6H5zm7 2a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm0 3c1.38 0 2.5 1.12 2.5 2.5S13.38 16 12 16s-2.5-1.12-2.5-2.5S10.62 11 12 11z" />
                    </svg>
                    <span className="text-sm font-medium">Character Sheet</span>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default GameSidebar;
