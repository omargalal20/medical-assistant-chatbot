import { http_client } from '../common/http-client';
import { API_ROUTES } from '@/services/v1/common/routes';
import { PatientResource } from './types';

// Fetch multiple patients
export const getMany = async (): Promise<PatientResource[]> => {
  try {
    const response = await http_client.get(API_ROUTES.PATIENTS.GET_MANY);
    return response.data; // FastAPI returns a list of patient JSON objects
  } catch (error) {
    console.error('Failed to fetch patients:', error);
    throw new Error('Failed to get patients.');
  }
};

// Fetch a single patient by ID
export const getOne = async (id: string): Promise<PatientResource> => {
  try {
    const response = await http_client.get(API_ROUTES.PATIENTS.GET_ONE(id));
    return response.data; // FastAPI returns a patient JSON object
  } catch (error) {
    console.error(`Failed to fetch patient with ID ${id}:`, error);
    throw new Error('Failed to get patient.');
  }
};
