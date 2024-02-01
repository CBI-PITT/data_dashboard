import React from "react";
import Plot from "react-plotly.js";

export default function StackedBar({ data,type }) {
  // Sample data

  // Layout configuration
  data.forEach(element => {
    element.type = type
  });
  const layout = {
    barmode: "stack", // Stack bars on top of each other
    // title: "Stacked Bar Chart with Error Bars",
    legend: {
      x: 0, // Adjust the x-coordinate for the legend
      y: 1, // Adjust the y-coordinate for the legend
      orientation: "h",
      font: {
        size: 14, // Increase the font size of the legend
      },
    },
    font: {
      size: 16, // Increase the overall font size of the chart layout
    },
   
  };

  return (
    <Plot
      data={data}
      layout={layout}
      style={{ width: "100%", height: "100%" }}
    />
  );
}
