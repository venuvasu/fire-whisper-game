import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import NavBar from "./NavBar";
import { useAuth } from "./auth/AuthContext";
import { apiRequest } from "./utils/apiClient";
import EmberlynMessage from "./components/EmberlynMessage";

export default function CreateCharacter() {
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState(null);

  const [name, setName] = useState("");
  const [race, setRace] = useState("Human");
  const [gender, setGender] = useState("Male");
  const [profession, setProfession] = useState("Warrior");

  const navigate = useNavigate();
  const { user } = useAuth();

  const handleCreateCharacter = async () => {
    setCreating(true);
    setError(null);
    try {
      const data = await apiRequest({
        path: "/createcharacter",
        method: "POST",
        token: user.id_token,
        body: {
          name,
          race,
          gender,
          profession,
        },
      });

      console.log("Created character:", data);

      if (data.character_id) {
        navigate(`/character/${data.character_id}`);
      } else {
        throw new Error("Character ID missing in response.");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred.");
    } finally {
      setCreating(false);
    }
  };

  if (!user || user.expired) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-primaryBackground text-white font-serif">
        <p>You must be logged in to create a character.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-primaryBackground text-white font-garamond">
      <NavBar user={user} />

      <div className="flex flex-col items-center justify-center space-y-6 px-4 pt-16 w-full max-w-xl mx-auto">
        <EmberlynMessage title="Create your character!">
          <p>
            🌟 Time to breathe life into legend! Shape your hero below—choose
            their path, their spirit, and their spark. The world of Fire Whisper
            awaits your creation...
          </p>
        </EmberlynMessage>

        <div className="bg-containerBackground text-black rounded-2xl shadow-lg p-6 w-full max-w-6xl mx-auto">
          <div className="space-y-4">
            <div>
              <label className="block mb-1 font-semibold">Name</label>
              <input
                type="text"
                maxLength={50}
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
              />
            </div>

            <div>
              <label className="block mb-1 font-semibold">Race</label>
              <select
                value={race}
                onChange={(e) => setRace(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
              >
                <option>Human</option>
                <option>Elf</option>
                <option>Dwarf</option>
                <option>Halfling</option>
                <option>Orc</option>
                <option>Catfolk</option>
                <option>Lizardfolk</option>
                <option>Giant</option>
                <option>Goblin</option>
                <option>Centaur</option>
              </select>
            </div>

            <div>
              <label className="block mb-1 font-semibold">Gender</label>
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
              >
                <option>Male</option>
                <option>Female</option>
                <option>Transgender Male</option>
                <option>Transgender Female</option>
                <option>Non-Binary</option>
              </select>
            </div>

            <div>
              <label className="block mb-1 font-semibold">Profession</label>
              <select
                value={profession}
                onChange={(e) => setProfession(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
              >
                <option>Warrior</option>
                <option>Berserker</option>
                <option>Mage</option>
                <option>Druid</option>
                <option>Shaman</option>
                <option>Cleric</option>
                <option>Templar</option>
                <option>Assassin</option>
                <option>Thief</option>
                <option>Bard</option>
              </select>
            </div>
          </div>

          <button
            className="w-full mt-6 px-4 py-3 rounded-full bg-green-700 hover:bg-green-800 text-white font-semibold shadow-lg transition disabled:opacity-60"
            onClick={handleCreateCharacter}
            disabled={creating}
          >
            {creating ? "Creating..." : "Create Character"}
          </button>
        </div>

        {error && <div className="text-red-400 font-semibold">{error}</div>}
      </div>
    </div>
  );
}
