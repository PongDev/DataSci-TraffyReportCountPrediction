import { useState } from "react";

export function PredictButton() {
  const [isHover, setHover] = useState(false);

  const extraStyle = isHover
    ? {
        backgroundColor: "#005a9e",
        color: "white",
      }
    : {
        backgroundColor: "#0078d4",
        color: "#ffd21f",
      };

  return (
    <div
      style={{
        display: "inline-block",
        padding: "5px 10px",
        border: "1px solid #0078d4",
        borderRadius: "5px",
        transition: "all 0.2s ease",
        cursor: "pointer",
        ...extraStyle,
      }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      Predict!
    </div>
  );
}
