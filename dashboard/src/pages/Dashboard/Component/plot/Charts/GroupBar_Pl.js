import React from "react";
import Plot from "react-plotly.js";
import { plotLayout } from "./plotTheme";

export default function GroupBar({ data, agg, field }) {
  const layout = plotLayout({
    barmode: "group",
    legend: {
      x: 0,
      y: 1,
      orientation: "h",
    },
    xaxis: { type: "category" },
  });

  return (
    <div>
      {data.map((traces, index) => (
        <div key={index}>
          <Plot
            data={traces}
            layout={{
              ...layout,
              title: `${agg[index]} _ ${field}`, // Set title dynamically
            }}
            style={{ width: "100%", height: "100%" }}
          />
        </div>
      ))}
    </div>
  );
}
