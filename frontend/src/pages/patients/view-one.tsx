'use client';

import { cn } from '@/lib/utils';
import { useNavigate, useParams } from 'react-router-dom';
import { MEDICAL_QA_NAVIGATE_ROUTES } from '@/routes/paths/medical-qa';

function PatientDetails() {
  const navigate = useNavigate();
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
      <h1 className='text-2xl font-semibold mb-4'>Patient Details</h1>
      <div className='w-full max-w-lg space-y-4'>
        <p>
          <strong>Name:</strong> {patient.name}
        </p>
        <p>
          <strong>Age:</strong> {patient.age}
        </p>
        <p>
          <strong>Condition:</strong> {patient.condition}
        </p>
        <button
          onClick={() => navigate(MEDICAL_QA_NAVIGATE_ROUTES.PATIENT_SPECIFIC_CHAT(patient.id))}
          className={cn(
            'bg-green-500',
            'text-white',
            'px-4',
            'py-2',
            'rounded-lg',
            'hover:bg-green-600',
          )}
        >
          Chat About Patient
        </button>
      </div>
    </div>
  );
}

export default PatientDetails;
