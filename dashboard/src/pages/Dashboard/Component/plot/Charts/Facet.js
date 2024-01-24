import { Facet} from '@ant-design/plots';
import { DataView } from "@antv/data-set";
import { Button } from '@mui/material';
import React, { useState } from 'react';


// export default function FacetChart({ data_BLA, data_acronym_density_BLA, groupBy, field, aggregation, density_dict,displayData,N}){
//     {
//       console.log(displayData)
//       // return(<h2>Sorry, Its under construction</h2>)
//         // const newData = [
//         //   {
//         //     value_count_atlas_structure_acronym: 42008,
//         //     time_point: "24.0",
//         //     route: "aerosol",
//         //     treatment: "veev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 66922,
//         //     time_point: "24.0",
//         //     route: "subcutaneous",
//         //     treatment: "veev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 4072799,
//         //     time_point: "48.0",
//         //     route: "aerosol",
//         //     treatment: "veev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 311055,
//         //     time_point: "48.0",
//         //     route: "subcutaneous",
//         //     treatment: "veev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 713686,
//         //     time_point: "72.0",
//         //     route: "aerosol",
//         //     treatment: "eeev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 11700626,
//         //     time_point: "72.0",
//         //     route: "aerosol",
//         //     treatment: "veev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 100795,
//         //     time_point: "72.0",
//         //     route: "subcutaneous",
//         //     treatment: "eeev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 1952691,
//         //     time_point: "72.0",
//         //     route: "subcutaneous",
//         //     treatment: "veev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 5875594,
//         //     time_point: "96.0",
//         //     route: "aerosol",
//         //     treatment: "eeev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 4966133,
//         //     time_point: "96.0",
//         //     route: "aerosol",
//         //     treatment: "veev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 48154321,
//         //     time_point: "96.0",
//         //     route: "subcutaneous",
//         //     treatment: "eeev",
//         //   },
//         //   {
//         //     value_count_atlas_structure_acronym: 6635356,
//         //     time_point: "96.0",
//         //     route: "subcutaneous",
//         //     treatment: "veev",
//         //   },
//         // ];
    
//         // const config = {
//         //   // appendPadding: [0, 16, 16, 16],
//         //   data: newData,
//         //   type: "tree",
//         //   fields: ["time_point", "treatment"],
//         //   // coordinate: { type: 'theta' },
    
//         //   // tree-facet 连接线样式和是否平滑
//         //   meta: {
//         //     percent: {
//         //       formatter(val) {
//         //         return (val * 100).toFixed(2) + "%";
//         //       },
//         //     },
//         //   },
//         //   line: {
//         //     style: {
//         //       stroke: "#dedede",
//         //     },
//         //     smooth: false,
//         //   },
//         //   tooltip: {
//         //     showMarkers: false,
//         //   },
//         //   eachView: (view, facet) => {
//         //     //   // 对角线的图形，做数据封箱之后绘制图形
//         //     const dv = new DataView();
//         //     dv.source(facet.data).transform({
//         //       type: "percent",
//         //       field: "value_count_atlas_structure_acronym",
//         //       dimension: "route",
//         //       // as: ['percent'],
//         //     });
//         //     return {
//         //       type: "pie",
//         //       options: {
//         //         data: dv.rows,
//         //         angleField: "value_count_atlas_structure_acronym",
//         //         colorField: "route",
//         //         pieStyle: {
//         //           opacity: 0.85,
//         //         },
//         //         // 添加动画
//         //         animation: true,
//         //         // 添加交互
//         //         interactions: [
//         //           {
//         //             type: "association-element-active",
//         //           },
//         //           {
//         //             type: "association-highlight",
//         //           },
//         //           {
//         //             type: "association-tooltip",
//         //           },
//         //         ],
//         //       },
//         //     };
//         //   },
//         // };
//         // return <Facet {...config} />;
//         // return (
//         //   <div>
//         //   <h1>Under Construction 🚧 </h1>
//         //   </div>
//         // )
//         return (
//           <div>
//             {aggregation.map((agg) => {
//               let data = [];
//               displayData.forEach((element) => {
//                 let block = {};
//                 block[agg + "_" + field] = element[agg + "_" + field]["value"];
//                 if (groupBy.length === 1) {
//                   block[groupBy[0]] = element["key"];
//                 } else {
//                   for (let i = 0; i < groupBy.length; i++) {
//                     block[groupBy[i]] = element["key"][i];
//                   }
//                 }
//                 data.push(block);
//               });
//               // console.log("tree data", data);
//               let config = {
//                 // appendPadding: [0, 16, 16, 16],
//                 data,
//                 type: "tree",
//                 fields: ['sex','treatment','time_point'],
//                 line: {
//                   style: {
//                     stroke: "#dedede",
//                   },
//                   smooth: true,
//                 },
//                 tooltip: {
//                   showMarkers: false,
//                 },
//                 eachView: (view, facet) => {
//                   let dv = new DataView();
//                   dv.source(facet.data).transform({
//                     type: "percent",
//                     field: agg + "_" + field,
//                     dimension: 'atlas_structure_acronym',
//                     // as: 'percent',
//                   });
//                   return {
//                     type: "pie",
//                     options: {
//                       data: dv.rows,
//                       angleField: agg + "_" + field,
//                       colorField: 'atlas_structure_acronym',
//                       pieStyle: {
//                         opacity: 0.85,
//                       },
//                       animation: {},
//                       interactions: [
//                         {
//                           type: "association-active",
//                         },
//                         {
//                           type: "association-tooltip",
//                         },
//                       ],
//                     },
//                   };
//                 },
//               };
//               return (
//                 <div>
//                   <h3>{agg + "_" + field}</h3>
//                   {/* {facetComp(config)} */}
//                   <Facet {...config} key={agg + "_" + field} />
//                   {/* <Button onClick={()=>{
//                     setDimention('route')
//                   }}>dimension</Button>
//                   <Button onClick={()=>{setFields(['treatment','time_point'])}}>fields</Button> */}
                  
