import { Area } from "@ant-design/plots";
import React from "react";
import N_number from "../Control/N_number";
export default function AreaChart({
  data_BLA,
  data_acronym_density_BLA,
  groupBy,
  field,
  aggregation,
  meta,
  N,
}) {
  const config = {
    data: data_BLA,
    xField: "X_axis",
    yField: "value",
    seriesField: "type",
    smooth: true,
    
    slider: {
      start: 0,
      end: 1,
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
    legend: {
      
      itemName: {
        style: {
          fontSize: 16, // Set legend item text size to 16 (adjust as needed)
        },
      },
    },
  };

  if (
    groupBy.includes(meta.atlas_structure_acronym) &&
    field === meta.atlas_structure_acronym &&
    aggregation.includes(meta.aggregation_condition)
  ) {
    let config_density = { ...config };
    config_density.data = data_acronym_density_BLA;
    config_density.smooth = false;
    return (
      <div className="chartFill">
        
        <Area {...config} />
        <br></br>
        <Area {...config_density} />
      </div>
    );
  } else {
    return (
      <div className="chartFill">
        
        <Area {...config} />
      </div>
    );
  }
}
