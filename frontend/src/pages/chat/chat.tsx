"use client";

import { useState, useRef, useEffect } from "react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { ChatHeader } from "@/components/layout/header";
import { MessageList } from "./message-list";
import { ChatFooter } from "@/components/layout/footer";

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

type GenerationStage = "idle" | "thinking" | "searching" | "responding";

const sources = {
  "1": {
    title: "Artificial Intelligence Basics",
    url: "https://example.com/ai-basics",
    author: "John Smith",
    date: "2023-05-10",
  },
  "2": {
    title: "Machine Learning Fundamentals",
    url: "https://example.com/ml-fundamentals",
    author: "Sarah Johnson",
    date: "2022-11-22",
  },
  "3": {
    title: "Deep Learning Applications",
    url: "https://example.com/deep-learning",
    author: "Michael Chen",
    date: "2024-01-15",
  },
};

const CitationReference = ({
  match,
  children,
}: {
  match: RegExpMatchArray;
  children: React.ReactNode;
}) => {
  const citationNumber = match[1] as keyof typeof sources;
  const source = sources[citationNumber];

  if (!source) {
    return <span>{children}</span>;
  }

  return (
    <Popover>
      <PopoverTrigger asChild>
        <span className="cursor-pointer text-blue-500 font-medium">
          {children}
        </span>
      </PopoverTrigger>
      <PopoverContent className="w-80">
        <div className="space-y-2">
          <h3 className="font-medium">{source.title}</h3>
          <p className="text-sm text-muted-foreground">
            By {source.author} • {source.date}
          </p>
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center text-sm text-blue-500 hover:underline"
          >
            View source <span className="ml-1">↗</span>
          </a>
        </div>
      </PopoverContent>
    </Popover>
  );
};

export default function Chat() {
  const [messages, setMessages] = useState<MessageData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [generationStage, setGenerationStage] =
    useState<GenerationStage>("idle");
  const [selectedModel] = useState("gpt-4");
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const patternHandlers = [
    {
      pattern: /\[(\d+)\]/g,
      component: CitationReference,
    },
  ];

  const handleSendMessage = (content: string) => {
    const userMessage: MessageData = {
      id: Date.now().toString(),
      content,
      sender: "user",
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setGenerationStage("thinking");

    timeoutRef.current = setTimeout(() => {
      setGenerationStage("searching");

      timeoutRef.current = setTimeout(() => {
        setGenerationStage("responding");

        timeoutRef.current = setTimeout(() => {
          let responseContent = "";

          if (
            content.toLowerCase().includes("ai") ||
            content.toLowerCase().includes("artificial intelligence")
          ) {
            responseContent = `Artificial Intelligence (AI) is a field of computer science focused on creating systems capable of performing tasks that typically require human intelligence [1]. These include learning, reasoning, problem-solving, perception, and language understanding.
            
Machine learning, a subset of AI, uses algorithms to enable systems to learn from data [2]. Recent advancements in deep learning have significantly improved AI capabilities in areas like image recognition and natural language processing [3].`;
          } else {
            responseContent = `[${
              selectedModel === "gpt-4"
                ? "GPT-4"
                : selectedModel === "gpt-3.5"
                ? "GPT-3.5"
                : selectedModel === "claude-3"
                ? "Claude 3"
                : selectedModel === "gemini-pro"
                ? "Gemini Pro"
                : "Llama 3"
            }] Response to: "${content}"`;
          }

          const assistantMessage: MessageData = {
            id: (Date.now() + 1).toString(),
            content: responseContent,
            sender: "assistant",
            metadata: {
              model: selectedModel,
              responseTime: 4.5,
              tokens: 256,
            },
          };

          setMessages((prev) => [...prev, assistantMessage]);
          setIsLoading(false);
          setGenerationStage("idle");
          timeoutRef.current = null;
        }, 1500);
      }, 1500);
    }, 1500);
  };

  const handleStopGeneration = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;

      const stoppedMessage: MessageData = {
        id: Date.now().toString(),
        content: "Generation stopped by user",
        sender: "assistant",
        metadata: {
          model: selectedModel,
          responseTime: 0,
          tokens: 0,
        },
      };

      setMessages((prev) => [...prev, stoppedMessage]);
      setIsLoading(false);
      setGenerationStage("idle");
    }
  };

  const handleEditMessage = (id: string, content: string) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === id ? { ...msg, content } : msg))
    );
  };

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <ChatHeader />
      <div className="container mx-auto flex flex-col flex-1 overflow-hidden">
        {/* Make the message list container take available space */}
        <div className="flex-1 overflow-hidden">
          <MessageList
            messages={messages}
            isLoading={isLoading}
            generationStage={generationStage}
            patternHandlers={patternHandlers}
            onEditMessage={handleEditMessage}
          />
        </div>
        <ChatFooter
          onSendMessage={handleSendMessage}
          onStopGeneration={handleStopGeneration}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}
