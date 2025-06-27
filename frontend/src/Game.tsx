import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NavBar from "./NavBar";
import GameLoading from "./GameLoading";
import { useAuth } from "./auth/AuthContext";
import { apiRequest } from "./utils/apiClient";
import GameSidebar from "./components/GameSidebar";
import GameChat from "./components/GameChat";

const Game: React.FC = () => {
  const { gameid } = useParams<{ gameid: string }>();
  const [loading, setLoading] = useState(true);
  const [gameData, setGameData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    if (typeof window !== "undefined") {
      return window.innerWidth >= 640;
    }
    return false;
  });

  const { user } = useAuth();

  // Close sidebar when clicking outside on mobile
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 640) {
        setSidebarOpen(true);
      } else {
        setSidebarOpen(false);
      }
    };

    const handleClickOutside = (event: MouseEvent) => {
      if (window.innerWidth < 640 && sidebarOpen) {
        const sidebar = document.getElementById("game-sidebar");
        const toggleButton = document.getElementById("sidebar-toggle");

        if (
          sidebar &&
          !sidebar.contains(event.target as Node) &&
          toggleButton &&
          !toggleButton.contains(event.target as Node)
        ) {
          setSidebarOpen(false);
        }
      }
    };

    window.addEventListener("resize", handleResize);
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      window.removeEventListener("resize", handleResize);
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [sidebarOpen]);

  useEffect(() => {
    let isMounted = true;

    const fetchGame = async () => {
      if (!gameid) return;

      try {
        const data = await apiRequest({
          path: `/getgame?game_id=${gameid}`,
        });

        console.log("Game data:", data);
        if (isMounted) setGameData(data);
      } catch (err) {
        if (isMounted) setError((err as Error).message);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchGame();

    return () => {
      isMounted = false;
    };
  }, [gameid]);

  const handleSend = async () => {
    if (!input.trim() || sending) return;
    setSending(true);
    setError(null);

    setGameData((prev: any) => {
      if (!prev) return prev;
      return {
        ...prev,
        messages: [...(prev.messages || []), input],
      };
    });

    try {
      const data = await apiRequest({
        path: "/taketurn",
        method: "POST",
        token: user.id_token,
        body: {
          game_id: gameid,
          message: input,
        },
      });

      setGameData(data);
      setInput("");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  };

  if (loading) return <GameLoading />;

  if (error)
    return (
      <div className="p-8 bg-containerBackground min-h-screen text-[#3E2713]">
        <NavBar user={user} />
        <h1 className="text-2xl font-bold mb-4">Game Page</h1>
        <p className="text-red-400">Error: {error}</p>
      </div>
    );

  return (
    <div className="bg-containerBackground text-[#3E2713] h-screen flex flex-col overflow-hidden text-sm">
      <div className="flex-shrink-0">
        <NavBar user={user} />
      </div>

      <div className="flex flex-1 overflow-hidden pt-16 relative">
        {/* Overlay for mobile when sidebar is open */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black bg-opacity-50 z-30 sm:hidden top-16"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        <GameSidebar
          sidebarOpen={sidebarOpen}
          toggleSidebar={() => setSidebarOpen((prev) => !prev)}
          gameData={gameData}
        />

        <GameChat
          messages={gameData?.messages || []}
          gameActive={gameData?.game_active}
          input={input}
          onInputChange={setInput}
          onSend={handleSend}
          sending={sending}
          sidebarOpen={sidebarOpen}
        />
      </div>
    </div>
  );
};

export default Game;
