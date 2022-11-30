async function getData() {
  //const res = await fetch('http://google.com');
  //const data = await res.json();
  return {};
}

export default async function Page() {
  // This value is fully typed
  // The return value is *not* serialized
  // so you can return Date, Map, Set, etc.
  const name = await getData();

  return <main>{/* ... */}</main>;
}