import StateList from '../../components/statelist'
import DiseaseList from '../../components/diseaselist'
import Link from 'next/link'

export async function getServerSideProps(context) {
  const state : string = ("state" in context.query) ? context.query.state : 'Ohio';
  const disease : string = ("disease" in context.query) ? context.query.state : 'Botulism';  
  
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
  console.log(data)
  return {props: {diseases: data.diseases, state: state, disease: disease}};
}

export default function DiseasePage(props: {diseases: string[], state: string, disease: string}) {
  // This value is fully typed
  // The return value is *not* serialized
  // so you can return Date, Map, Set, etc.
  console.log(props.diseases)
  const stateList = ["Hawaii","Indiana","Ohio"];
  return (<table>
            <tr>
              <td><StateList states={stateList} disease={props.disease} /></td>
              <td><DiseaseList diseases={props.diseases} state={props.state} /></td>
            </tr>
          </table>
          );
}