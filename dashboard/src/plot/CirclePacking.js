import { CirclePacking } from "@ant-design/plots";
import React from "react";
import N_number from "./N_number";
export default function CirclePackingChart({
  data_BLA,
  data_acronym_density_BLA,
  groupBy,
  field,
  aggregation,
  density_dict,
  displayData,
  N,
}) {
  return (
    <div>
      <N_number N={N} />
      {aggregation.map((agg) => {
        let data = { children: [] };
        displayData.forEach((element) => {
          let block = {
            name:
              groupBy.length === 1 ? element["key"] : element["key_as_string"],
            value: element[agg + "_" + field]["value"],
          };
          data["children"].push(block);
        });

        console.log("format for circle", data);
        const config = {
          autoFit: true,
          padding: 0,
          data,

          // sizeField: 'r',
          // color: 'rgb(252, 253, 191)-rgb(231, 82, 99)-rgb(183, 55, 121)',
          // 自定义 label 样式
          label: {
            // 偏移
            offsetY: 8,
            style: {
              // fontSize: 12,
              textAlign: "center",
              fill: "rgba(0,0,0,200)",
            },
          },
          // interactions: [
          //   {
          //     type: 'element-selected',
          //   },
          //   {
          //     type: 'element-active',
          //   },
          // ],
          animation: true,
        };

        // return <h1>hello</h1>
        return (
          <div className="chartFill" key={agg}>
          
            <h3>{agg + "_" + field} </h3>
            <CirclePacking {...config} />
            <br />
          </div>
        );
      })}
    </div>
  );
}
