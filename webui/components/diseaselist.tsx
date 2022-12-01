export default function DiseaseList(props: {diseases: string[]}) {
    // This value is fully typed
    // The return value is *not* serialized
    // so you can return Date, Map, Set, etc.
  
    return (
        <ul>
            {props.diseases.map(x=>{return (<li>${x}</li>)})}
        </ul>
        
    );}
