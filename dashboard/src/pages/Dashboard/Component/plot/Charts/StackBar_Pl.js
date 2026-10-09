import React from "react";
import Plot from "react-plotly.js";
import { plotLayout } from "./plotTheme";

export default function StackedBar({ data, type }) {
  data.forEach((element) => {
    element.type = type;
  });
  const layout = plotLayout({
    barmode: "stack",
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
