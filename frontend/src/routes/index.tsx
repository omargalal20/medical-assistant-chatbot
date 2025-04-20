import { lazy } from 'react';
import { Route } from 'react-router-dom';
import { MEDICAL_QA_PATHS } from './paths/medical-qa';

const Home = lazy(() => import('@/pages/home/home'));
const PATIENTS_VIEW_ALL = lazy(() => import('@/pages/patients/view-all'));
const PATIENTS_VIEW_ONE = lazy(() => import('@/pages/patients/view-one'));
const CHAT_GENERAL_QA = lazy(() => import('@/pages/chat/general'));
const CHAT_PATIENT_QA = lazy(() => import('@/pages/chat/patient-specific'));

export const HomeRoutes = [<Route path={MEDICAL_QA_PATHS.HOME} element={<Home />} key='home' />];

export const PatientRoutes = [
  <Route
    path={MEDICAL_QA_PATHS.PATIENTS.VIEW_ALL}
    element={<PATIENTS_VIEW_ALL />}
    key='patients-view-all'
  />,
  <Route
    path={MEDICAL_QA_PATHS.PATIENTS.VIEW_ONE}
    element={<PATIENTS_VIEW_ONE />}
    key='patients-view-one'
  />,
];

export const ChatRoutes = [
  <Route
    path={MEDICAL_QA_PATHS.CHAT.GENERAL_QA}
    element={<CHAT_GENERAL_QA />}
    key='chat-general'
  />,
  <Route
    path={MEDICAL_QA_PATHS.CHAT.PATIENT_QA}
    element={<CHAT_PATIENT_QA />}
    key='chat-patient'
  />,
];
