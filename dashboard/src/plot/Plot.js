import {
  ScatterChart, Scatter, BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart,
  // Line, 
  Brush, AreaChart, 
  // Area
} from 'recharts';
import { Area,Box, Pie, Column,Line } from '@ant-design/plots';
import { PieChart } from 'recharts';
import React, { PureComponent } from 'react';
import COLORS from './colors';
import CoverImg from '../asset/CoverImg.png'

function Plot({ displayData, field, groupBy, aggregation, plotChoice }) {
  var groupByList = ''
  groupBy.forEach(val => {
    groupByList = groupByList + val + '_'
  });
  // for(let ind in groupBy)
  // {
  //     groupByList = groupByList + groupBy[ind] + '_'
  // }
  // console.log("displayData", displayData)
  // console.log("displayData", groupByList)
  // console.log("displayData", aggregation)


  if (displayData === undefined) {
    // return <p>Loading....</p>
    return (
      <div>
        <br></br>
        <img src={CoverImg} className="coverImg"></img>
        <h3 id='coverText'>Statistics and Visulization for Klimstra Project</h3>
      </div>
    )
  }
  // if (plotChoice === "bar") {
  //   console.log("check here",displayData)
  //   return (
  //     <ResponsiveContainer width="100%" aspect={2}>
  //       <BarChart

  //         data={displayData}
  //         margin={{
  //           top: 5,
  //           right: 30,
  //           left: 20,
  //           bottom: 5,
  //         }}
  //       >
  //         <CartesianGrid strokeDasharray="3 3" />
  //         <XAxis dataKey={groupByList} />
  //         <YAxis />
  //         <Tooltip />
  //         <Legend />
  //         <Bar dataKey={aggregation} fill="#8884d8" />
  //       </BarChart>
  //     </ResponsiveContainer>
  //   );
  // }
  let data = []
  displayData.forEach(element => {
    
    aggregation.forEach(agg => {
      let block = {
        X_axis: groupBy.length == 1 ? element['key'] : element['key_as_string']
      }
      block['type'] = agg + '_' + field
      block['value'] = element[agg + '_' + field]['value']
      data.push(block)
    });
    
  });

  if (plotChoice === "bar") {
    console.log("check here", displayData)
    
    console.log("bar",data)
    const config = {
      data,
      isStack: true,
      xField: 'X_axis',
      yField: 'value',
      seriesField: 'type',
      slider: {
        start: 0,
        end: 1,
      },
      label: {
        // 可手动配置 label 数据标签位置
        position: 'middle',
        // 'top', 'bottom', 'middle'
        // 可配置附加的布局方法
        layout: [
          // 柱形图数据标签位置自动调整
          {
            type: 'interval-adjust-position',
          }, // 数据标签防遮挡
          {
            type: 'interval-hide-overlap',
          }, // 数据标签文颜色自动调整
          {
            type: 'adjust-color',
          },
        ],
      },
      interactions: [
        {
          type: 'active-region',
          enable: false,
        },
      ],
      connectedArea: {
        style: (oldStyle, element) => {
          return {
            fill: 'rgba(0,0,0,0.25)',
            stroke: oldStyle.fill,
            lineWidth: 0.5,
          };
        },
      },
    };
    return  <ResponsiveContainer width="100%" aspect={2}><Column {...config} /></ResponsiveContainer>;
    // return (

    //   <ResponsiveContainer width="100%" aspect={2}>
    //     <BarChart
    //       width={500}
    //       height={300}
    //       data={displayData}
    //       margin={{
    //         top: 20,
    //         right: 30,
    //         left: 20,
    //         bottom: 5,
    //       }}
    //     >
    //       <CartesianGrid strokeDasharray="3 3" />
    //       <XAxis dataKey={groupBy.length == 1 ? 'key' : 'key_as_string'} />
    //       <YAxis />
    //       <Tooltip />
    //       <Legend />


    //       {
    //         aggregation.map((agg, ind) => {

    //           let val = agg + '_' + field + "['value']"
    //           return (
    //             <Bar dataKey={val} stackId='a' fill={COLORS[ind % COLORS.length]} />
    //           )
    //           // console.log(agg + "_" + field['value'],ind)
    //           // console.log('min_metadata'['value'])
    //         })
    //       }
    //       {/* <Bar dataKey="doc_count" fill="#8884d8" /> */}
    //       <Brush />
    //     </BarChart>
    //   </ResponsiveContainer>

    // );
  }
  else if (plotChoice === "pie") {
    // let data = [

    //   { type: '10|96|eeev', value: 4440312 }
    //   ,
    //   { type: '22|96|weev', value: 424018 }
    //   ,
    //   { type: '26|72|weev', value: 422979 }
    //   ,
    //   { type: '11|96|weev', value: 414549 }
    //   ,
    //   { type: '2|96|eeev', value: 333575 }
    //   ,
    //   { type: '18|96|weev', value: 277428 }
    //   ,
    //   { type: '14|72|weev', value: 98642 }

    // ];
    // console.log("test data", data)
    // const config = {
    //   appendPadding: 10,
    //   data,
    //   angleField: 'value',
    //   colorField: 'type',
    //   radius: 0.75,
    //   label: {
    //     type: 'spider',
    //     labelHeight: 28,
    //     content: '{name}\n{percentage}',
    //   },
    //   interactions: [
    //     {
    //       type: 'element-selected',
    //     },
    //     {
    //       type: 'element-active',
    //     },
    //   ],
    // };
    // return <Pie {...config} />;
    return (
      aggregation.map(agg => {
        let data = []
        displayData.forEach(element => {
          let block = {
            type: groupBy.length == 1 ? element['key'] : element['key_as_string'],
            value: element[agg + "_" + field]['value']
          }
          data.push(block)
        })
        console.log("data", data)

        const config = {
          appendPadding: 10,
          data,
          // theme:'dark',
          angleField: 'value',
          colorField: 'type',
          radius: 0.9,
          label: {
            type: 'spider',
            labelHeight: 28,
            content: '{name}\n{percentage}',
          },
          interactions: [
            {
              type: 'element-selected',
            },
            {
              type: 'element-active',
            },
          ],
        }

        // return <h1>hello</h1>
        return <div><Pie {...config} /><br /></div>;
      }

      )
    )

    // let inner = 100
    // let outer = 120
    // return (
    //   <ResponsiveContainer width="100%" aspect={2}>
    //      <PieChart width={400} height={400} className='pie_container'>
    //       {

    //         aggregation.map((agg, ind) => {

    //           let val = agg + '_' + field + "['value']"
    //           if (ind != 0) {
    //             inner = outer + 3
    //             outer = inner + 20
    //           }
    //           return (
    //             <Pie
    //               dataKey={val}
    //               // nameKey={groupBy.length == 1 ? 'key' : 'key_as_string'}
    //               isAnimationActive={true}
    //               data={displayData}
    //               innerRadius={inner}
    //               outerRadius={outer}
    //               paddingAngle={5}

    //             // label
    //             >
    //               {displayData.map((entry, index) => (
    //                 <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
    //               ))}

    //             </Pie>
    //           )


    //         })
    //       }
    //       <Legend/>
    //       <Tooltip />
    //     </PieChart> 


    //   </ResponsiveContainer>
    // );
  }
  else if (plotChoice === "line") {
    const config = {
      data,
      xField: 'X_axis',
      yField: 'value',
      seriesField: 'type',
      smooth: true,
      point: {
        size: 5,
        style: {
          lineWidth: 1,
          fillOpacity: 1,
        },
        shape: 'circle'
        
      },
      slider: {
        start: 0,
        end: 1,
      },
      
    };
  
    return <ResponsiveContainer width="100%" aspect={2}><Line {...config} /></ResponsiveContainer>;



    return (
      <ResponsiveContainer width="100%" aspect={2}>
        <LineChart
          width={500}
          height={300}
          data={displayData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={groupBy.length == 1 ? 'key' : 'key_as_string'} />
          <YAxis />
          <Tooltip />
          {
            aggregation.map((agg, ind) => {

              let val = agg + '_' + field + "['value']"
              return (
                <Line type="monotone" dataKey={val} strokeWidth={2} stroke={COLORS[ind % COLORS.length]} />
              )
              // console.log(agg + "_" + field['value'],ind)
              // console.log('min_metadata'['value'])
            })
          }
          <Brush />
          <Legend />
        </LineChart>
      </ResponsiveContainer>
    )
  }
  else if (plotChoice === "area") {


    const config = {
      data,
      xField: 'X_axis',
      yField: 'value',
      seriesField: 'type',
      slider: {
        start: 0,
        end: 1,
      },
      smooth: true
    };
    return <ResponsiveContainer width="100%" aspect={2}><Area {...config} /></ResponsiveContainer>;

    console.log("area")
    return (
      <ResponsiveContainer width="100%" aspect={2}>
        <AreaChart
          width={500}
          height={300}
          data={displayData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={groupBy.length == 1 ? 'key' : 'key_as_string'} />
          <YAxis />
          <Tooltip />
          {/* <Area type="monotone" dataKey={aggregation} stroke="#8884d8" fill="#8884d8" /> */}
          {
            aggregation.map((agg, ind) => {

              let val = agg + '_' + field + "['value']"
              return (
                <Area type="monotone" dataKey={val} stackId='a' stroke={COLORS[ind % COLORS.length]} fill={COLORS[ind % COLORS.length]} />
              )
              // console.log(agg + "_" + field['value'],ind)
              // console.log('min_metadata'['value'])
            })
          }
          <Brush />
          <Legend />
        </AreaChart>
      </ResponsiveContainer>
    );
  }

  else if (plotChoice === "box") {
    // const urlPrefix = "http://127.0.0.1:5000"

    // const url_query = "/api/query2"
    // let formData_copy = formData
    // formData.aggregate.push('boxplot')
    // let formData_send = JSON.stringify(formData_copy)
    // console.log(formData_copy)
    // console.log(formData_send)
    // // console.log("formdata_send", typeof (formData_send))

    // fetch(urlPrefix + url_query, {
    //   headers: { 'Content-Type': 'application/json' },
    //   method: 'POST',
    //   body: formData_send
    // }).then(
    //   res => res.json()
    // ).then(
    //   data => {
    //     console.log(typeof (data), data)

    //     setDisplayData(data)
    //     // console.log("setDisplayData", displayData)
    //   }
    // )
    // if(!aggregation.includes('boxplot'))
    // {
    //   return <h1>Please select boxplot choice in aggregation section</h1>
    // }
    let boxplot_data_list = []
    let boxplot_name = 'boxplot' + '_' + field
    // console.log("boxplot_name",element[boxplot_name])
    displayData.forEach(element => {
      let temp = {
        'x': groupBy.length == 1 ? element['key'] : element['key_as_string'],
        'min': element[boxplot_name]['min'],
        'q1': element[boxplot_name]['q1'],
        'median': element[boxplot_name]['q2'],
        'q3': element[boxplot_name]['q3'],
        'max': element[boxplot_name]['max']
      }
      boxplot_data_list.push(temp)
    });
    console.log("boxplot_data_list", boxplot_data_list)

    let boxplot_data_block = "boxplot" + '_' + field
    // let q1 = "boxplot" + '_' +field + "['q1']"
    // let median = "boxplot" + '_' +field + "['q2']"
    // let q3 = "boxplot" + '_' +field + "['q3']"
    console.log()
    const config = {
      width: 400,
      height: 500,
      data: boxplot_data_list,
      xField: 'x',
      yField: ['min', "q1", 'median', 'q3', 'max'],
      boxStyle: {
        stroke: '#545454',
        fill: '#292929',
        fillOpacity: 0.6,
      },
      animation: true,
    };
    return (
      <ResponsiveContainer width="100%" aspect={2}>
        <Box{...config} />

      </ResponsiveContainer>

    )
  }

  else if (plotChoice === "scatter") {
    if (aggregation.length !== 2) {
      return (
        <div>
          <h1>Aggregation parameters selected should be equal to 2 for scatter plot</h1>
        </div>
      )
    }
    var X = aggregation[0] + '_' + field + "['value']"
    var Y = aggregation[1] + '_' + field + "['value']"
    return (
      <ResponsiveContainer width="100%" aspect={2}>
        <ScatterChart
          margin={{
            top: 20,
            right: 20,
            bottom: 20,
            left: 20,
          }}
        >
          <CartesianGrid />

          <XAxis type="number" dataKey={X} name={X} />
          <YAxis type="number" dataKey={Y} name={Y} />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter name="A school" data={displayData} fill="#8884d8" />
        </ScatterChart>
      </ResponsiveContainer>
    )
  }

}

export default Plot;




