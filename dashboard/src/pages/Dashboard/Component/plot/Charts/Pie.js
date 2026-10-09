import { Pie } from "@ant-design/plots";
import React from "react";
import N_number from "../Control/N_number";
import Typography from "@mui/material/Typography";
export default function PieChart({
  data_BLA,
  data_acronym_density_BLA,
  groupBy,
  field,
  aggregation,
  meta,
  displayData,
  N,
  acronym_volumn,
}) {
  return (
    <div className="pie">
      {aggregation.map(
        (agg) => {
          // if (
          //   groupBy.includes(meta.atlas_structure_acronym) &&
          //   field === meta.atlas_structure_acronym &&
          //   agg === meta.aggregation_condition
          // ) {
          //   let data = []
          //   let data_density = []
          //   displayData.forEach((element) => {
          //     let block = {
          //       type:
          //         groupBy.length === 1
          //           ? element["key"]
          //           : element["key_as_string"],
          //       value: element[agg + "_" + field]["value"],
          //     };
          //     data.push(block);
          //     let block_density = {...block}
          //     let acronym =
          //     groupBy.length === 1
          //       ? element["key"].toString()
          //       : element["key"][groupBy.indexOf(meta.atlas_structure_acronym)];
          //     if(acronym_volumn[acronym]){
          //       block_density.value = block.value/acronym_volumn[acronym]
          //     }
          //     else{
          //       block_density.value =0
          //     }
          //     data_density.push(block_density)
          //   });

          //   // console.log('format for pie: data', data)
          //   // console.log('format for pie: data_density', data_density)
          //   const config = {
          //     appendPadding: 10,
          //     data,
          //     // theme:'dark',
          //     angleField: "value",
          //     colorField: "type",
          //     radius: 0.9,
          //     label: {
          //       type: "spider",
          //       labelHeight: 28,
          //       content: "{name}\n{percentage}",
          //       style: {
          //         fill: '#111111', // Set fill to black for labels
          //         fontSize:15
          //       },
          //       layout: [
          //         // 柱形图数据标签位置自动调整
          //         // 数据标签防遮挡
          //         // {
          //         //   type: 'interval-hide-overlap',
          //         // }, // 数据标签文颜色自动调整
          //         // {
          //         //   type: 'adjust-color',
          //         // },
          //       ]
          //     },
          //     legend: {
          //       layout: 'vertical',
          //       position: 'right',
          //       itemName: {
          //         style: {
          //           // fill: '#111111', // 将图例文本颜色设置为黑色
          //           fontSize:20
          //         },
          //       },
          //     },
          //     interactions: [
          //       {
          //         type: "element-selected",
          //       },
          //       {
          //         type: "element-active",
          //       },
          //     ],
          //   };
          //   const config_density = {...config}
          //   config_density.data = data_density
          //   // config_density.data = data_acronym_density_BLA
          //   // config_density.angleField = 'value'
          //   // config_density.colorField = 'X_axis'

          //   // return <h1>hello</h1>
          //   return (
          //     <div key={agg + '&' + "density" + "_" + field}>
          //       <h3>{agg + "_" + field}</h3>
          //       <Pie {...config} />
          //       <br />
          //       <h3>{"density" + "_" + field}</h3>
          //       <Pie {...config_density} />
          //       <br />
          //     </div>
          //   );
          // } else {
          let data = [];

          displayData.forEach((element) => {
            let x_array = []
              groupBy.forEach((gb) => {
                x_array.push(element["key"][gb]);
              });
            let block = {
              
              type: x_array.join("|"),
               
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
              style: {
                fill: "#111111", // Set fill to black for labels
                fontSize: 15,
              },
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
            legend: {
              layout: "vertical",
              position: "right",
              itemName: {
                style: {
                  // fill: '#111111', // 将图例文本颜色设置为黑色
                  fontSize: 20,
                },
              },
            },
          };

          // return <h1>hello</h1>
          return (
            <div key={agg} >
              <h3 className="chartTitle">{agg + "_" + field}</h3>
              <Pie {...config} />
              <br />
            </div>
          );
        }
        // }
      )}
    </div>
  );
}
