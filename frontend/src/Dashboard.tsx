import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import GameLoading from "./GameLoading";
import { Link } from "react-router-dom";
import { apiRequest } from "./utils/apiClient";
import EmberlynMessage from "./components/EmberlynMessage";

interface DashboardProps {
  user: any;
}

export default function Dashboard({ user }: DashboardProps) {
  const [loading, setLoading] = useState(true);
  const [characters, setCharacters] = useState([]);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const data = await apiRequest({
          path: `/getuserdata`,
        });

        const loadedCharacters = data?.characters || [];
        setCharacters(loadedCharacters);
        console.log("Loaded characters:", loadedCharacters);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return <GameLoading />;
  }

  return (
    <div className="bg-primaryBackground min-h-screen text-[#3E2713] font-garamond">
      <NavBar user={user} />

      <div className="pt-24 px-6 max-w-6xl mx-auto flex justify-center">
        <EmberlynMessage title="Fairy Facts with Emberlyn">
          <ul className="list-disc list-inside text-base text-[#3E2713] space-y-2">
            {characters.length === 0 && (
              <li>
                Every journey needs a hero! Tap the magic below to conjure your
                very first character, and let the adventure begin!
              </li>
            )}
            {characters.length > 0 && characters.length < 5 && (
              <li>
                Another spark, another soul! You may summon up to five
                companions—go ahead, the realms are waiting...
              </li>
            )}
            {characters.length > 0 && (
              <li>
                A new tale or a chapter continued? Step into your Saga, brave
                one, and let the fire whisper once more.
              </li>
            )}
          </ul>
        </EmberlynMessage>
      </div>

      <div className="p-6 max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-10">
        {characters.map((char) => (
          <div
            key={char.character_id}
            className="bg-containerBackground rounded-2xl shadow-lg p-6 flex flex-col justify-between"
          >
            <div>
              <h2 className="text-2xl font-bold mb-2 text-center">
                {char.name}
              </h2>
              <p className="text-center text-lg">
                Level {char.level} {char.profession}
              </p>
            </div>

            <div className="mt-4 flex justify-center space-x-6">
              <Link
                to={`/character/${char.character_id}`}
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
              {char.active[0] ? (
                <Link
                  to={`/game/${char.active[0].game_id}`}
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
              ) : (
                <Link
                  to={`/createsaga/${char.character_id}`}
                  className="flex flex-col items-center text-[#3E2713] hover:text-orange-700 hover:scale-105 transition-transform"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-8 w-8 mb-1"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      d="M12 5v14m-7-7h14"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  <span className="text-sm font-medium">Start Saga</span>
                </Link>
              )}
            </div>
          </div>
        ))}

        {/* Fill remaining slots up to 5 */}
        {characters.length < 5 && (
          <Link
            to="/createcharacter"
            className="bg-containerBackground rounded-2xl shadow-lg p-6 flex items-center justify-center text-[#3E2713] hover:opacity-90 text-xl font-semibold"
          >
            + Create New Character
          </Link>
        )}
      </div>
    </div>
  );
}
