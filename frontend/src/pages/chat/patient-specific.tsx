'use client';

import { cn } from '@/lib/utils';
import { useParams } from 'react-router-dom';

function PatientSpecificChat() {
  const { patientId } = useParams();
  const patient = { id: Number(patientId), name: 'John Doe', age: 45, condition: 'Hypertension' }; // Mock data

  return (
    <div
      className={cn(
        'flex',
        'flex-col',
        'items-center',
        'justify-center',
        'h-screen',
        'w-full',
        'p-4',
      )}
    >
      <h1 className='text-2xl font-semibold mb-4'>
        Chat About Patient #{patientId}, {patient.name}
      </h1>
      <textarea
        placeholder='Ask a question about this patient...'
        className={cn(
          'w-full',
          'max-w-lg',
          'h-40',
          'p-2',
          'border',
          'border-gray-300',
          'rounded-lg',
          'focus:ring-2',
          'focus:ring-green-500',
        )}
      ></textarea>
      <button
        className={cn(
          'mt-4',
          'bg-green-500',
          'text-white',
          'px-6',
          'py-2',
          'rounded-lg',
          'hover:bg-green-600',
        )}
      >
        Submit
      </button>
    </div>
  );
}

export default PatientSpecificChat;
