function Landing({ onEnter }) {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>CareConnect</h1>
      <p style={styles.subtitle}>
        A lightweight healthcare scheduling and reporting platform inspired by
        Salesforce Health Cloud.
      </p>

      <div style={styles.card}>
        <h3>What CareConnect Solves</h3>
        <ul>
          <li>Reduces overcrowded clinics</li>
          <li>Improves appointment scheduling</li>
          <li>Tracks no-shows and provider workload</li>
        </ul>
      </div>

      <button style={styles.button} onClick={onEnter}>
        View Dashboard
      </button>

      <p style={styles.footer}>
        DBMS Semester Project · MariaDB · React · Python API
      </p>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    background: "linear-gradient(135deg, #1e3c72, #2a5298)",
    color: "white",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
    textAlign: "center"
  },
  title: { fontSize: 48, marginBottom: 10 },
  subtitle: { fontSize: 18, maxWidth: 600 },
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
    padding: "12px 24px",
    fontSize: 16,
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
    backgroundColor: "#ffffff",
    color: "#1e3c72",
    fontWeight: "bold"
  },
  footer: { marginTop: 40, fontSize: 12, opacity: 0.8 }
};

export default Landing;
