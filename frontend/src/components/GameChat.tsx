import React, { useEffect, useRef } from "react";
import MessageBubble from "../components/MessageBubble";

interface GameChatProps {
  messages: string[];
  gameActive: boolean;
  input: string;
  onInputChange: (value: string) => void;
  onSend: () => void;
  sending: boolean;
  sidebarOpen: boolean;
}

const GameChat: React.FC<GameChatProps> = ({
  messages,
  gameActive,
  input,
  onInputChange,
  onSend,
  sending,
  sidebarOpen,
}) => {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const messagesContainerRef = useRef<HTMLDivElement | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const [textareaHeight, setTextareaHeight] = React.useState(48);
  const [showScrollButton, setShowScrollButton] = React.useState(false);

  useEffect(() => {
    // Use requestAnimationFrame to ensure scroll happens after layout
    requestAnimationFrame(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });

      // After scrolling, check if we're at bottom to hide the button
      setTimeout(() => {
        const container = messagesContainerRef.current;
        if (container) {
          const { scrollTop, scrollHeight, clientHeight } = container;
          const isAtBottom = scrollTop + clientHeight >= scrollHeight - 10;
          setShowScrollButton(!isAtBottom);
        }
      }, 200); // Increased timeout to ensure scroll animation completes
    });
  }, [messages]);

  // Check if user is scrolled to bottom
  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = container;
      const isAtBottom = scrollTop + clientHeight >= scrollHeight - 10;
      setShowScrollButton(!isAtBottom);
    };

    container.addEventListener("scroll", handleScroll);

    return () => container.removeEventListener("scroll", handleScroll);
  }, [textareaHeight]);

  useEffect(() => {
    // Only auto-focus on desktop (640px and wider), not mobile
    if (!sending && window.innerWidth >= 640) {
      textareaRef.current?.focus();
    }
  }, [sending]);

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      const maxHeight = window.innerHeight * 0.4;
      const newHeight = Math.min(textarea.scrollHeight, maxHeight);
      textarea.style.height = `${newHeight}px`;
      setTextareaHeight(newHeight);
    }
  }, [input]);

  const getPaddingBottom = () => {
    const isMobile = window.innerWidth < 640;
    if (isMobile) {
      return Math.max(textareaHeight + 16, 64);
    } else {
      return Math.max(textareaHeight - 40, 8);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const renderedMessages =
    Array.isArray(messages) && messages.length > 1
      ? messages
          .slice(1)
          .map((msg, idx) => (
            <MessageBubble key={idx} message={msg} isUser={idx % 2 !== 0} />
          ))
      : [];

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Messages area */}
      <div
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto px-8 space-y-3 pt-4 sm:pt-20"
        style={{
          paddingBottom: `${getPaddingBottom()}px`,
        }}
      >
        {renderedMessages.length ? (
          renderedMessages
        ) : (
          <div className="text-gray-400">No messages yet.</div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Gradient overlay */}
      <div
        className={`
          fixed right-0 h-8 z-5
          bg-gradient-to-t from-containerBackground to-transparent
          pointer-events-none
          transition-all duration-300
          ${sidebarOpen ? "left-0 sm:left-64" : "left-0 sm:left-12"}
        `}
        style={{
          bottom: `${textareaHeight + 8}px`,
        }}
      />

      {/* Scroll to bottom button */}
      {showScrollButton && (
        <div
          className={`
            fixed z-20 transition-all duration-300
            ${
              sidebarOpen
                ? "left-1/2 sm:left-[calc(50%+8rem)]"
                : "left-1/2 sm:left-[calc(50%+1.5rem)]"
            }
            transform -translate-x-1/2
          `}
          style={{
            bottom: `${textareaHeight + 32}px`, // Added another 8px more space (was +24, now +32)
          }}
        >
          <button
            onClick={scrollToBottom}
            className="bg-white hover:bg-gray-50 border border-gray-300 rounded-full p-2 shadow-lg transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-4 h-4 text-gray-600"
            >
              <path
                fillRule="evenodd"
                d="M12 2.25a.75.75 0 01.75.75v16.19l6.22-6.22a.75.75 0 111.06 1.06l-7.5 7.5a.75.75 0 01-1.06 0l-7.5-7.5a.75.75 0 111.06-1.06L11.25 19.19V3a.75.75 0 01.75-.75z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>
      )}

      {/* Fixed chat input at bottom */}
      <div
        className={`
          fixed bottom-0 right-0 bg-containerBackground px-8 pb-4 pt-2 z-10
          transition-all duration-300
          ${sidebarOpen ? "left-0 sm:left-64" : "left-0 sm:left-12"}
        `}
      >
        {sending ? (
          <div className="flex items-center justify-center text-[#3E2713] text-lg font-medium py-4">
            Waiting for response...
          </div>
        ) : !gameActive ? (
          <div className="flex items-center justify-center text-[#3E2713] text-lg font-bold py-4">
            Congratulations, you have completed this Saga!
          </div>
        ) : (
          <div className="flex justify-center">
            <div className="relative w-full max-w-[800px]">
              <textarea
                ref={textareaRef}
                className="w-full rounded-2xl px-4 py-3 pr-14 resize-none bg-white focus:outline-none focus:ring-2 focus:ring-[#E25C30] text-[#3E2713] shadow-sm border border-gray-200 min-h-[48px] leading-6"
                placeholder="Type your message..."
                value={input}
                onChange={(e) => onInputChange(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    onSend();
                  }
                }}
                disabled={sending}
                style={{
                  maxHeight: "40vh",
                  overflowY: "auto",
                }}
              />
              <button
                className="absolute bottom-3 right-3 text-white p-2 rounded-2xl disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
                style={{
                  backgroundColor: "#E25C30",
                  width: "32px",
                  height: "32px",
                }}
                onMouseEnter={(e) =>
                  (e.currentTarget.style.backgroundColor = "#D14520")
                }
                onMouseLeave={(e) =>
                  (e.currentTarget.style.backgroundColor = "#E25C30")
                }
                onClick={onSend}
                disabled={sending || !input.trim()}
              >
                {sending ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    className="w-4 h-4"
                  >
                    <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                  </svg>
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GameChat;
