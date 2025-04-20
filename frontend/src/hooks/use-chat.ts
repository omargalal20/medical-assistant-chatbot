import { useState, useRef, useEffect } from 'react';
import { Message, Role } from '@/components/ui/chat-message';

interface UseChatHook {
  messages: Message[];
  input: string;
  setInput: React.Dispatch<React.SetStateAction<string>>;
  handleInputChange: (value: string) => void;
  handleSubmit: (
    event?: { preventDefault?: () => void },
    options?: { experimental_attachments?: FileList },
  ) => void;
  isLoading: boolean;
  isTyping: boolean;
  stop: () => void;
  error: string | null;
}

interface MessagePayload {
  id: string;
  role: Role.USER | Role.ASSISTANT;
  content: string;
  created_at: Date;
  attachments?: {
    name: string;
    size: number;
    type: string;
  }[];
}

const useChat = (url: string): UseChatHook => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isTyping, setIsTyping] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log('Connected to WebSocket:', url);
      setError(null); // Clear any previous errors on successful connection
    };

    socket.onclose = () => {
      console.log('Disconnected from WebSocket');
    };

    socket.onmessage = (event) => {
      try {
        const rawData = JSON.parse(event.data);
        console.log('Raw message received:', rawData);

        if (typeof rawData === 'string') {
          const nestedData = JSON.parse(rawData);
          console.log('Nested message decoded:', nestedData);

          const normalizedMessage: Message = {
            id: nestedData.id,
            role: nestedData.role as Role.USER | Role.ASSISTANT,
            content: nestedData.content,
            created_at: new Date(nestedData.created_at),
          };

          setMessages((prevMessages) => [...prevMessages, normalizedMessage]);
        } else {
          const normalizedMessage: Message = {
            id: rawData.id,
            role: rawData.role.toLowerCase() as Role.USER | Role.ASSISTANT,
            content: rawData.content,
            created_at: new Date(rawData.created_at),
          };

          setMessages((prevMessages) => [...prevMessages, normalizedMessage]);
        }

        setIsLoading(false);
        setIsTyping(false);
      } catch (error) {
        console.error('Error processing message:', error);
        setError('Failed to process incoming message.');
      }
    };

    socket.onerror = (event) => {
      console.error('WebSocket encountered an error:', event);
      setError('A connection error occurred. Please try again.');
    };

    return () => {
      socket.close();
    };
  }, [url]);

  const handleInputChange = (value: string) => {
    setInput(value);
  };

  const handleSubmit = (
    event?: { preventDefault?: () => void },
    options?: { experimental_attachments?: FileList },
  ) => {
    event?.preventDefault?.();
    if (!socketRef.current || !input.trim()) return;

    const userMessage: Omit<MessagePayload, 'attachments'> = {
      id: `${Date.now()}`,
      role: Role.USER,
      content: input,
      created_at: new Date(),
    };

    const payload: MessagePayload = {
      ...userMessage,
      attachments: options?.experimental_attachments
        ? Array.from(options.experimental_attachments).map((file) => ({
            name: file.name,
            size: file.size,
            type: file.type,
          }))
        : undefined,
    };

    try {
      setMessages((prevMessages) => [...prevMessages, payload]);
      socketRef.current.send(JSON.stringify(payload));
      setIsLoading(true);
      setIsTyping(true);
      setError(null);
      setInput('');
    } catch (error) {
      console.error('Failed to send message:', error);
      setError('Failed to send the message. Please try again.');
    }
  };

  return {
    messages,
    input,
    setInput,
    handleInputChange,
    handleSubmit,
    isLoading,
    isTyping,
    stop,
    error,
  };
};

export default useChat;
