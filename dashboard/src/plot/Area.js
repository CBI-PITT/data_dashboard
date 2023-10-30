import { Area} from '@ant-design/plots';
import React from 'react';

export default function AreaChart ({ data_BLA, data_acronym_density_BLA, groupBy, field, aggregation, density_dict }){
    const config = {
        data: data_BLA,
        xField: "X_axis",
        yField: "value",
        seriesField: "type",
        slider: {
          start: 0,
          end: 1,
        },
        xAxis: {
          label: {
            autoHide: true,
            autoRotate: true,
          },
        },
        smooth: true,
      };
  
      if (
        groupBy.includes(density_dict.atlas_structure_acronym) &&
        field === density_dict.atlas_structure_acronym &&
        aggregation.includes(density_dict.aggregation_choice)
      ) {
        let config_density = { ...config };
        config_density.data = data_acronym_density_BLA;
        return (
          <div className="chartFill">
            {" "}
            <Area {...config} />
            <Area {...config_density} />
          </div>
        );
      } else {
        return (
          <div className="chartFill">
            {" "}
            <Area {...config} />
          </div>
        );
      }
}