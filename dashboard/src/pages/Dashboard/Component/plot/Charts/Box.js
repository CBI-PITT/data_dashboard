import { Box } from "@ant-design/plots";
import N_number from "../Control/N_number";
// import React from 'react';

export default function BoxChart({
  data_BLA,
  data_acronym_density_BLA,
  groupBy,
  field,
  aggregation,
  meta,
  displayData,
  N,
}) {
  let boxplot_data_list = [];
  let boxplot_name = "boxplot" + "_" + field;
  // console.log("boxplot_name",element[boxplot_name])
  console.log(displayData);

  displayData.forEach((element) => {
    let x_array = [];
      groupBy.forEach((gb) => {
        x_array.push(element["key"][gb]);
      });
    let temp = {
      
      x: x_array.join("|"),
      min: element[boxplot_name]["min"],
      q1: element[boxplot_name]["q1"],
      median: element[boxplot_name]["q2"],
      q3: element[boxplot_name]["q3"],
      max: element[boxplot_name]["max"],
    };
    boxplot_data_list.push(temp);
  });
  // console.log("boxplot_data_list", boxplot_data_list);

  const config = {
    width: 400,
    height: 500,
    data: boxplot_data_list,
    xField: "x",
    yField: ["min", "q1", "median", "q3", "max"],
    boxStyle: {
      stroke: "#4C3D3D",
      fill: "#292929",
      fillOpacity: 0.6,
    },
    xAxis: {
      label: {
        autoHide: true,
        autoRotate: true,
        style: {
          fontSize: 18,
        },
      },
    },
    yAxis: {
      label: {
        autoHide: true,
        autoRotate: true,
        style: {
          fontSize: 18,
        },
      },
    },
    animation: true,
  };
  return (
    <div className="chartFill">
      
      <Box {...config} />
    </div>
  );
}
