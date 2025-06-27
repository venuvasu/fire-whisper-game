import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import { useParams } from "react-router-dom";
import GameLoading from "./GameLoading";
import { useAuth } from "./auth/AuthContext";
import { apiRequest } from "./utils/apiClient";
import RelationshipsSection from "./components/charactersheet/RelationshipsSection";
import EquipmentSection from "./components/charactersheet/EquipmentSection";
import InventorySection from "./components/charactersheet/InventorySection";
import AttributesSection from "./components/charactersheet/AttributesSection";
import KnowledgeSection from "./components/charactersheet/KnowledgeSection";
import IdentitySection from "./components/charactersheet/IdentitySection";
import CapabilitiesSection from "./components/charactersheet/CapabilitiesSection";
import SagasSection from "./components/charactersheet/SagasSection";
import DeleteCharacterSection from "./components/charactersheet/DeleteCharacterSection";
import VitalitySection from "./components/charactersheet/VitalitySection";
import IdentityHeaderSection from "./components/charactersheet/IdentityHeaderSection";

const TabButton = ({ tabName, activeTab, setActiveTab, children }) => (
  <button
    className={`text-xl pb-2 transition-transform transform hover:scale-105 hover:text-orange-700 ${
      activeTab === tabName
        ? "font-extrabold drop-shadow-sm border-b-4 border-[#3E2713] text-[#3E2713]"
        : "text-gray-500"
    }`}
    onClick={() => setActiveTab(tabName)}
  >
    {children}
  </button>
);

const CharacterPage = () => {
  const { characterId } = useParams();
  const [loading, setLoading] = useState(true);
  const [character, setCharacter] = useState(null);
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState("Info");

  useEffect(() => {
    const fetchCharacter = async () => {
      if (!characterId) return;

      try {
        const data = await apiRequest({
          path: `/getcharacter?character_id=${characterId}`,
        });

        console.log(data);
        setCharacter(data);
      } catch (err) {
        setCharacter(null);
      } finally {
        setLoading(false);
      }
    };
    if (user) fetchCharacter();
  }, [characterId]);

  if (loading) return <GameLoading />;

  return (
    <div className="bg-primaryBackground min-h-screen p-6 font-garamond text-[#2D2A26] bg-texture bg-fixed">
      <NavBar user={user} />
      <div className="max-w-5xl mx-auto bg-containerBackground rounded-3xl shadow-xl p-10 mt-20">
        <div className="space-y-4">
          <div className="flex justify-between items-center flex-wrap gap-4">
            <IdentityHeaderSection
              identity={character.IDENTITY}
              progression={character.PROGRESSION}
            />

            <VitalitySection vitality={character.VITALITY} />
          </div>

          <div className="border-b border-[#3E2713]">
            <nav className="-mb-px flex space-x-6">
              <TabButton
                tabName="Info"
                activeTab={activeTab}
                setActiveTab={setActiveTab}
              >
                Info
              </TabButton>
              <TabButton
                tabName="Gear"
                activeTab={activeTab}
                setActiveTab={setActiveTab}
              >
                Gear
              </TabButton>
              <TabButton
                tabName="Relationships"
                activeTab={activeTab}
                setActiveTab={setActiveTab}
              >
                <span className="hidden sm:inline">Relationships</span>
                <span className="sm:hidden">Rel.</span>
              </TabButton>
              <TabButton
                tabName="Sagas"
                activeTab={activeTab}
                setActiveTab={setActiveTab}
              >
                Sagas
              </TabButton>
            </nav>
          </div>

          <div className="pt-4">
            {activeTab === "Info" && (
              <div className="space-y-8">
                <AttributesSection attributes={character.ATTRIBUTES} />

                <IdentitySection identity={character.IDENTITY} />

                <CapabilitiesSection capabilities={character.CAPABILITIES} />

                <KnowledgeSection additional={character.ADDITIONAL} />

                <DeleteCharacterSection
                  character={character}
                  characterId={characterId}
                />
              </div>
            )}
            {activeTab === "Gear" && (
              <div className="space-y-8">
                <EquipmentSection equipment={character.EQUIPMENT} />

                <InventorySection inventory={character.INVENTORY} />
              </div>
            )}
            {activeTab === "Relationships" && (
              <RelationshipsSection relationships={character.RELATIONSHIPS} />
            )}
            {activeTab === "Sagas" && (
              <SagasSection
                activeGames={character.active_games}
                completedGames={character.completed_games}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CharacterPage;
