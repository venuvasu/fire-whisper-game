import React from "react";
import { GiMagicGate, GiSpellBook } from "react-icons/gi";
import { Link } from "react-router-dom";

const SectionHeader = ({ icon: Icon, title }) => (
  <div className="flex items-center text-2xl font-bold pb-1 mb-2">
    <Icon className="mr-2 text-[#3E2713]" size={28} />
    <span className="uppercase tracking-wide">{title}</span>
  </div>
);

const ActiveSagasSection = ({ activeGames }) => (
  <section>
    <SectionHeader icon={GiMagicGate} title="Active Sagas" />
    {activeGames && activeGames.length > 0 ? (
      <ul className="space-y-4">
        {activeGames.map((game) => (
          <li
            key={game.game_id}
            className="bg-[#EBDDCB] p-4 rounded-xl border border-[#D4C2A3] shadow"
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-xl font-bold text-[#3E2713]">
                  {game.game_name}
                </h3>
                <p className="text-sm italic text-[#3E2713]">
                  Turns taken: {game.message_count / 2}
                </p>
              </div>
              <Link
                to={`/game/${game.game_id}`}
                className="flex flex-col items-center text-[#3E2713] hover:text-orange-700 hover:scale-105 transition-transform"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-8 w-8 mb-1"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M8 5v14l11-7z" />
                </svg>
                <span className="text-sm font-medium">Continue Saga</span>
              </Link>
            </div>
          </li>
        ))}
      </ul>
    ) : (
      <p className="italic text-gray-600">No active sagas yet.</p>
    )}
  </section>
);

const CompletedSagasSection = ({ completedGames }) => (
  <section>
    <SectionHeader icon={GiSpellBook} title="Completed Sagas" />
    {completedGames && completedGames.length > 0 ? (
      <ul className="space-y-4">
        {completedGames.map((game) => (
          <li
            key={game.game_id}
            className="bg-[#EBDDCB] p-4 rounded-xl border border-[#D4C2A3] shadow"
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-xl font-bold text-[#3E2713]">
                  {game.game_name}
                </h3>
                <p className="text-sm italic text-[#3E2713]">
                  Turns taken: {game.message_count / 2}
                </p>
              </div>
              <Link
                to={`/game/${game.game_id}`}
                className="flex flex-col items-center text-[#3E2713] hover:text-orange-700 hover:scale-105 transition-transform"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-8 w-8 mb-1"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M8 5v14l11-7z" />
                </svg>
                <span className="text-sm font-medium">Review Saga</span>
              </Link>
            </div>
          </li>
        ))}
      </ul>
    ) : (
      <p className="italic text-gray-600">No completed sagas yet.</p>
    )}
  </section>
);

const SagasSection = ({ activeGames, completedGames }) => (
  <div className="space-y-10">
    <ActiveSagasSection activeGames={activeGames} />
    <CompletedSagasSection completedGames={completedGames} />
  </div>
);

export default SagasSection;
