'use client';

import { useEffect, useState } from 'react';
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
import { useParams } from 'react-router-dom';
import { PatientResource } from '@/services/v1/patients/types';
import { getOne } from '@/services/v1/patients/routes';
import { getFullName } from '../patients/utils';

const MODELS = [{ id: 'us.anthropic.claude-3-7-sonnet-20250219-v1:0', name: 'Claude 3.7 Sonnet' }];

function PatientSpecificChat() {
  const { patientId } = useParams();
  const [patient, setPatient] = useState<PatientResource | null>(null);
  const [selectedModel, setSelectedModel] = useState(MODELS[0].id);

  useEffect(() => {
    if (!patientId) return;
    const fetchPatientData = async () => {
      try {
        const patientData = await getOne(patientId);
        setPatient(patientData);
      } catch (error) {
        console.error('Failed to fetch patient details:', error);
      }
    };
    fetchPatientData();
  }, [patientId]);

  const { messages, input, setInput, handleSubmit, isLoading, isTyping, stop } = useChat(
    import.meta.env.VITE_WS_URL as string + `/patient/${patient?.id}/ws`,
  );

  const isEmpty = messages.length === 0;

  return (
    <div className={cn('flex', 'flex-col', 'h-screen', 'w-full')}>
      {/* Top bar */}

      <div className={cn('flex', 'justify-between', 'p-4', 'border-b')}>
        <div className='text-lg font-semibold mr-4'>
          {patient ? `Chat about ${getFullName(patient)}` : 'Loading...'}
        </div>
        <div className='text-lg mr-4'>
          {patient ? `Patient ID: ${patient.id}` : ''}
        </div>
        <div className='text-lg mr-4'>
          {patient ? `Date of Birth: ${patient.birthDate}` : ''}
        </div>

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

export default PatientSpecificChat;
