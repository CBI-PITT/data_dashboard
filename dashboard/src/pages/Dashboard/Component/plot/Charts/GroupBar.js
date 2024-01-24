import { Column } from "@ant-design/plots";
import React, { useState } from "react";
import N_number from "../Control/N_number";
import { Button } from "@mui/material";
export default function GroupBarChart({
  displayData,
  data_BLA,
  data_acronym_density_BLA,
  groupBy,
  field,
  aggregation,
  meta,
  N,
}) {
  const extractItems = (object, groupby, aggregation, fieldName) => {
    const extractedItems = {};

    aggregation.forEach((aggItem) => {
      const key = `${aggItem}_${fieldName}`;
      const value = object[key]?.value; // Extract the value from the subfield
      extractedItems[key] = value;
    });

    groupby.forEach((key) => {
      extractedItems[key] = object.key[groupby.indexOf(key)];
    });

    return {
      ...object, // Keep all other fields in the original object
      ...extractedItems,
    };
  };

  // Create a new array with the extracted items for each object
  const newArray = displayData.map((object) =>
    extractItems(object, groupBy, aggregation, field)
  );
//   console.log(newArray);
  const charts = aggregation.map((aggItem) => {
    const config = {
      data: newArray,
      isGroup: true,
      xField: groupBy[0],
      yField: `${aggItem}_${field}`,
      seriesField: groupBy[1],
      legend: {
        position: "top-left",
        itemName: {
          style: {
            fontSize: 18,
          },
        },
      },
      axis: {},
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
      slider: {
        start: 0,
        end: 1,
      },
    };

    return (
      <div className="chartFill">
        <h3>{aggItem + "_" + field}</h3>
        <Column key={aggItem} {...config} />
      </div>
    );
  });

  // Render all charts
  return <>{charts}</>;
  //   function handleClick(){
  //     setXYChange[xychange[1],xychange[0]]
  //   }

  //   if (
  //     groupBy.includes(meta.atlas_structure_acronym) &&
  //     field === meta.atlas_structure_acronym &&
  //     aggregation.includes(meta.aggregation_condition)
  //   ) {
  //     let config_density = { ...config };
  //     config_density.data = data_acronym_density_BLA;
  //     config_density.smooth = false;
  //     return (
  //       <div className="chartFill">
  //         {/* <Button onClick={handleClick}>Reverse</Button> */}
  //         <N_number N={N} />
  //         <Column {...config} />
  //         <br></br>
  //         <Column {...config_density} />
  //       </div>
  //     );
  //   } else {
  //     return (
  //       <div className="chartFill">
  //         <N_number N={N} />
  //         <Column {...config} />
  //       </div>
  //     );
  //   }
  // return <Column {...config}/>
}
