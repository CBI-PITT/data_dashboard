import { Box} from '@ant-design/plots';

// import React from 'react';

export default function BoxChart({ data_BLA, data_acronym_density_BLA, groupBy, field, aggregation, density_dict,displayData }){
    let boxplot_data_list = [];
    let boxplot_name = "boxplot" + "_" + field;
    // console.log("boxplot_name",element[boxplot_name])
    console.log(displayData);

    displayData.forEach((element) => {
      let temp = {
        x: groupBy.length === 1 ? element["key"] : element["key_as_string"],
        min: element[boxplot_name]["min"],
        q1: element[boxplot_name]["q1"],
        median: element[boxplot_name]["q2"],
        q3: element[boxplot_name]["q3"],
        max: element[boxplot_name]["max"],
      };
      boxplot_data_list.push(temp);
    });
    console.log("boxplot_data_list", boxplot_data_list);

    const config = {
      width: 400,
      height: 500,
      data: boxplot_data_list,
      xField: "x",
      yField: ["min", "q1", "median", "q3", "max"],
      boxStyle: {
        stroke: "#545454",
        fill: "#292929",
        fillOpacity: 0.6,
      },
      animation: true,
    };
    return <Box {...config} />;
}