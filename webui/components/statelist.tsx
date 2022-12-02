import Link from 'next/link'
import styles from './statelist.module.css'

export default function StateList(props: {states: string[], disease: string, state: string}) {
    // This value is fully typed
    // The return value is *not* serialized
    // so you can return Date, Map, Set, etc.
  
    return (
        <ul>
            {props.states.map(x=>{return (<li className={(x === props.state) ? styles.selected : styles.deselected}><Link href={`/${encodeURI(x)}/${encodeURI(props.disease)}`}>{x}</Link></li>)})}
        </ul>
        
    );}
