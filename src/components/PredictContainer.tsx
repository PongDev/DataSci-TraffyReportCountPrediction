import { PredictButton } from "./PredictButton";

export function PredictContainer() {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "10vh",
      }}
    >
      <PredictButton />
    </div>
  );
}
