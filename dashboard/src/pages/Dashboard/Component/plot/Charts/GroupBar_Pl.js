import React from "react";
import Plot from "react-plotly.js";

export default function GroupBar({ data ,agg,field}) {
  // Sample data

  // Layout configuration
  
  const layout = {
    barmode: "group", // Stack bars on top of each other
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
    title:"",
    xaxis: {
      type: 'category',
      // Specify the numeric x-axis data as category array
    }
  };

  return (
    <div>
      {data.map((traces, index) => (
        <div key={index} >
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
