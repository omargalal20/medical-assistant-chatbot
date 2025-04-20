'use client';

import { cn } from '@/lib/utils';
import { useNavigate } from 'react-router-dom';
import { MEDICAL_QA_NAVIGATE_ROUTES } from '@/routes/paths/medical-qa';

function PatientList() {
  const navigate = useNavigate();
  const patients = [
    { id: 1, name: 'John Doe', age: 45 },
    { id: 2, name: 'Jane Smith', age: 32 },
  ];

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
      <h1 className='text-2xl font-semibold mb-4'>Patients</h1>
      <ul className='w-full max-w-lg space-y-4'>
        {patients.map((patient) => (
          <li
            key={patient.id}
            className={cn(
              'flex',
              'justify-between',
              'items-center',
              'p-4',
              'border',
              'border-gray-300',
              'rounded-lg',
            )}
          >
            <span>
              {patient.name} (Age: {patient.age})
            </span>
            <button
              onClick={() => navigate(MEDICAL_QA_NAVIGATE_ROUTES.PATIENT_DETAILS(patient.id))}
              className={cn(
                'bg-green-500',
                'text-white',
                'px-4',
                'py-2',
                'rounded-lg',
                'hover:bg-green-600',
              )}
            >
              View
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PatientList;
