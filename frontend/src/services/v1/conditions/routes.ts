import { http_client } from '../common/http-client';
import { API_ROUTES } from '@/services/v1/common/routes';
import { ConditionResource } from './types';

// Fetch the latest condition for a patient
export const getLatestCondition = async (patientId: string): Promise<ConditionResource[]> => {
  try {
    const response = await http_client.get(API_ROUTES.CONDITIONS.GET_LATEST(patientId));
    return response.data; // FastAPI returns a condition JSON object or an error object
  } catch (error) {
    console.error(`Failed to fetch the latest condition for patient with ID ${patientId}:`, error);
    throw new Error('Failed to get the latest condition.');
  }
};
