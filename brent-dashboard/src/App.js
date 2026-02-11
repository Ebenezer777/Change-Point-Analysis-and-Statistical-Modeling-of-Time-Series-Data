import React from "react";
import "./App.css";
import PriceChart from "./services/components/PriceChart";

function App() {
  return (
    <div className="App">
      <h1>Brent Oil Price Dashboard</h1>
      <PriceChart />
    </div>
  );
}

export default App;
