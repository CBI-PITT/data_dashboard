import { Pie } from "@ant-design/plots";
import React from "react";
import N_number from "./N_number";
import Typography from '@mui/material/Typography';
export default function PieChart({
  data_BLA,
  data_acronym_density_BLA,
  groupBy,
  field,
  aggregation,
  meta,
  displayData,
  N,
  acronym_volumn
}) {
  return (
    <div className="pie">
      <N_number N={N} />
      {aggregation.map((agg) => {
        if (
          groupBy.includes(meta.atlas_structure_acronym) &&
          field === meta.atlas_structure_acronym &&
          agg === meta.aggregation_condition
        ) {
          let data = []
          let data_density = []
          displayData.forEach((element) => {
            let block = {
              type:
                groupBy.length === 1
                  ? element["key"]
                  : element["key_as_string"],
              value: element[agg + "_" + field]["value"],
            };
            data.push(block);
            let block_density = {...block}
            let acronym =
            groupBy.length === 1
              ? element["key"].toString()
              : element["key"][groupBy.indexOf(meta.atlas_structure_acronym)];
            block_density.value = block.value/acronym_volumn[acronym]
            data_density.push(block_density)
          });

          console.log('format for pie: data', data)
          console.log('format for pie: data_density', data_density)
          const config = {
            appendPadding: 10,
            data,
            // theme:'dark',
            angleField: "value",
            colorField: "type",
            radius: 0.9,
            label: {
              type: "spider",
              labelHeight: 28,
              content: "{name}\n{percentage}",
              layout: [
                // 柱形图数据标签位置自动调整
                // 数据标签防遮挡
                // {
                //   type: 'interval-hide-overlap',
                // }, // 数据标签文颜色自动调整
                // {
                //   type: 'adjust-color',
                // },
              ],
            },
            interactions: [
              {
                type: "element-selected",
              },
              {
                type: "element-active",
              },
            ],
          };
          const config_density = {...config}
          config_density.data = data_density

          // return <h1>hello</h1>
          return (
            <div key={agg + '&' + "density" + "_" + field}>
              <h3>{agg + "_" + field}</h3>
              <Pie {...config} />
              <br />
              <h3>{"density" + "_" + field}</h3>
              <Pie {...config_density} />
              <br />
            </div>
          );
        } else {
          let data = [];

          displayData.forEach((element) => {
            let block = {
              type:
                groupBy.length === 1
                  ? element["key"]
                  : element["key_as_string"],
              value: element[agg + "_" + field]["value"],
            };
            data.push(block);
          });

          // console.log('format for pie', data)
          const config = {
            appendPadding: 10,
            data,
            // theme:'dark',
            angleField: "value",
            colorField: "type",
            radius: 0.9,
            label: {
              type: "spider",
              labelHeight: 28,
              content: "{name}\n{percentage}",
              layout: [
                // 柱形图数据标签位置自动调整
                // 数据标签防遮挡
                // {
                //   type: 'interval-hide-overlap',
                // }, // 数据标签文颜色自动调整
                // {
                //   type: 'adjust-color',
                // },
              ],
            },
            interactions: [
              {
                type: "element-selected",
              },
              {
                type: "element-active",
              },
            ],
          };

          // return <h1>hello</h1>
          return (
            <div key={agg}>
              <h3>{agg + "_" + field}</h3>
              <Pie {...config} />
              <br />
            </div>
          );
        }
      })}
    </div>
  );
}
