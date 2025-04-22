'use client';

import { cn } from '@/lib/utils';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { MEDICAL_QA_NAVIGATE_ROUTES } from '@/routes/paths/medical-qa';
import { getOne } from '@/services/v1/patients/routes';
import { PatientResource } from '@/services/v1/patients/types';
import { getFullName } from './utils';

function ViewOne() {
  const navigate = useNavigate();
  const { patientId } = useParams();
  const [patient, setPatient] = useState<PatientResource | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!patientId) return;

    const fetchPatientDetails = async () => {
      setLoading(true);
      try {
        const data = await getOne(patientId);
        setPatient(data);
      } catch (error) {
        console.error('Failed to fetch patient details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPatientDetails();
  }, [patientId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen w-full">
        <p>Loading...</p>
      </div>
    );
  }

  if (!patient) {
    return (
      <div className="flex items-center justify-center h-screen w-full">
        <p>Patient not found</p>
      </div>
    );
  }

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
      <h1 className="text-2xl font-semibold mb-4">Patient Details</h1>
      <div className="w-full max-w-lg space-y-4">
        <p>
          <strong>Name:</strong> {getFullName(patient)}
        </p>
        <p>
          <strong>Date Of Birth:</strong> {patient.birthDate}
        </p>
        <p>
          <strong>Gender:</strong> {patient.gender}
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

export default ViewOne;