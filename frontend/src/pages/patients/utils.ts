import { PatientResource } from "@/services/v1/patients/types";

export function getFullName(patient: PatientResource): string {
    if (!patient.name || patient.name.length === 0) {
        return "N/A";
    }

    // Take the first name entry (commonly the "official" one)
    const { given = [], family = "" } = patient.name[0];

    // Flatten and concatenate the names
    return [...given, family].join(" ").trim();
}
