import { Message, PatternHandler } from "@/components/message";
import {
  GenerationStatus,
  GenerationStage,
} from "@/components/generation-status";
import { Info, Copy } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { toast } from "sonner";

interface MessageData {
  id: string;
  content: string;
  sender: "user" | "assistant";
  metadata?: {
    model?: string;
    responseTime?: number;
    tokens?: number;
  };
}

interface MessageListProps {
  messages: MessageData[];
  isLoading: boolean;
  generationStage: GenerationStage;
  patternHandlers: PatternHandler[];
  onEditMessage: (id: string, content: string) => void;
}

export function MessageList({
  messages,
  isLoading,
  generationStage,
  patternHandlers,
  onEditMessage,
}: MessageListProps) {
  const [metadataVisible, setMetadataVisible] = useState<Record<string, boolean>>({});
  const [copying, setCopying] = useState<string | null>(null);

  // Create a ref for the scrollable container
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to the bottom when messages change
  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const toggleMetadata = (id: string) => {
    setMetadataVisible((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const handleCopy = (id: string, content: string) => {
    navigator.clipboard.writeText(content);
    setCopying(id);

    toast.success("Copied to clipboard", {
      description: "Message content has been copied to your clipboard.",
      duration: 2000,
    });

    setTimeout(() => {
      setCopying(null);
    }, 1000);
  };

  return (
    <div
      ref={scrollContainerRef}
      className="h-full flex-1 overflow-y-auto p-4 space-y-8"
    >
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full" />
      ) : (
        messages.map((message) => {
          const actionButtons =
            message.sender === "assistant"
              ? [
                  {
                    id: "info",
                    icon: <Info size={14} />,
                    onClick: () => toggleMetadata(message.id),
                    title: "View message info",
                    position: "inside" as const,
                    className: metadataVisible[message.id] ? "text-blue-500" : "",
                  },
                  {
                    id: "copy",
                    icon: (
                      <Copy
                        size={14}
                        className={copying === message.id ? "text-green-500" : ""}
                      />
                    ),
                    onClick: () => handleCopy(message.id, message.content),
                    title: "Copy message",
                    position: "inside" as const,
                  },
                ]
              : [
                  {
                    id: "copy",
                    icon: (
                      <Copy
                        size={16}
                        className={copying === message.id ? "text-green-500" : ""}
                      />
                    ),
                    onClick: () => handleCopy(message.id, message.content),
                    title: "Copy message",
                    position: "outside" as const,
                  },
                ];

          return (
            <div key={message.id} className="w-full">
              <Message
                content={message.content}
                sender={message.sender}
                actionButtons={actionButtons}
                editable={false}
                onEdit={(content) => onEditMessage(message.id, content)}
                patternHandlers={message.sender === "assistant" ? patternHandlers : undefined}
              />

              {message.sender === "assistant" &&
                message.metadata &&
                metadataVisible[message.id] && (
                  <div className="ml-10 mt-1 p-3 bg-muted/80 rounded-md text-sm border border-border shadow-sm max-w-[70%]">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-sm">Message Info</h4>
                      <button
                        onClick={() => toggleMetadata(message.id)}
                        className="text-muted-foreground hover:text-foreground text-xs"
                      >
                        Close
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      {Object.entries(message.metadata).map(([key, value]) => (
                        <div key={key} className="contents">
                          <div className="text-muted-foreground capitalize text-xs">
                            {key.replace(/([A-Z])/g, " $1").trim()}:
                          </div>
                          <div className="font-medium text-xs">
                            {String(value)}
                            {key === "responseTime" && "s"}
                            {key === "tokens" && " tokens"}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
            </div>
          );
        })
      )}

      {isLoading && <GenerationStatus stage={generationStage} />}
    </div>
  );
}
