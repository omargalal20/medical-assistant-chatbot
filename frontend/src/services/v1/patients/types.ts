export type PatientResource = {
    id: string;
    meta: {
        lastUpdated: string;
        source: string;
        versionId: string;
    };
    extension: Array<{
        url: string;
        extension?: Array<{
            url: string;
            valueCoding?: {
                code: string;
                display: string;
                system: string;
            };
            valueString?: string;
            valueCode?: string;
            valueDecimal?: number;
            valueAddress?: {
                city?: string;
                state?: string;
                country?: string;
            };
        }>;
        valueString?: string;
        valueCode?: string;
        valueDecimal?: number;
        valueAddress?: {
            city?: string;
            state?: string;
            country?: string;
        };
    }>;
    text: {
        div: string;
        status: string;
    };
    address: Array<{
        extension?: Array<{
            url: string;
            extension: Array<{
                url: string;
                valueDecimal: number;
            }>;
        }>;
        city?: string;
        country?: string;
        line?: string[];
        postalCode?: string;
        state?: string;
    }>;
    birthDate: string;
    communication: Array<{
        language: {
            coding: Array<{
                code: string;
                display: string;
                system: string;
            }>;
            text: string;
        };
    }>;
    gender: string;
    identifier: Array<{
        system: string;
        value: string;
        type?: {
            coding: Array<{
                code: string;
                display: string;
                system: string;
            }>;
            text: string;
        };
    }>;
    maritalStatus: {
        coding: Array<{
            code: string;
            display: string;
            system: string;
        }>;
        text: string;
    };
    multipleBirthBoolean: boolean;
    name: Array<{
        family: string;
        given: string[];
        prefix?: string[];
        use: string;
    }>;
    telecom: Array<{
        system: string;
        use: string;
        value: string;
    }>;
    resourceType: string;
};
