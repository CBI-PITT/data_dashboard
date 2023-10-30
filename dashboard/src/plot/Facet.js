import { Facet} from '@ant-design/plots';
import { DataView } from "@antv/data-set";
import React from 'react';

export default function FacetChart({ data_BLA, data_acronym_density_BLA, groupBy, field, aggregation, density_dict,displayData }){
    {
        // const newData = [
        //   {
        //     value_count_atlas_structure_acronym: 42008,
        //     time_point: "24.0",
        //     route: "aerosol",
        //     treatment: "veev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 66922,
        //     time_point: "24.0",
        //     route: "subcutaneous",
        //     treatment: "veev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 4072799,
        //     time_point: "48.0",
        //     route: "aerosol",
        //     treatment: "veev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 311055,
        //     time_point: "48.0",
        //     route: "subcutaneous",
        //     treatment: "veev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 713686,
        //     time_point: "72.0",
        //     route: "aerosol",
        //     treatment: "eeev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 11700626,
        //     time_point: "72.0",
        //     route: "aerosol",
        //     treatment: "veev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 100795,
        //     time_point: "72.0",
        //     route: "subcutaneous",
        //     treatment: "eeev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 1952691,
        //     time_point: "72.0",
        //     route: "subcutaneous",
        //     treatment: "veev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 5875594,
        //     time_point: "96.0",
        //     route: "aerosol",
        //     treatment: "eeev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 4966133,
        //     time_point: "96.0",
        //     route: "aerosol",
        //     treatment: "veev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 48154321,
        //     time_point: "96.0",
        //     route: "subcutaneous",
        //     treatment: "eeev",
        //   },
        //   {
        //     value_count_atlas_structure_acronym: 6635356,
        //     time_point: "96.0",
        //     route: "subcutaneous",
        //     treatment: "veev",
        //   },
        // ];
    
        // const config = {
        //   // appendPadding: [0, 16, 16, 16],
        //   data: newData,
        //   type: "tree",
        //   fields: ["time_point", "treatment"],
        //   // coordinate: { type: 'theta' },
    
        //   // tree-facet 连接线样式和是否平滑
        //   meta: {
        //     percent: {
        //       formatter(val) {
        //         return (val * 100).toFixed(2) + "%";
        //       },
        //     },
        //   },
        //   line: {
        //     style: {
        //       stroke: "#dedede",
        //     },
        //     smooth: false,
        //   },
        //   tooltip: {
        //     showMarkers: false,
        //   },
        //   eachView: (view, facet) => {
        //     //   // 对角线的图形，做数据封箱之后绘制图形
        //     const dv = new DataView();
        //     dv.source(facet.data).transform({
        //       type: "percent",
        //       field: "value_count_atlas_structure_acronym",
        //       dimension: "route",
        //       // as: ['percent'],
        //     });
        //     return {
        //       type: "pie",
        //       options: {
        //         data: dv.rows,
        //         angleField: "value_count_atlas_structure_acronym",
        //         colorField: "route",
        //         pieStyle: {
        //           opacity: 0.85,
        //         },
        //         // 添加动画
        //         animation: true,
        //         // 添加交互
        //         interactions: [
        //           {
        //             type: "association-element-active",
        //           },
        //           {
        //             type: "association-highlight",
        //           },
        //           {
        //             type: "association-tooltip",
        //           },
        //         ],
        //       },
        //     };
        //   },
        // };
        // return <Facet {...config} />;
    
        return (
          <div>
            {aggregation.map((agg) => {
              let data = [];
              displayData.forEach((element) => {
                let block = {};
                block[agg + "_" + field] = element[agg + "_" + field]["value"];
                if (groupBy.length === 1) {
                  block[groupBy[0]] = element["key"];
                } else {
                  for (let i = 0; i < groupBy.length; i++) {
                    block[groupBy[i]] = element["key"][i];
                  }
                }
                data.push(block);
              });
              console.log("tree data", data);
              let config = {
                // appendPadding: [0, 16, 16, 16],
                data,
                type: "tree",
                fields: ["time_point", "treatment"],
                line: {
                  style: {
                    stroke: "#dedede",
                  },
                  smooth: true,
                },
                tooltip: {
                  showMarkers: false,
                },
                eachView: (view, facet) => {
                  let dv = new DataView();
                  dv.source(facet.data).transform({
                    type: "percent",
                    field: agg + "_" + field,
                    dimension: "route",
                    // as: 'percent',
                  });
                  return {
                    type: "pie",
                    options: {
                      data: dv.rows,
                      angleField: agg + "_" + field,
                      colorField: "route",
                      pieStyle: {
                        opacity: 0.85,
                      },
                      animation: {},
                      interactions: [
                        {
                          type: "association-active",
                        },
                        {
                          type: "association-tooltip",
                        },
                      ],
                    },
                  };
                },
              };
              return (
                <div>
                  <h3>{agg + "_" + field}</h3>
                  <Facet {...config} key={agg + "_" + field} />
                  <br />
                </div>
              );
            })}
          </div>
        );
      }
}