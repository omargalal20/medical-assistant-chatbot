import { http_client } from '../common/http-client';
import { API_ROUTES } from '@/services/v1/common/routes';
import { EncounterResource } from './types';

// Fetch recent encounters for a patient
export const getRecentEncounters = async (
  patientId: string,
  count: number = 3,
): Promise<EncounterResource[]> => {
  try {
    const response = await http_client.get(API_ROUTES.ENCOUNTERS.GET_RECENT(patientId, count));
    return response.data; // FastAPI returns a list of encounter JSON objects
  } catch (error) {
    console.error(`Failed to fetch recent encounters for patient with ID ${patientId}:`, error);
    throw new Error('Failed to get recent encounters.');
  }
};
