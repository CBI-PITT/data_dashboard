import { Line } from "@ant-design/plots";
import React from "react";
import N_number from "./N_number";
export default function LineChart({
  data_BLA,
  data_acronym_density_BLA,
  groupBy,
  field,
  aggregation,
  density_dict,
  N,
}) {
  const config = {
    data: data_BLA,
    xField: "X_axis",
    yField: "value",
    seriesField: "type",
    smooth: true,
    point: {
      size: 5,
      style: {
        lineWidth: 1,
        fillOpacity: 1,
      },
      shape: "circle",
    },
    slider: {
      start: 0,
      end: 1,
    },
    xAxis: {
      label: {
        autoHide: true,
        autoRotate: false,
      },
    },
  };

  if (
    groupBy.includes(density_dict.atlas_structure_acronym) &&
    field === density_dict.atlas_structure_acronym &&
    aggregation.includes(density_dict.aggregation_choice_forDensity)
  ) {
    let config_density = { ...config };
    config_density.data = data_acronym_density_BLA;
    return (
      <div className="chartFill">
        <N_number N={N} />
        <Line {...config} />
        <Line {...config_density} />
      </div>
    );
  } else {
    return (
      <div className="chartFill">
        <N_number N={N} />
        <Line {...config} />
      </div>
    );
  }
}
