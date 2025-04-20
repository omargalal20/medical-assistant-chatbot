'use client';

import { cn } from '@/lib/utils';
import { useNavigate } from 'react-router-dom';
import { MEDICAL_QA_NAVIGATE_ROUTES } from '@/routes/paths/medical-qa';

function Home() {
  const navigate = useNavigate();
  return (
    <div className={cn('flex', 'flex-col', 'items-center', 'justify-center', 'h-screen', 'w-full')}>
      <h1 className='text-2xl font-semibold mb-4'>Welcome to Medical Q&A Assistant</h1>
      <div className='space-y-4'>
        <button
          onClick={() => navigate(MEDICAL_QA_NAVIGATE_ROUTES.GENERAL_CHAT)}
          className={cn(
            'btn',
            'bg-blue-500',
            'text-white',
            'px-4',
            'py-2',
            'rounded-lg',
            'hover:bg-blue-600',
            'm-2',
          )}
        >
          Ask General Questions
        </button>
        <button
          onClick={() => navigate(MEDICAL_QA_NAVIGATE_ROUTES.PATIENTS)}
          className={cn(
            'btn',
            'bg-green-500',
            'text-white',
            'px-4',
            'py-2',
            'rounded-lg',
            'hover:bg-green-600',
            'm-2',
          )}
        >
          View Patients
        </button>
      </div>
    </div>
  );
}

export default Home;
