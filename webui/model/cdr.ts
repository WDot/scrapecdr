import CDRHawaiiLocale from "./cdrhawaii"

export default interface CDR {
    disease: string
    contactMethod: string | CDRHawaiiLocale[]
    contactTiming: string
}