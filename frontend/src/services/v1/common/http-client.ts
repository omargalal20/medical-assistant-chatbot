import axios from 'axios';
import { BASE_URL } from '@/services/v1/common/constants';

export const http_client = axios.create({
  baseURL: BASE_URL,
});
