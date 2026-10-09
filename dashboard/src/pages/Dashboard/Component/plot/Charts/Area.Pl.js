import React from "react";
import Plot from "react-plotly.js";
import { plotLayout } from "./plotTheme";

export default function Area({ data, type, fill }) {
  data.forEach((element) => {
    element.type = type;
    element.fill = "tozeroy";
  });
  const layout = plotLayout({
    legend: {
      x: 0,
      y: 1,
      orientation: "h",
    },
    xaxis: { type: "category" },
  });

  return (
    <Plot
      data={data}
      layout={layout}
      style={{ width: "100%", height: "90%" }}
    />
  );
}
