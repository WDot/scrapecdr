import DiseaseList from './diseaselist'

export default async function Page() {
  // This value is fully typed
  // The return value is *not* serialized
  // so you can return Date, Map, Set, etc.

  return <main><DiseaseList /></main>;
}