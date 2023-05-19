import { useState } from "react";
import { PredictButton } from "./PredictButton";

export function PredictContainer() {
  const [prediction, setPrediction] = useState(false);
  const handleUpdate = (values: string) => {
    // Perform the necessary update logic
    console.log(values);
    // setPrediction(false);
  };
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "10vh",
      }}
    >
      <PredictButton handleClick={handleUpdate} />
    </div>
  );
}
