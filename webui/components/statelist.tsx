import Link from 'next/link'

export default function StateList(props: {states: string[], disease: string}) {
    // This value is fully typed
    // The return value is *not* serialized
    // so you can return Date, Map, Set, etc.
  
    return (
        <ul>
            {props.states.map(x=>{return (<li><Link href={`/${x}/${props.disease}`}>{x}</Link></li>)})}
        </ul>
        
    );}
