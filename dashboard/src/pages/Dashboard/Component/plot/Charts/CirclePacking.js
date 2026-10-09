import { CirclePacking } from "@ant-design/plots";
import React from "react";
import N_number from "../Control/N_number";
export default function CirclePackingChart({
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
    <div className="circle packing">
      
      {aggregation.map((agg) => {
        // if (
        //   groupBy.includes(meta.atlas_structure_acronym) &&
        //   field === meta.atlas_structure_acronym &&
        //   agg === meta.aggregation_condition
        // ) {
        //   let data = { children: [] };
        //   let data_density = { children: [] };
        //   displayData.forEach((element) => {
        //     let block = {
        //       name:
        //         groupBy.length === 1
        //           ? element["key"]
        //           : element["key_as_string"],
        //       value: element[agg + "_" + field]["value"],
        //     };
        //     data.children.push(block);
        //     let block_density = { ...block };
        //     let acronym =
        //       groupBy.length === 1
        //         ? element["key"].toString()
        //         : element["key"][
        //             groupBy.indexOf(meta.atlas_structure_acronym)
        //           ];
        //     block_density.value = block.value / acronym_volumn[acronym];
        //     data_density.children.push(block_density);
        //   });

        //   const config = {
        //     autoFit: true,
        //     padding: 0,
        //     data,

        //     // sizeField: 'r',
        //     // color: 'rgb(252, 253, 191)-rgb(231, 82, 99)-rgb(183, 55, 121)',
        //     // 自定义 label 样式
        //     label: {
        //       // 偏移
        //       offsetY: 8,
        //       style: {
        //         // fontSize: 12,
        //         textAlign: "center",
        //         fill: "rgba(0,0,0,200)",
        //       },
        //     },
        //     // interactions: [
        //     //   {
        //     //     type: 'element-selected',
        //     //   },
        //     //   {
        //     //     type: 'element-active',
        //     //   },
        //     // ],
        //     animation: true,
        //   };
        //   const config_density = { ...config };
        //   config_density.data = data_density;

        //   // return <h1>hello</h1>
        //   return (
        //     <div key={agg + "&" + "density" + "_" + field}>
        //       <h3>{agg + "_" + field}</h3>
        //       <CirclePacking {...config} />
        //       <br />
        //       <h3>{"density" + "_" + field}</h3>
        //       <CirclePacking {...config_density} />
        //       <br />
        //     </div>
        //   );
        // } else {

          

          
          let data = { children: [] };

          displayData.forEach((element) => {
            let x_array = []
              groupBy.forEach((gb) => {
                x_array.push(element["key"][gb]);
              });
            let block = {
              
              name: x_array.join("|"),
               
              value: element[agg + "_" + field]["value"],
            };
            data.children.push(block);
          });

          // console.log('format for pie', data)
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
            <div key={agg}>
              <h3 className="chartTitle">{agg + "_" + field}</h3>
              <CirclePacking {...config} />
              <br />
            </div>
          );
        }
      // }
      )}
    </div>
  );
  
}
