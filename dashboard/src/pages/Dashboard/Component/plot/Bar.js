import { Column } from "@ant-design/plots";
import React from "react";
import N_number from "./N_number";
export default function BarChart({
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
    isStack: true,
    xField: "X_axis",
    yField: "value",
    seriesField: "type",

    // label: {
    //   // 可手动配置 label 数据标签位置
    //   position: 'middle',
    //   // 'top', 'bottom', 'middle'
    //   // 可配置附加的布局方法
    //   layout: [
    //     // 柱形图数据标签位置自动调整
    //     {
    //       type: 'interval-adjust-position',
    //     }, // 数据标签防遮挡
    //     {
    //       type: 'interval-hide-overlap',
    //     }, // 数据标签文颜色自动调整
    //     {
    //       type: 'adjust-color',
    //     },
    //   ],
    // },
    legend: {
      position: "top", // Set the legend position to "top"
    },
    xAxis: {
      label: {
        autoHide: true,
        autoRotate: true,
        // style: {
        //   fontSize: 20,
        // },
      },
    },
    // yAxis: {
    //     label: {
    //       autoHide: true,
    //       autoRotate: true,
    //       style: {
    //         fontSize: 20,
    //       },
    //     },
    //   },
    slider: {
      start: 0,
      end: 1,
    },
    interactions: [
      {
        // type: 'active-region',
        // type: 'element-highlight',
        type: "element-active",
        // enable: true,
      },
    ],
  };

  if (
    groupBy.includes(meta.atlas_structure_acronym) &&
    field === meta.atlas_structure_acronym &&
    aggregation.includes(meta.aggregation_condition)
  ) {
    let config_density = { ...config };
    config_density.data = data_acronym_density_BLA;

    return (
      <div className="chartFill">
        <N_number N={N} />
        <Column {...config} />
        <Column {...config_density} />
      </div>
    );
  } else {
    return (
      <div className="chartFill">
        <N_number N={N} />
        <Column {...config} />{" "}
      </div>
    );
  }
}
