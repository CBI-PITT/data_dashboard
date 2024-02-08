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
  acronym_volumn,
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
  const extractItems_density = (object, groupby, aggregation, fieldName) => {
    const extractedItems = {};

    aggregation.forEach((aggItem) => {
      const key = `${aggItem}_${fieldName}`;
      const value = object[key]?.value; // Extract the value from the subfield
      let acronym =
        groupBy.length === 1
          ? object["key"].toString()
          : object["key"][groupBy.indexOf(meta.atlas_structure_acronym)];
      extractedItems[key] = value / acronym_volumn[acronym];
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

  // console.log(newArray);
  const charts = aggregation.map((aggItem) => {
    // if (
    //   groupBy.includes(meta.atlas_structure_acronym) &&
    //   field === meta.atlas_structure_acronym &&
    //   aggItem === meta.aggregation_condition
    // ) {
    //   let newArray = displayData.map((object) =>
    //     extractItems(object, groupBy, aggregation, field)
    //   );
    //   let newArrayDensity = displayData.map((object) =>
    //     extractItems_density(object, groupBy, aggregation, field)
    //   );
    //   const config = {
    //     data: newArray,
    //     isGroup: true,
    //     xField: groupBy[0],
    //     yField: `${aggItem}_${field}`,
    //     seriesField: groupBy[1],
    //     legend: {
    //       position: "top-left",
    //       itemName: {
    //         style: {
    //           fontSize: 18,
    //         },
    //       },
    //     },
    //     axis: {},
    //     xAxis: {
    //       label: {
    //         autoHide: true,
    //         autoRotate: true,
    //         style: {
    //           fontSize: 18,
    //         },
    //       },
    //     },
    //     yAxis: {
    //       label: {
    //         autoHide: true,
    //         autoRotate: true,
    //         style: {
    //           fontSize: 18,
    //         },
    //       },
    //     },
    //     slider: {
    //       start: 0,
    //       end: 1,
    //     },
    //   };
    //   const density_config = {...config}
    //   density_config.data = newArrayDensity
    //   return (
    //     <>
    //     <div className="chartFill">
    //       <h3>{aggItem + "_" + field}</h3>
    //       <Column key={aggItem} {...config} />
    //       <br></br>
          
    //     </div>
    //     <div className="chartFill">
    //     <h3>{'density' + "_" + field}</h3>
    //       <Column key={'density'} {...density_config}/>
    //       <br></br>
    //     </div>
    //     </>
    //   );
    // } else {
      let newArray = displayData.map((object) =>
        extractItems(object, groupBy, aggregation, field)
      );
      console.log(newArray)
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
        <div >
          <h3>{aggItem + "_" + field}</h3>
          <Column key={aggItem} {...config} />
        </div>
      );
    // }
  });

  // Render all charts
  return <>{charts}</>;
}
