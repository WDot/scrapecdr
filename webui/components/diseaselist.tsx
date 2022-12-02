import Link from 'next/link'
import styles from './diseaselist.module.css'

export default function DiseaseList(props: {diseases: string[], state: string, disease: string}) {
    // This value is fully typed
    // The return value is *not* serialized
    // so you can return Date, Map, Set, etc.
  
    return (
        <ul>
            {props.diseases.map(x=>{return (<li className={(x === props.disease) ? styles.selected : styles.deselected}><Link href={`/${encodeURIComponent(props.state)}/${encodeURIComponent(x)}`}>{x}</Link></li>)})}
        </ul>
        
    );}
