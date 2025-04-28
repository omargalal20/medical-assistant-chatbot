export type EncounterResource = {
  id: string;
  meta: {
    lastUpdated: string;
    source: string;
    versionId: string;
  };
  class: {
    code: string;
    system: string;
  };
  hospitalization?: {
    dischargeDisposition?: {
      coding: {
        code: string;
        display: string;
        system: string;
      }[];
      text?: string;
    };
  };
  participant: {
    individual: {
      display: string;
      reference: string;
    };
  }[];
  period: {
    start: string;
    end: string;
  };
  reasonCode?: {
    coding: {
      code: string;
      display: string;
      system: string;
    }[];
  }[];
  serviceProvider: {
    display: string;
    reference: string;
  };
  status: string;
  subject: {
    display: string;
    reference: string;
  };
  type: {
    coding: {
      code: string;
      display: string;
      system: string;
    }[];
    text?: string;
  }[];
  resourceType: string;
};
