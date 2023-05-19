import { PredictData } from "../types/data";

export function getPredictData(
  predictData: PredictData,
  type: string,
  regionIndex: number
): number {
  if (type == "sidewalk") {
    switch (regionIndex) {
      case 0:
        return predictData.กรุงธนเหนือ_sidewalk;
      case 1:
        return predictData.กรุงธนใต้_sidewalk;
      case 2:
        return predictData.กรุงเทพกลาง_sidewalk;
      case 3:
        return predictData.กรุงเทพตะวันออก_sidewalk;
      case 4:
        return predictData.กรุงเทพเหนือ_sidewalk;
      case 5:
        return predictData.กรุงเทพใต้_sidewalk;
    }
  } else if (type == "light") {
    switch (regionIndex) {
      case 0:
        return predictData.กรุงธนเหนือ_light;
      case 1:
        return predictData.กรุงธนใต้_light;
      case 2:
        return predictData.กรุงเทพกลาง_light;
      case 3:
        return predictData.กรุงเทพตะวันออก_light;
      case 4:
        return predictData.กรุงเทพเหนือ_light;
      case 5:
        return predictData.กรุงเทพใต้_light;
    }
  } else if (type == "road") {
    switch (regionIndex) {
      case 0:
        return predictData.กรุงธนเหนือ_road;
      case 1:
        return predictData.กรุงธนใต้_road;
      case 2:
        return predictData.กรุงเทพกลาง_road;
      case 3:
        return predictData.กรุงเทพตะวันออก_road;
      case 4:
        return predictData.กรุงเทพเหนือ_road;
      case 5:
        return predictData.กรุงเทพใต้_road;
    }
  }
  return 0;
}

export function mapColorRegions(key: string): string {
  switch (key) {
    case "กรุงธนเหนือ":
      return "rgb(255, 99, 99)";
    case "กรุงธนใต้":
      return "rgb(68, 235, 53)";
    case "กรุงเทพกลาง":
      return "rgb(235, 223, 53)";
    case "กรุงเทพตะวันออก":
      return "rgb(53, 232, 235)";
    case "กรุงเทพเหนือ":
      return "rgb(114, 53, 235)";
    case "กรุงเทพใต้":
      return "rgb(235, 53, 174)";
  }
  return "rgb(0, 0, 0)";
}
