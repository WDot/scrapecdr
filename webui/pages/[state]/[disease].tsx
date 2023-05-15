import StateList from "../../components/statelist";
import DiseaseList from "../../components/diseaselist";
import BestPracticeAdvisory from "../../components/bestpracticeadvisory";
import Link from "next/link";
import styles from "./[disease].module.css";

export async function getServerSideProps(context) {
  const state: string = "state" in context.query ? context.query.state : "Ohio";

  const diseaseListResponse = await fetch(
    `http://flask:80/allcdrsinstate/${state}`,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      cache: "no-store",
      body: JSON.stringify({}),
    }
  );
  console.log(diseaseListResponse);
  const diseaseListData = await diseaseListResponse.json();

  const disease = diseaseListData.diseases.includes(context.query.disease)
    ? context.query.disease
    : diseaseListData.diseases[0];

  const cdrInfoResponse = await fetch(
    `http://flask:80/cdrinfo/${state}/${disease}`,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      cache: "no-store",
      body: JSON.stringify({}),
    }
  );
  console.log(cdrInfoResponse);
  const cdrInfoData = await cdrInfoResponse.json();
  return {
    props: {
      diseases: diseaseListData.diseases,
      state: state,
      disease: disease,
      contactMethod: cdrInfoData.contactMethod,
      contactTiming: cdrInfoData.contactTiming,
    },
  };
}

export default function DiseasePage(props: {
  diseases: string[];
  state: string;
  disease: string;
  contactMethod: string;
  contactTiming: string;
}) {
  // This value is fully typed
  // The return value is *not* serialized
  // so you can return Date, Map, Set, etc.
  console.log(props.diseases);
  const stateList = ["Hawaii", "Indiana", "Ohio"];
  return (
    <table>
      <tbody>
        <tr>
          <td className={styles.column}>
            <StateList
              states={stateList}
              disease={props.disease}
              state={props.state}
            />
          </td>
          <td className={styles.column}>
            <DiseaseList
              diseases={props.diseases}
              state={props.state}
              disease={props.disease}
            />
          </td>
          <td className={styles.column}>
            <BestPracticeAdvisory
              disease={props.disease}
              state={props.state}
              contactMethod={props.contactMethod}
              contactTiming={props.contactTiming}
            />
          </td>
        </tr>
      </tbody>
    </table>
  );
}
