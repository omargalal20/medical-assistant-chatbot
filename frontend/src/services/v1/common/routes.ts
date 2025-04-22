export const API_ROUTES = {
  PATIENTS: {
    GET_MANY: `/patients`,
    GET_ONE: (id: string) => `/patients/${id}`,
  },
};
