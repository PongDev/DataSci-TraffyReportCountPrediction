import { useState } from "react";
import { PredictButton } from "./PredictButton";

export function PredictContainer() {
  const [predictData, setPredict] = useState({});

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "10vh",
      }}
    >
      <PredictButton setPredict={setPredict} />
    </div>
  );
}
