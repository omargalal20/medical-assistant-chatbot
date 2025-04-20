export const MEDICAL_QA_PATHS = {
  HOME: '/',
  PATIENTS: {
    VIEW_ALL: '/patients',
    VIEW_ONE: '/patients/:patientId',
  },
  CHAT: {
    GENERAL_QA: '/chat/general',
    PATIENT_QA: '/chat/patient/:patientId',
  },
};

export const MEDICAL_QA_NAVIGATE_ROUTES = {
  HOME: '/',
  GENERAL_CHAT: '/chat/general',
  PATIENTS: '/patients',
  PATIENT_DETAILS: (id: number) => `/patients/${id}`,
  PATIENT_SPECIFIC_CHAT: (id: number) => `/chat/patient/${id}`,
};
