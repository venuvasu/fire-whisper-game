import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { apiRequest } from "../utils/apiClient";
import NavBar from "../NavBar";

interface Character {
  name: string;
  class: string;
  background: string;
  description: string;
}

interface Saga {
  name: string;
  description: string;
  difficulty: string;
}

const BillionDollarGameCreator: React.FC = () => {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [sagas, setSagas] = useState<Saga[]>([]);
  const [selectedCharacter, setSelectedCharacter] = useState<string>("");
  const [selectedSaga, setSelectedSaga] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [charactersData, sagasData] = await Promise.all([
          apiRequest({ path: "/characters" }),
          apiRequest({ path: "/sagas" })
        ]);
        
        setCharacters(charactersData.characters || []);
        setSagas(sagasData.sagas || []);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleCreateGame = async () => {
    if (!selectedCharacter || !selectedSaga) {
      setError("Please select both a character and a saga");
      return;
    }

    setCreating(true);
    setError(null);

    try {
      const response = await apiRequest({
        path: "/creategame",
        method: "POST",
        token: user.id_token,
        body: {
          character: selectedCharacter,
          saga: selectedSaga
        }
      });

      // Navigate to the new game
      navigate(`/game/${response.game_id}`);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setCreating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-white border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-white text-xl">Loading game data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-3/4 right-1/4 w-64 h-64 bg-orange-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
      </div>

      <NavBar user={user} />
      
      <div className="relative z-10 pt-24 pb-12">
        <div className="max-w-4xl mx-auto px-4">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">
              🔥 Create Your Epic Adventure
            </h1>
            <p className="text-xl text-gray-300">
              Choose your character and saga to begin your billion dollar journey
            </p>
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-4 mb-8">
              <p className="text-red-200 text-center">{error}</p>
            </div>
          )}

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Character Selection */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-6 text-center">
                🧙‍♂️ Choose Your Character
              </h2>
              <div className="space-y-4">
                {characters.map((character) => (
                  <div
                    key={character.name}
                    className={`p-4 rounded-xl cursor-pointer transition-all transform hover:scale-105 ${
                      selectedCharacter === character.name
                        ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                        : 'bg-white/10 hover:bg-white/20 text-gray-200'
                    }`}
                    onClick={() => setSelectedCharacter(character.name)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-bold text-lg">{character.name}</h3>
                      <span className="text-sm opacity-75">{character.class}</span>
                    </div>
                    <p className="text-sm opacity-90 mb-2">{character.background}</p>
                    <p className="text-xs opacity-75">{character.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Saga Selection */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-6 text-center">
                📚 Choose Your Saga
              </h2>
              <div className="space-y-4">
                {sagas.map((saga) => (
                  <div
                    key={saga.name}
                    className={`p-4 rounded-xl cursor-pointer transition-all transform hover:scale-105 ${
                      selectedSaga === saga.name
                        ? 'bg-gradient-to-r from-orange-500 to-red-600 text-white shadow-lg'
                        : 'bg-white/10 hover:bg-white/20 text-gray-200'
                    }`}
                    onClick={() => setSelectedSaga(saga.name)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-bold text-lg">{saga.name}</h3>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        saga.difficulty === 'Easy' ? 'bg-green-500' :
                        saga.difficulty === 'Medium' ? 'bg-yellow-500' : 'bg-red-500'
                      }`}>
                        {saga.difficulty}
                      </span>
                    </div>
                    <p className="text-sm opacity-90">{saga.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Create Game Button */}
          <div className="text-center">
            <button
              onClick={handleCreateGame}
              disabled={creating || !selectedCharacter || !selectedSaga}
              className="bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 disabled:from-gray-500 disabled:to-gray-600 text-white px-12 py-4 rounded-2xl font-bold text-xl transition-all transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed shadow-2xl"
            >
              {creating ? (
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Creating Your Adventure...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-3">
                  <span>🚀 Start Epic Adventure</span>
                </div>
              )}
            </button>
            
            {selectedCharacter && selectedSaga && (
              <p className="text-gray-300 mt-4">
                Ready to begin as <strong>{selectedCharacter}</strong> in the <strong>{selectedSaga}</strong> saga!
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BillionDollarGameCreator;