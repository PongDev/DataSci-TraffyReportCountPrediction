import { useState } from "react";
import { PredictButton } from "./PredictButton";
import { VisualData } from "../types/data";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { regions } from "../types/consts";
import { getPredictData, mapColorRegions } from "../util/helper";

export function PredictContainer() {
  const [visualData, setVisualData] = useState<VisualData>({
    pastData: [],
    predictData: [],
  });

  const updateVisualData = async () => {
    setVisualData({
      pastData: await (await fetch("/get_data")).json(),
      predictData: await (await fetch("/predict")).json(),
    });
  };

  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );
  let chartDatas: JSX.Element[] = [];
  const chartTypes = ["sidewalk", "light", "road"];
  if (visualData.pastData.length >= 7 && visualData.predictData.length >= 3) {
    let i = 0;
    for (const chartType of chartTypes) {
      const chartOptions = {
        responsive: true,
        plugins: {
          legend: {
            position: "top" as const,
          },
          title: {
            display: true,
            text: chartType,
          },
        },
      };

      const dataDates: string[] = ["", "", "", "", "", "", "", "", "", ""];
      const dataSets: any[] = [];
      for (let idx = 0; idx < regions.length; idx++) {
        const data: number[] = [];
        for (let day = 0; day < 7; day++) {
          switch (chartType) {
            case "sidewalk":
              data.push(visualData.pastData[day * 6 + idx].sidewalk);
              break;
            case "light":
              data.push(visualData.pastData[day * 6 + idx].light);
              break;
            case "road":
              data.push(visualData.pastData[day * 6 + idx].road);
              break;
          }
          dataDates[day] = visualData.pastData[day * 6 + idx].date;
        }
        for (let day = 0; day < 3; day++) {
          data.push(
            getPredictData(visualData.predictData[day], chartType, idx)
          );
          dataDates[day + 7] = `Predict Day ${day}`;
        }
        dataSets.push({
          label: regions[idx],
          data: data,
          backgroundColor: mapColorRegions(regions[idx]),
        });
      }
      const chartData = {
        labels: dataDates,
        datasets: dataSets,
      };
      chartDatas.push(
        <Line options={chartOptions} data={chartData} key={`graph_${i}`} />
      );
      i += 1;
    }
  }

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        padding: "10px",
      }}
    >
      <div>
        <PredictButton updateVisualData={updateVisualData} />
      </div>
      <div>{chartDatas}</div>
    </div>
  );
}
