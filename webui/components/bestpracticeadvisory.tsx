import Link from "next/link";
import styles from "./bestpracticeadvisory.module.css";

export default function BestPracticeAdvisory(props: {
  state: string;
  disease: string;
  contactMethod?: string;
  contactTiming?: string;
}) {
  // This value is fully typed
  // The return value is *not* serialized
  // so you can return Date, Map, Set, etc.

  return (
    <div className={styles.window}>
      <div>
        It looks like this particular diagnosis is a Reportable Communicable
        Disease according to your state's Department of Health. They request you
        report it in the following manner.
      </div>
      <div className={styles.field}>
        <b>State: </b>
        {props.state}
      </div>
      <div className={styles.field}>
        <b>Disease: </b>
        {props.disease}
      </div>
      <div className={styles.field}>
        <b>Contact Timing: </b>
        {props.contactTiming}
      </div>
      <div className={styles.field}>
        <b>Contact Method: </b>
        {props.contactMethod}
      </div>
    </div>
  );
}
