import React from "react";
import Typography from "@mui/material/Typography";
import Plot from "react-plotly.js";

function PieCharts({ groupedData }) {
  const generatePieCharts = (data, prefix = "") => {
    const pieCharts = [];

    Object.keys(data).forEach((key) => {
      const currentKey = prefix ? `${prefix} ${key}` : key;

      if (typeof data[key] === "object" && !Array.isArray(data[key])) {
        pieCharts.push(...generatePieCharts(data[key], currentKey));
      } else {
        const valueCount = data[key]?.value_count || 0;
        const avgValueCount = data[key]?.avg_value_count || 0;

        pieCharts.push({
          labels: ["value_count", "avg_value_count"],
          values: [valueCount, avgValueCount],
          type: "pie",
          name: currentKey,
          hoverinfo: "label+value+name",
        });
      }
    });

    return pieCharts;
  };

  const pieChartsData = generatePieCharts(groupedData);

  return (
    <div>
      {pieChartsData.map((data, index) => (
        <div key={index}>
          <Plot data={[data]} />
        </div>
      ))}
    </div>
  );
}

export default function FacetChart({
  displayData,
  aggregation,
  field,
  dimension,
  groupByKeys,
}) {
  // console.log(Object.keys(check))
  // sorting problem when field on numerical value
  // last layer should be array type instead of {}

  // method 1 for facet data construction 
  // const groupedData = displayData.reduce((acc, obj) => {
  //   const groupByKeysContent = groupByKeys.map((key) => obj.key[key]);

  //   const dimensionContent = obj.key[dimension];

  //   const values = {};
  //   aggregation.forEach((agg) => {
  //     values[agg] = obj[agg + "_" + field]?.value || 0;
  //   });
  //   let currentLevel = acc;
  //   groupByKeysContent.forEach((key) => {
  //     if (!currentLevel[key]) {
  //       currentLevel[key] = {};
  //     }
  //     currentLevel = currentLevel[key];
  //   });
  //   // console.log(currentLevel)
  //   aggregation.forEach((agg) => {
  //     if (!currentLevel[agg]) {
  //       currentLevel[agg] = [];
  //       // console.log(label_content)
  //       currentLevel[agg].push({
  //         [dimensionContent]:values[agg]
  //       })

  //     } else {
  //       currentLevel[agg].push({
  //         [dimensionContent]:values[agg]
  //       })
  //     }
  //   });
  //   return acc;
  // }, {});

  // method 2 for facet data construction 
  const groupedData = displayData.reduce((acc, obj) => {
    const groupByKeysContent = groupByKeys.map((key) => obj.key[key]);

    const dimensionContent = obj.key[dimension];

    const values = {};
    aggregation.forEach((agg) => {
      values[agg] = obj[agg + "_" + field]?.value || 0;
    });
    let currentLevel = acc;
    groupByKeysContent.forEach((key) => {
      if (!currentLevel[key]) {
        currentLevel[key] = {};
      }
      currentLevel = currentLevel[key];
    });
    // console.log(currentLevel)
    aggregation.forEach((agg) => {
      if (!currentLevel[agg]) {
        currentLevel[agg] = {
          'labels_list': [],
          'values_list': [],
        };
        // console.log(label_content)
        currentLevel[agg].labels_list.push(dimensionContent)
        currentLevel[agg].values_list.push(values[agg])
        
      } else {
        currentLevel[agg].labels_list.push(dimensionContent)
        currentLevel[agg].values_list.push(values[agg])
      }
    });
    return acc;
  }, {});

  // console.log(groupedData);

  let agg_list_render = {};
  let agg_list_set = [];
  aggregation.forEach((agg) => {
    agg_list_render[agg] = [];
    agg_list_set.push(agg);
  });

  function loopThroughObject(obj, keyInfo = "") {
    for (const key in obj) {
      if (typeof obj[key] === "object" && obj[key] !== null) {
        const newKeyInfo = keyInfo ? `${keyInfo}-${key}` : key;
        // If the value is an object (including arrays), recursively call the function
        if (agg_list_set.includes(key)) {
          
          // console.log(obj[key]);
          // console.log(obj[key].map(obj => Object.keys(obj)[0]));
          // console.log(Object.values(obj[key]))
          
          let chartData = {
            // access data for method 1
            // labels: obj[key].map((obj) => Object.keys(obj)[0]),
            // values: obj[key].map((obj) => Object.values(obj)[0]),

            // access data for method 2
            labels:obj[key].labels_list,
            values: obj[key].values_list,
            type: "pie",
            textinfo: "none",
            sort: false,
          };
          agg_list_render[key].push(
            <Plot key={keyInfo}
              data={[chartData]}
              layout={{
                width: 400,
                height: 400,
                title: `${key}  (${keyInfo})`,
                sort: false,
              }}
            />
          );
        }
        loopThroughObject(obj[key], newKeyInfo);
      } else {
        return;
      }
    }
  }
  loopThroughObject(groupedData);
  return (
    <div>
      {aggregation.map((agg) => (
        <div key={agg}>
          <Typography variant="h5">
            {agg}_ {field}
          </Typography>
          {agg_list_render[agg]}
        </div>
      ))}
    </div>
  );
}
// console.log(groupedData)
// return <PieCharts groupedData={groupedData} />;

// const pieCharts = [];

// Object.entries(groupedData).forEach(([groupKey, subGroups]) => {
//   const subGroupCharts = [];

//   Object.entries(subGroups).forEach(([subGroupKey, data]) => {
//     const lable_content = Object.keys(data); // Get all unique acronyms as labels
//     console.log(lable_content)

//     const valuesData = lable_content.map(label => data[label].value_count); // Extract value for each label
//     const chartData = aggregation.map(agg => ({
//       values: valuesData,
//       labels: lable_content,
//       type: 'pie',
//       textinfo: 'none',
//       name: agg,
//     }));
//     console.log(chartData)
//     subGroupCharts.push(
//       <div key={`${groupKey}-${subGroupKey}`} style={{ display: 'inline-block', margin: '10px' }}>
//         <h4>{groupBy.join(': ')} - {groupKey} - {subGroupKey}</h4>
//         <div style={{ display: 'flex' }}>
//           {chartData.map((data, index) => (
//             <div key={index} style={{ marginRight: '20px' }}>
//               <h5>{lable_content[index]} Distribution</h5>
//               <Plot
//                 data={[data]}
//                 layout={{ width: 400, height: 400, title: `${lable_content[index]} Pie Chart for ${subGroupKey}` }}
//               />
//             </div>
//           ))}
//         </div>
//       </div>
//     );
//   });

//   pieCharts.push(
//     <div key={groupKey}>
//       <h3>{groupBy.join(': ')} - {groupKey}</h3>
//       {subGroupCharts}
//     </div>
//   );
// });

// return <div>{pieCharts}</div>;
