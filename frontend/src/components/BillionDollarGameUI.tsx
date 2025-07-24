import React, { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import NavBar from "../NavBar";
import GameLoading from "../GameLoading";
import { useAuth } from "../auth/AuthContext";
import { apiRequest } from "../utils/apiClient";

interface GameMessage {
  text: string;
  isUser: boolean;
  timestamp: Date;
  id: string;
}

const BillionDollarGameUI: React.FC = () => {
  const { gameid } = useParams<{ gameid: string }>();
  const [loading, setLoading] = useState(true);
  const [gameData, setGameData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [messages, setMessages] = useState<GameMessage[]>([]);
  const [showStats, setShowStats] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const { user } = useAuth();

  // Convert raw messages to structured format
  useEffect(() => {
    if (gameData?.messages) {
      const structuredMessages: GameMessage[] = [];
      for (let i = 0; i < gameData.messages.length; i++) {
        structuredMessages.push({
          text: gameData.messages[i],
          isUser: i % 2 === 1, // Odd indices are user messages
          timestamp: new Date(),
          id: `msg-${i}`
        });
      }
      setMessages(structuredMessages);
    }
  }, [gameData]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Fetch game data
  useEffect(() => {
    let isMounted = true;

    const fetchGame = async () => {
      if (!gameid) return;

      try {
        const data = await apiRequest({
          path: `/getgame?game_id=${gameid}`,
        });

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

    // Add user message immediately
    const userMessage: GameMessage = {
      text: input,
      isUser: true,
      timestamp: new Date(),
      id: `user-${Date.now()}`
    };
    setMessages(prev => [...prev, userMessage]);

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

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (loading) return <GameLoading />;

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100 flex items-center justify-center">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="text-6xl mb-4">⚠️</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Game Error</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <button 
              onClick={() => window.location.reload()}
              className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-xl font-semibold transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-3/4 right-1/4 w-64 h-64 bg-orange-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-4000"></div>
      </div>

      <NavBar user={user} />
      
      <div className="relative z-10 pt-16 h-screen flex flex-col">
        {/* Game Header */}
        <div className="bg-black/20 backdrop-blur-sm border-b border-white/10 p-4">
          <div className="max-w-6xl mx-auto flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🔥</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Fire Whisper RPG</h1>
                <p className="text-gray-300 text-sm">
                  Character: {gameData?.character?.name} | Saga: {gameData?.saga?.name}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowStats(!showStats)}
                className="bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded-lg transition-colors"
              >
                📊 Stats
              </button>
              <div className="text-white text-sm">
                Turns: {Math.floor(messages.length / 2)}
              </div>
            </div>
          </div>
        </div>

        {/* Stats Panel */}
        {showStats && (
          <div className="bg-black/30 backdrop-blur-sm border-b border-white/10 p-4">
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white/10 rounded-xl p-4">
                  <h3 className="text-white font-semibold mb-2">Character</h3>
                  <p className="text-gray-300 text-sm">{gameData?.character?.class}</p>
                  <p className="text-gray-400 text-xs">{gameData?.character?.background}</p>
                </div>
                <div className="bg-white/10 rounded-xl p-4">
                  <h3 className="text-white font-semibold mb-2">Progress</h3>
                  <p className="text-gray-300 text-sm">Messages: {messages.length}</p>
                  <p className="text-gray-400 text-xs">Active: {gameData?.game_active ? 'Yes' : 'No'}</p>
                </div>
                <div className="bg-white/10 rounded-xl p-4">
                  <h3 className="text-white font-semibold mb-2">Saga</h3>
                  <p className="text-gray-300 text-sm">{gameData?.saga?.name}</p>
                  <p className="text-gray-400 text-xs">{gameData?.saga?.description}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Messages Area */}
        <div className="flex-1 overflow-hidden">
          <div className="h-full max-w-4xl mx-auto p-4">
            <div className="h-full overflow-y-auto space-y-4 pb-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-3xl rounded-2xl p-4 ${
                      message.isUser
                        ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white ml-12'
                        : 'bg-white/90 backdrop-blur-sm text-gray-800 mr-12'
                    } shadow-lg animate-fade-in`}
                  >
                    {!message.isUser && (
                      <div className="flex items-center mb-2">
                        <div className="w-6 h-6 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center mr-2">
                          <span className="text-xs">🎭</span>
                        </div>
                        <span className="text-sm font-semibold text-gray-600">Game Master</span>
                      </div>
                    )}
                    <p className="whitespace-pre-wrap leading-relaxed">{message.text}</p>
                  </div>
                </div>
              ))}
              
              {sending && (
                <div className="flex justify-start">
                  <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-4 mr-12 shadow-lg">
                    <div className="flex items-center space-x-2">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce animation-delay-200"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce animation-delay-400"></div>
                      </div>
                      <span className="text-gray-600 text-sm">Game Master is thinking...</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-black/20 backdrop-blur-sm border-t border-white/10 p-4">
          <div className="max-w-4xl mx-auto">
            {!gameData?.game_active ? (
              <div className="text-center py-8">
                <div className="text-6xl mb-4">🎉</div>
                <h2 className="text-3xl font-bold text-white mb-2">Saga Complete!</h2>
                <p className="text-gray-300 mb-6">Congratulations on completing your adventure!</p>
                <button className="bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 text-white px-8 py-3 rounded-xl font-semibold transition-all transform hover:scale-105">
                  Start New Adventure
                </button>
              </div>
            ) : (
              <div className="flex items-end space-x-4">
                <div className="flex-1">
                  <textarea
                    ref={inputRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="What do you do next? Type your action..."
                    className="w-full bg-white/90 backdrop-blur-sm rounded-2xl px-6 py-4 text-gray-800 placeholder-gray-500 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 shadow-lg"
                    rows={3}
                    disabled={sending}
                  />
                </div>
                <button
                  onClick={handleSend}
                  disabled={sending || !input.trim()}
                  className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 disabled:from-gray-400 disabled:to-gray-500 text-white px-8 py-4 rounded-2xl font-semibold transition-all transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed shadow-lg"
                >
                  {sending ? (
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Sending</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-2">
                      <span>Send</span>
                      <span>⚡</span>
                    </div>
                  )}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BillionDollarGameUI;