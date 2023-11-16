import { Area } from "@ant-design/plots";
import React from "react";
import N_number from "./N_number";
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
        autoRotate: false,
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
        <N_number N={N} />
        <Area {...config} />
        <Area {...config_density} />
      </div>
    );
  } else {
    return (
      <div className="chartFill">
        <N_number N={N} />
        <Area {...config} />
      </div>
    );
  }
}
