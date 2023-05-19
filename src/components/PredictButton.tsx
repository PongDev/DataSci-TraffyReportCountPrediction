import { useEffect, useState } from "react";

type PredictButtonProps = {
  setPrediction: (values: string) => void;
};

export function PredictButton({ handleClick }: PredictButtonProps) {
  const [isHover, setHover] = useState(false);
  // useEffect(() => {
  //   const d3 = document.createElement("script");
  //   d3.async = true;
  //   d3.src = "https://cdn.jsdelivr.net/npm/d3@4.13.0/build/d3.min.js"
  //   document.body.appendChild(d3);

  //   const tau = document.createElement("script");
  //   tau.async = true;
  //   tau.src = "https://cdn.jsdelivr.net/npm/taucharts@2/dist/taucharts.min.js"
  //   document.body.appendChild(tau);

  //   return () => {
  //     document.body.removeChild(d3);
  //     document.body.removeChild(tau);
  //   };
  // },[]);
  // const handleClick = () => {
  //   console.log('You clicked me')
  //   alert('You clicked me!')
  // }
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
      onClick={handleClick}
    >
      Predict!
    </div>
  );
}
