import { useEffect, useState } from "react";

function Dashboard() {
  const [appointments, setAppointments] = useState([]);
  const [noShows, setNoShows] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/appointments/upcoming")
      .then(res => res.json())
      .then(setAppointments);

    fetch("http://localhost:5000/reports/no_show_rate")
      .then(res => res.json())
      .then(setNoShows);
  }, []);

  return (
    <div style={styles.page}>
      <h1>CareConnect Dashboard</h1>

      <section style={styles.section}>
        <h2>Upcoming Appointments</h2>
        <table style={styles.table}>
          <thead>
            <tr>
              <th>Date</th>
              <th>Patient</th>
              <th>Provider</th>
              <th>Clinic</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {appointments.map((a, i) => (
              <tr key={i}>
                <td>{a.start_datetime}</td>
                <td>{a.patient}</td>
                <td>{a.provider}</td>
                <td>{a.clinic_name}</td>
                <td>{a.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section style={styles.section}>
        <h2>Top No-Show Rates</h2>
        <div style={styles.cards}>
          {noShows.map((n, i) => (
            <div key={i} style={styles.card}>
              <strong>Dr. {n.provider}</strong>
              <p>{n.no_show_rate}% no-show rate</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

const styles = {
  page: { padding: 30, fontFamily: "Arial", background: "#f4f6f8" },
  section: { marginBottom: 40 },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    background: "white"
  },
  cards: { display: "flex", gap: 20, flexWrap: "wrap" },
  card: {
    background: "white",
    padding: 20,
    borderRadius: 8,
    minWidth: 200,
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
  }
};

export default Dashboard;
