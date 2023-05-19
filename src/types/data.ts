export type PredictData = {
  กรุงธนเหนือ_sidewalk: number;
  กรุงธนเหนือ_light: number;
  กรุงธนเหนือ_road: number;
  กรุงเทพกลาง_sidewalk: number;
  กรุงเทพกลาง_light: number;
  กรุงเทพกลาง_road: number;
  กรุงธนใต้_sidewalk: number;
  กรุงธนใต้_light: number;
  กรุงธนใต้_road: number;
  กรุงเทพตะวันออก_sidewalk: number;
  กรุงเทพตะวันออก_light: number;
  กรุงเทพตะวันออก_road: number;
  กรุงเทพใต้_sidewalk: number;
  กรุงเทพใต้_light: number;
  กรุงเทพใต้_road: number;
  กรุงเทพเหนือ_sidewalk: number;
  กรุงเทพเหนือ_light: number;
  กรุงเทพเหนือ_road: number;
};

export type PastData = {
  date: string;
  region: string;
  obstacle: number;
  canal: number;
  security: number;
  sanitary: number;
  traffic: number;
  road: number;
  sidewalk: number;
  sewer: number;
  flood: number;
  bridge: number;
  electricWire: number;
  light: number;
  tree: number;
};

export type VisualData = {
  pastData: PastData[];
  predictData: PredictData[];
};