//                   <br />
//                 </div>
//               );
//             })}
//           </div>
//         );
//       }
// }


export default function FacetChart  ()  {
  const data = [
    {
      value_count_atlas_structure_acronym: 42008,
      time_point: "24.0",
      route: "aerosol",
      treatment: "veev",
    },
    {
      value_count_atlas_structure_acronym: 66922,
      time_point: "24.0",
      route: "subcutaneous",
      treatment: "veev",
    },
    {
      value_count_atlas_structure_acronym: 4072799,
      time_point: "48.0",
      route: "aerosol",
      treatment: "veev",
    },
    {
      value_count_atlas_structure_acronym: 311055,
      time_point: "48.0",
      route: "subcutaneous",
      treatment: "veev",
    },
    {
      value_count_atlas_structure_acronym: 713686,
      time_point: "72.0",
      route: "aerosol",
      treatment: "eeev",
    },
    {
      value_count_atlas_structure_acronym: 11700626,
      time_point: "72.0",
      route: "aerosol",
      treatment: "veev",
    },
    {
      value_count_atlas_structure_acronym: 100795,
      time_point: "72.0",
      route: "subcutaneous",
      treatment: "eeev",
    },
    {
      value_count_atlas_structure_acronym: 1952691,
      time_point: "72.0",
      route: "subcutaneous",
      treatment: "veev",
    },
    {
      value_count_atlas_structure_acronym: 5875594,
      time_point: "96.0",
      route: "aerosol",
      treatment: "eeev",
    },
    {
      value_count_atlas_structure_acronym: 4966133,
      time_point: "96.0",
      route: "aerosol",
      treatment: "veev",
    },
    {
      value_count_atlas_structure_acronym: 48154321,
      time_point: "96.0",
      route: "subcutaneous",
      treatment: "eeev",
    },
    {
      value_count_atlas_structure_acronym: 6635356,
      time_point: "96.0",
      route: "subcutaneous",
      treatment: "veev",
    },
  ];

 
  const config = {
    type: 'tree',
  fields: ['time_point','route'],
  cols: 3,
  // 超过3个换行
  padding: [0, 10, 10],
  appendPadding: 30,
  data,
  axes: {},
  meta: {
    carat: {
      sync: true,
    },
    price: {
      sync: true,
    },
    cut: {
      // 设置 sync 同步之后，可以按照 'cut' 进行颜色映射分类
      sync: true,
    },
  },
  eachView: (view, f) => {
    return {
      type: 'pie',
      options: {
        data: f.data,
        angleField: 'value_count_atlas_structure_acronym',
        colorField: 'treatment',
        radius: 0.8,
        label: {
          type: 'inner',
          offset: '-50%',
          content: '{value}',
          style: {
            textAlign: 'center',
          },
        },
        interactions: [
          { type: 'element-selected' },
          { type: 'element-active' },
        ],
      },
    };
  },
  };

  return <Facet {...config} />;
};