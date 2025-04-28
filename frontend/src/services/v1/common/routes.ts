export const API_ROUTES = {
  PATIENTS: {
    GET_MANY: `/patients`,
    GET_ONE: (id: string) => `/patients/${id}`,
  },
  ENCOUNTERS: {
    GET_RECENT: (patientId: string, count: number) => `/encounters/recent/patients/${patientId}?count=${count}`,
  },
  CONDITIONS: {
    GET_LATEST: (patientId: string) => `/conditions/latest/patients/${patientId}`,
  }
};
