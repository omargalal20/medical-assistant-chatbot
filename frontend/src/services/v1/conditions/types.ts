export interface Meta {
    lastUpdated: string;
    source: string;
    versionId: string;
}

export interface Coding {
    code: string;
    system: string;
    display?: string;
}

export interface ClinicalStatus {
    coding: Coding[];
}

export interface Code {
    display: string;
    coding: Coding[];
    text: string;
}

export interface Reference {
    reference: string;
}

export interface VerificationStatus {
    coding: Coding[];
}

export interface ConditionResource {
    id: string;
    meta: Meta;
    abatementDateTime?: string;
    clinicalStatus: ClinicalStatus;
    code: Code;
    encounter?: Reference;
    onsetDateTime?: string;
    recordedDate?: string;
    subject: Reference;
    verificationStatus: VerificationStatus;
    resourceType: string;
}
