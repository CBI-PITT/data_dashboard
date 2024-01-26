import { Column } from "@ant-design/plots";
import React from "react";
import N_number from "../Control/N_number";
export default function StackBarChart({
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
    // isGroup: true,
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

    columnStyle: {
      // radius: [20, 20, 0, 0],
      stroke: "#1890ff",
      // opacity: 0.8,
    },
    legend: {
      position: "top-left",

      itemName: {
        style: {
          fontSize: 18, // 将图例文本大小设置为16（根据需要调整）
        },
      },
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

  // if (
  //   groupBy.includes(meta.atlas_structure_acronym) &&
  //   field === meta.atlas_structure_acronym &&
  //   aggregation.includes(meta.aggregation_condition)
  // ) {
  //   let config_density = { ...config };
  //   config_density.data = data_acronym_density_BLA;
  //   config_density.smooth = false;
  //   return (
  //     <div className="chartFill">
        
  //       <Column {...config} />
  //       <br></br>
  //       <Column {...config_density} />
  //     </div>
  //   );
  // } else {
    return (
      <div className="chartFill">
        
        <Column {...config} />
      </div>
    );
  // }
}
