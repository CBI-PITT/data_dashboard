import React from "react";
import Plot from "react-plotly.js";

export default function Area({ data,type,fill }) {
  // Sample data

  // Layout configuration
  data.forEach(element => {
    element.type = type
    element.fill = 'tozeroy'
  });
  const layout = {
   
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
