import { useEffect, useState } from "react";

const theme = {
  primary: "#0b4f6c",
  secondary: "#1b6ca8",
  background: "#f4f6f8",
  card: "#ffffff",
  border: "#dce1e7"
};

function Dashboard() {
  const [appointments, setAppointments] = useState([]);
  const [noShows, setNoShows] = useState([]);
  const [clinicReport, setClinicReport] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/appointments/upcoming")
      .then(res => res.json())
      .then(setAppointments);

    fetch("http://127.0.0.1:5000/reports/no_show_rate")
      .then(res => res.json())
      .then(setNoShows);

    fetch("http://127.0.0.1:5000/reports/appointments_by_clinic")
      .then(res => res.json())
      .then(setClinicReport);
  }, []);

  return (
    <div style={{ padding: 30, background: theme.background, minHeight: "100vh" }}>
      <h1 style={{ color: theme.primary }}>
        CareConnect – Public Hospital Dashboard
      </h1>

      {/* Upcoming Appointments */}
      <h2>Upcoming Appointments</h2>
      <table style={styles.table}>
        <thead>
          <tr>
            {["Date", "Patient", "Provider", "Clinic", "Status"].map(h => (
              <th key={h} style={styles.th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {appointments.map((a, i) => (
            <tr key={i}>
              <td style={styles.td}>{a.start_datetime}</td>
              <td style={styles.td}>{a.patient}</td>
              <td style={styles.td}>{a.provider}</td>
              <td style={styles.td}>{a.clinic_name}</td>
              <td style={styles.td}>{a.status}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* No-show Rates */}
      <h2 style={{ marginTop: 40 }}>Top No-Show Rates</h2>
      <div style={styles.cardRow}>
        {noShows.map((n, i) => (
          <div key={i} style={styles.card}>
            <strong>Dr. {n.provider}</strong>
            <p>{n.no_show_rate}% no-show rate</p>
          </div>
        ))}
      </div>

      {/* Clinic Summary */}
      <h2 style={{ marginTop: 40 }}>Clinic Summary</h2>
      <div style={styles.cardRow}>
        {clinicReport.map((c, i) => (
          <div key={i} style={styles.card}>
            <h3 style={{ color: theme.primary }}>{c.clinic_name}</h3>
            <p><strong>Total Appointments:</strong> {c.total_appointments}</p>
            <p><strong>No-Shows:</strong> {c.no_shows}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  table: {
    width: "100%",
    background: theme.card,
    borderCollapse: "collapse",
    borderRadius: 8,
    overflow: "hidden"
  },
  th: {
    background: theme.primary,
    color: "white",
    padding: 12,
    textAlign: "left"
  },
  td: {
    padding: 10,
    borderBottom: `1px solid ${theme.border}`
  },
  cardRow: {
    display: "flex",
    gap: 20,
    flexWrap: "wrap"
  },
  card: {
    background: theme.card,
    padding: 20,
    borderRadius: 8,
    width: 260,
    boxShadow: "0 2px 6px rgba(0,0,0,0.08)"
  }
};

export default Dashboard;
