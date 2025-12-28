function Landing({ onEnter }) {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>CareConnect</h1>

      <p style={styles.subtitle}>
        A public healthcare scheduling and reporting platform 
        designed to be used by various health clinics in Guyana.
      </p>
      <table style={styles.table}>
      <thead>
        <tr>
          <th style={styles.th}>Group Member Name</th>
          <th style={styles.th}>USI</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style={styles.td}>Tarico Henry</td>
          <td style={styles.td}>US1057554</td>
        </tr>
        <tr>
          <td style={styles.td}>Serina Garrett</td>
          <td style={styles.td}>1046909</td>
        </tr>
        <tr>
          <td style={styles.td}>Tarico Henry</td>
          <td style={styles.td}>1037042</td>
        </tr>
        <tr>
          <td style={styles.td}>Katrina Adams</td>
          <td style={styles.td}>1051923</td>
        </tr>
      </tbody>
    </table>


      <div style={styles.card}>
        <h3>Core Capabilities</h3>
        <ul>
          <li>Appointment scheduling & tracking</li>
          <li>Provider workload management</li>
          <li>No-show and clinic utilization reporting</li>
        </ul>
      </div>

      <button style={styles.button} onClick={onEnter}>
        View Reporting Dashboard
      </button>

      <p style={styles.footer}>
        DBMS Semester Project · MariaDB · Python API · React
      </p>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    background: "linear-gradient(135deg, #0b4f6c, #1b6ca8)",
    color: "white",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
    padding: 20
  },
  title: { fontSize: 48, marginBottom: 10 },
  subtitle: { maxWidth: 600, fontSize: 18 },
  card: {
    background: "rgba(255,255,255,0.15)",
    padding: 20,
    borderRadius: 10,
    marginTop: 30,
    maxWidth: 500,
    textAlign: "left"
  },
  button: {
    marginTop: 30,
    padding: "12px 26px",
    fontSize: 16,
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
    backgroundColor: "#ffffff",
    color: "#0b4f6c",
    fontWeight: "bold"
  },
  footer: {
    marginTop: 40,
    fontSize: 12,
    opacity: 0.85
  },
  table: {
  marginTop: 30,
  borderCollapse: "collapse",
  background: "rgba(255,255,255,0.15)",
  borderRadius: 8,
  overflow: "hidden",
  minWidth: 360
},
th: {
  background: "rgba(0,0,0,0.25)",
  padding: 12,
  color: "white",
  textAlign: "left"
},
td: {
  padding: 10,
  borderTop: "1px solid rgba(255,255,255,0.2)"
}

};

export default Landing;
