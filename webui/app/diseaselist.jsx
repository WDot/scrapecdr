async function getDiseaseList(state) {
    const res = await fetch(`http://flask:80/allcdrsinstate/${state}`,{
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: "POST",
      cache: 'no-store',
      body: JSON.stringify({})
  });
    const data = await res.json();
    return data;
  }
  
  export default async function DiseaseList() {
    // This value is fully typed
    // The return value is *not* serialized
    // so you can return Date, Map, Set, etc.
    const data = await getDiseaseList('Ohio');
  
    return <p>{JSON.stringify(data)}</p>;
  }