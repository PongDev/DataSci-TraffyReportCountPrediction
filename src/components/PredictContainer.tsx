import { useState } from "react";
import { PredictButton } from "./PredictButton";
import { PredictData } from "../types/PredictData";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

export function PredictContainer() {
  const [predictData, setPredict] = useState<PredictData[]>([]);

  const updatePredictData = async () => {
    const res = await fetch("/predict");
    const data: PredictData[] = await res.json();
    setPredict(data);
  };

  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );
  const chartLabels = ["sidewalk", "light", "road"];
  let chartDatas = [];
  let i = 0;
  for (const e of predictData) {
    const chartOptions = {
      responsive: true,
      plugins: {
        legend: {
          position: "top" as const,
        },
        title: {
          display: true,
          text: `Day ${i}`,
        },
      },
    };
    const chartData = {
      labels: chartLabels,
      datasets: [
        {
          label: "กรุงธนเหนือ",
          data: [
            e.กรุงธนเหนือ_sidewalk,
            e.กรุงธนเหนือ_light,
            e.กรุงธนเหนือ_road,
          ],
          backgroundColor: "rgba(255, 99, 99, 0.5)",
        },
        {
          label: "กรุงเทพกลาง",
          data: [
            e.กรุงเทพกลาง_sidewalk,
            e.กรุงเทพกลาง_light,
            e.กรุงเทพกลาง_road,
          ],
          backgroundColor: "rgba(235, 223, 53, 0.5)",
        },
        {
          label: "กรุงธนใต้",
          data: [e.กรุงธนใต้_sidewalk, e.กรุงธนใต้_light, e.กรุงธนใต้_road],
          backgroundColor: "rgba(68, 235, 53, 0.5)",
        },
        {
          label: "กรุงเทพตะวันออก",
          data: [
            e.กรุงเทพตะวันออก_sidewalk,
            e.กรุงเทพตะวันออก_light,
            e.กรุงเทพตะวันออก_road,
          ],
          backgroundColor: "rgba(53, 232, 235, 0.5)",
        },
        {
          label: "กรุงเทพใต้",
          data: [e.กรุงเทพใต้_sidewalk, e.กรุงเทพใต้_light, e.กรุงเทพใต้_road],
          backgroundColor: "rgba(114, 53, 235, 0.5)",
        },
        {
          label: "กรุงเทพเหนือ",
          data: [
            e.กรุงเทพเหนือ_sidewalk,
            e.กรุงเทพเหนือ_light,
            e.กรุงเทพเหนือ_road,
          ],
          backgroundColor: "rgba(235, 53, 174, 0.5)",
        },
      ],
    };
    chartDatas.push(
      <Bar options={chartOptions} data={chartData} key={`graph_${i}`} />
    );
    i += 1;
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
        <PredictButton updatePredictData={updatePredictData} />
      </div>
      <div>{chartDatas}</div>
    </div>
  );
}
