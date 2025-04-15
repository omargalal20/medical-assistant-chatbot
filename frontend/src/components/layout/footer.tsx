// 3. ChatFooter.tsx
import { ChatInput } from "@/components/chat-input";

interface ChatFooterProps {
  onSendMessage: (content: string) => void;
  onStopGeneration: () => void;
  isLoading: boolean;
}

export function ChatFooter({
  onSendMessage,
  onStopGeneration,
  isLoading,
}: ChatFooterProps) {
  return (
    <div className="p-4">
      <ChatInput
        onSend={onSendMessage}
        onStopGeneration={onStopGeneration}
        isLoading={isLoading}
        placeholder="Ask about medical queries"
        tools={[]}
      />
    </div>
  );
}
