import React from "react";

interface MessageBubbleProps {
  message: string;
  isUser: boolean;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isUser }) => {
  return (
    <div
      className={`w-full flex ${isUser ? "justify-end" : ""} items-start gap-2`}
    >
      {!isUser && (
        <picture>
          <source srcSet="/emberlyn.webp" type="image/webp" />
          <img
            src="/emberlyn.png"
            alt="Emberlyn Avatar"
            className="w-8 h-8 rounded-full"
            loading="lazy"
          />
        </picture>
      )}
      <div
        className={`${
          isUser ? "bg-green-100 text-black" : "text-[#3E2713]"
        } rounded-lg px-4 py-2 max-w-[70%]`}
      >
        <span
          dangerouslySetInnerHTML={{ __html: message.replace(/\n/g, "<br />") }}
        />
      </div>
      {isUser && (
        <picture>
          <source srcSet="/logo-transparent.webp" type="image/webp" />
          <img
            src="/logo-transparent.png"
            alt="User Avatar"
            className="w-8 h-8 rounded-full"
            loading="lazy"
          />
        </picture>
      )}
    </div>
  );
};

export default React.memo(MessageBubble);
