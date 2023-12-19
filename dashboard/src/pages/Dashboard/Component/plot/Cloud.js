import { WordCloud } from "@ant-design/plots";
import React from "react";
import N_number from "./N_number";
export default function CloudChart({
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
    <div className="cloud">
      <N_number N={N} />
      {aggregation.map((agg) => {
        if (
          groupBy.includes(meta.atlas_structure_acronym) &&
          field === meta.atlas_structure_acronym &&
          agg === meta.aggregation_condition
        ) {
          let data = [];
          let data_density = [];
          displayData.forEach((element) => {
            let block = {
              type:
                groupBy.length === 1
                  ? element["key"]
                  : element["key_as_string"],
              value: element[agg + "_" + field]["value"],
            };
            data.push(block);
            let block_density = { ...block };
            let acronym =
              groupBy.length === 1
                ? element["key"].toString()
                : element["key"][
                    groupBy.indexOf(meta.atlas_structure_acronym)
                  ];
            block_density.value = block.value / acronym_volumn[acronym];
            data_density.push(block_density);
          });

          console.log("format for pie: data", data);
          console.log("format for pie: data_density", data_density);
          const config = {
            data,
            wordField: "type",
            weightField: "value",
            color: "#122c6a",
            // colorField: 'type',
            wordStyle: {
              fontFamily: "Verdana",
              // fontSize: [24, 50],
              rotation: 0,
            },
            // 设置交互类型
            interactions: [
              {
                type: "element-active",
              },
            ],
            state: {
              active: {
                // 这里可以设置 active 时的样式
                style: {
                  lineWidth: 1,
                },
              },
            },
            random: () => 0.5,
          };
          const config_density = { ...config };
          config_density.data = data_density;

          // return <h1>hello</h1>
          return (
            <div key={agg + "&" + "density" + "_" + field}>
              <h3>{agg + "_" + field}</h3>
              <WordCloud {...config} />
              <br />
              <h3>{"density" + "_" + field}</h3>
              <WordCloud {...config_density} />
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
            data,
            wordField: "type",
            weightField: "value",
            color: "#122c6a",
            // colorField: 'type',
            wordStyle: {
              fontFamily: "Verdana",
              // fontSize: [24, 50],
              rotation: 0,
            },
            // 设置交互类型
            interactions: [
              {
                type: "element-active",
              },
            ],
            state: {
              active: {
                // 这里可以设置 active 时的样式
                style: {
                  lineWidth: 1,
                },
              },
            },
            random: () => 0.5,
          };

          // return <h1>hello</h1>
          return (
            <div key={agg}>
              <h3>{agg + "_" + field}</h3>
              <WordCloud {...config} />
              <br />
            </div>
          );
        }
      })}
    </div>
  );
  return (
    <div>
      <N_number N={N} />
      {aggregation.map((agg) => {
        let data = [];
        displayData.forEach((element) => {
          let block = {
            type:
              groupBy.length === 1 ? element["key"] : element["key_as_string"],
            value: element[agg + "_" + field]["value"],
          };
          data.push(block);
        });

        console.log("format for pie and cloud", data);
        const config = {
          data,
          wordField: "type",
          weightField: "value",
          color: "#122c6a",
          // colorField: 'type',
          wordStyle: {
            fontFamily: "Verdana",
            // fontSize: [24, 50],
            rotation: 0,
          },
          // 设置交互类型
          interactions: [
            {
              type: "element-active",
            },
          ],
          state: {
            active: {
              // 这里可以设置 active 时的样式
              style: {
                lineWidth: 1,
              },
            },
          },
          random: () => 0.5,
        };

        // return <h1>hello</h1>
        return (
          <div key={agg}>
            <h3>{agg + "_" + field}</h3>
            <WordCloud {...config} />
            <br />
          </div>
        );
      })}
    </div>
  );
}
