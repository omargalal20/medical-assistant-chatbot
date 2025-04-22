'use client';

import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { useNavigate } from 'react-router-dom';
import { MEDICAL_QA_NAVIGATE_ROUTES } from '@/routes/paths/medical-qa';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

import { getMany } from '@/services/v1/patients/routes';
import { PatientResource } from '@/services/v1/patients/types';
import { getFullName } from './utils';

function ViewAll() {
  const navigate = useNavigate();
  const [patients, setPatients] = useState<PatientResource[]>([]);
  const [, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await getMany();
        console.log('Fetched Patients:', response);
        setPatients(response); // Update the state with fetched patients
      } catch (err) {
        console.error('Error fetching patients:', err);
        setError('Failed to fetch patients.');
      }
    };

    fetchPatients();
  }, []);

  return (
    <>
      <div
        className={cn(
          'flex',
          'flex-col',
          'items-center',
        )}
      >
        <h1 className='text-2xl font-semibold mb-4'>Patients</h1>
      </div>
      <Table className="w-[75%] mx-auto">
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">ID</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Date Of Birth</TableHead>
            <TableHead className="text-right">View Patient</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {patients.map((patient) => (
            <TableRow key={patient.id}>
              <TableCell className="font-medium">{patient.id}</TableCell>
              <TableCell>{getFullName(patient)}</TableCell>
              <TableCell>{patient.birthDate}</TableCell>
              <TableCell className="text-right">
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
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>

  );
}

export default ViewAll;
