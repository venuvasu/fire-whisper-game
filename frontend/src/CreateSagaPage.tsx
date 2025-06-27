import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import NavBar from "./NavBar";
import { useAuth } from "./auth/AuthContext";
import { apiRequest } from "./utils/apiClient";
import EmberlynMessage from "./components/EmberlynMessage";

export default function CreateSagaPage() {
  const { characterId } = useParams();
  const navigate = useNavigate();

  const [setting, setSetting] = useState("Norse");
  const [difficulty, setDifficulty] = useState("Story");

  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { user } = useAuth();

  useEffect(() => {
    if (!characterId) {
      navigate("/");
    }
  }, [characterId, navigate]);

  const handleCreateSaga = async () => {
    setCreating(true);
    setError(null);

    try {
      const data = await apiRequest({
        path: "/createsaga",
        method: "POST",
        token: user.id_token,
        body: {
          characterId,
          setting,
          difficulty,
        },
      });

      const gameId = data.game_id || data.gameId;
      if (gameId) {
        navigate(`/game/${gameId}`);
      } else {
        throw new Error("No game ID returned.");
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-primaryBackground text-white font-garamond">
      <NavBar user={user} />

      <div className="flex flex-col items-center justify-center space-y-6 px-4 pt-16 w-full max-w-xl mx-auto">
        <EmberlynMessage title="Forge Your Saga!">
          <p>
            🌟 Choose the fields below wisely, dear adventurer, and weave the
            first threads of your Saga. Every great story in Fire Whisper begins
            with a single spark...
          </p>
        </EmberlynMessage>

        <div className="bg-containerBackground text-black rounded-2xl shadow-lg p-6 w-full max-w-6xl mx-auto">
          <div className="space-y-4">
            <div>
              <label className="block mb-1 font-semibold">
                Choose a Setting
              </label>
              <select
                value={setting}
                onChange={(e) => setSetting(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
              >
                <option value="Norse">
                  Norse Mythology – Frost giants and ancient gods
                </option>
                <option value="Greek">
                  Greek Legends – Heroes and mighty Olympians
                </option>
                <option value="Medieval">
                  Medieval Fantasy – Knights, wizards, and dragons
                </option>
                <option value="Egyptian">
                  Egyptian Mythology – Pharaohs, gods, and ancient mysteries
                </option>
                <option value="Celtic">
                  Celtic Mythology – Druids, fae folk, and mystical forests
                </option>
                <option value="Arabian">
                  Arabian Nights – Genies, sultans, and desert magic
                </option>
                <option value="Chinese">
                  Chinese Mythology – Dragons, immortals, and celestial courts
                </option>
              </select>
            </div>

            <div>
              <label className="block mb-1 font-semibold">Difficulty</label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
              >
                <option value="Story">
                  Story – Focus on narrative and exploration
                </option>
                <option value="Adventurer">
                  Adventurer – Balanced with moderate risk
                </option>
                <option value="Hero">
                  Hero’s Journey – Strategic challenges
                </option>
              </select>
            </div>
          </div>

          <button
            className="w-full mt-6 px-4 py-3 rounded-full bg-green-700 hover:bg-green-800 text-white font-semibold shadow-lg transition disabled:opacity-60"
            onClick={handleCreateSaga}
            disabled={creating}
          >
            {creating ? "Creating..." : "Create Your Saga"}
          </button>
        </div>

        {error && <div className="text-red-400 font-semibold">{error}</div>}
      </div>
    </div>
  );
}
