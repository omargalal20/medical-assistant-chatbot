'use client';

import { cn } from '@/lib/utils';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { MEDICAL_QA_NAVIGATE_ROUTES } from '@/routes/paths/medical-qa';
import { getOne } from '@/services/v1/patients/routes';
import { getRecentEncounters } from '@/services/v1/encounters/routes';
import { getLatestCondition } from '@/services/v1/conditions/routes';
import { PatientResource } from '@/services/v1/patients/types';
import { EncounterResource } from '@/services/v1/encounters/types';
import { ConditionResource } from '@/services/v1/conditions/types';
import { getFullName } from './utils';

function ViewOne() {
  const navigate = useNavigate();
  const { patientId } = useParams();
  const [patient, setPatient] = useState<PatientResource | null>(null);
  const [encounters, setEncounters] = useState<EncounterResource[]>([]);
  const [latestCondition, setLatestCondition] = useState<ConditionResource | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!patientId) return;

    const fetchAllData = async () => {
      setLoading(true);
      try {
        const RECENT_ENCOUNTER_COUNT = 3; // Number of recent encounters to fetch
        // Fetch data concurrently
        const [patientData, encountersData, conditionData] = await Promise.all([
          getOne(patientId),
          getRecentEncounters(patientId, RECENT_ENCOUNTER_COUNT),
          getLatestCondition(patientId),
        ]);

        console.log('Patient Data:', patientData);
        console.log('Encounters Data:', encountersData);
        console.log('Latest Condition Data:', conditionData);

        // Update state with the fetched data
        setPatient(patientData);
        setEncounters(encountersData);
        setLatestCondition(conditionData);
      } catch (error) {
        console.error('Failed to fetch patient details or related data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAllData();
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
        <h2 className="text-xl font-semibold mt-6">Recent Encounters</h2>
        {encounters.length > 0 ? (
          <ul>
            {encounters.map((encounter) => (
              <li key={encounter.id}>
                <p><strong>Start Date:</strong> {encounter.period.start}</p>
                <p><strong>End Date:</strong> {encounter.period.end}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No recent encounters found.</p>
        )}
        <h2 className="text-xl font-semibold mt-6">Latest Condition</h2>
        {latestCondition ? (
          <div>
            <p><strong>Condition:</strong> {latestCondition.code.text || 'No display available'}</p>
          </div>
        ) : (
          <p>No condition found.</p>
        )}
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
