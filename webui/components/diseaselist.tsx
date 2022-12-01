import Link from 'next/link'

export default function DiseaseList(props: {diseases: string[], state: string}) {
    // This value is fully typed
    // The return value is *not* serialized
    // so you can return Date, Map, Set, etc.
  
    return (
        <ul>
            {props.diseases.map(x=>{return (<li><Link href={`/${props.state}/${x}`}>{x}</Link></li>)})}
        </ul>
        
    );}
