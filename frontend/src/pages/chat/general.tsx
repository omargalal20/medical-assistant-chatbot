'use client';

import { useState } from 'react';
import useChat from '@/hooks/use-chat';

import { cn } from '@/lib/utils';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ChatContainer, ChatForm, ChatMessages } from '@/components/ui/chat';
import { MessageInput } from '@/components/ui/message-input';
import { MessageList } from '@/components/ui/message-list';

const MODELS = [{ id: 'us.anthropic.claude-3-7-sonnet-20250219-v1:0', name: 'Claude 3.7 Sonnet' }];

function General() {
  const [selectedModel, setSelectedModel] = useState(MODELS[0].id);

  const { messages, input, setInput, handleSubmit, isLoading, isTyping, stop } = useChat(
    import.meta.env.VITE_WS_URL as string,
  );

  const isEmpty = messages.length === 0;

  console.log('Messages:', messages);

  return (
    <div className={cn('flex', 'flex-col', 'h-screen', 'w-full')}>
      {/* Top bar */}
      <div className={cn('flex', 'justify-end', 'p-4', 'border-b')}>
        <Select value={selectedModel} onValueChange={setSelectedModel}>
          <SelectTrigger className='w-[25%]'>
            <SelectValue placeholder='Select Model' />
          </SelectTrigger>
          <SelectContent>
            {MODELS.map((model) => (
              <SelectItem key={model.id} value={model.id}>
                {model.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Chat area */}
      <ChatContainer className='flex-1 flex flex-col overflow-hidden'>
        {!isEmpty && (
          <ChatMessages messages={messages}>
            <MessageList messages={messages} isTyping={isTyping} />
          </ChatMessages>
        )}

        <ChatForm
          className='w-ful mt-auto px-4 py-2 border-t'
          isPending={isLoading || isTyping}
          handleSubmit={handleSubmit}
        >
          {({ files, setFiles }) => (
            <MessageInput
              value={input}
              onChange={(e) => setInput(e.target.value)}
              allowAttachments
              files={files}
              setFiles={setFiles}
              stop={stop}
              isGenerating={isLoading}
            />
          )}
        </ChatForm>
      </ChatContainer>
    </div>
  );
}

export default General;
