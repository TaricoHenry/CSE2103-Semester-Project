import { useState } from "react";
import Landing from "./Landing";
import Dashboard from "./Dashboard";

function App() {
  const [page, setPage] = useState("landing");

  return (
    <>
      {page === "landing" && <Landing onEnter={() => setPage("dashboard")} />}
      {page === "dashboard" && <Dashboard />}
    </>
  );
}

export default App;
