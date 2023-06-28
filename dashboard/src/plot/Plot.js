import {
  ScatterChart, Scatter, BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart,
  Line, Brush, AreaChart, Area
} from 'recharts';
import { Box } from '@ant-design/plots';
import { PieChart, Pie } from 'recharts';
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
  if (plotChoice === "bar") {
    console.log("check here", displayData)
    return (

      <ResponsiveContainer width="100%" aspect={2}>
        <BarChart
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
          <Legend />


          {
            aggregation.map((agg, ind) => {

              let val = agg + '_' + field + "['value']"
              return (
                <Bar dataKey={val} stackId='a' fill={COLORS[ind % COLORS.length]} />
              )
              // console.log(agg + "_" + field['value'],ind)
              // console.log('min_metadata'['value'])
            })
          }
          {/* <Bar dataKey="doc_count" fill="#8884d8" /> */}
          <Brush />
        </BarChart>
      </ResponsiveContainer>

    );
  }
  else if (plotChoice === "pie") {
    let inner = 100
    let outer = 120
    return (
      <ResponsiveContainer width="100%" aspect={2}>
        <PieChart width={400} height={400} className='pie_container'>
          {

            aggregation.map((agg, ind) => {

              let val = agg + '_' + field + "['value']"
              if (ind != 0) {
                inner = outer + 3
                outer = inner + 20
              }
              return (
                <Pie
                  dataKey={val}
                  // nameKey={groupBy.length == 1 ? 'key' : 'key_as_string'}
                  isAnimationActive={true}
                  data={displayData}
                  innerRadius={inner}
                  outerRadius={outer}
                  paddingAngle={5}

                // label
                >
                  {displayData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}

                </Pie>
              )


            })
          }
          {/* <Legend/> */}
          {/* <Pie
            dataKey={aggregation}
            nameKey={groupBy.length == 1 ? 'key' : 'key_as_string'}
            isAnimationActive={true}
            data={displayData}
            cx="50%"
            cy="50%"
            outerRadius={200}
            innerRadius={100}
            paddingAngle={10}
            fill='#0088FE'
            label>
            {displayData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie> */}
          <Tooltip />

        </PieChart>

      </ResponsiveContainer>
    );
  }
  else if (plotChoice === "line") {
    return (
      <ResponsiveContainer width="100%" aspect={2}>
        <LineChart
          width={500}
          height={200}
          data={displayData}
          syncId="anyId"
          margin={{
            top: 10,
            right: 30,
            left: 0,
            bottom: 0,
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
    console.log("area")
    return (
      <ResponsiveContainer width="100%" aspect={2}>
        <AreaChart
          width={500}
          height={400}
          data={displayData}
          margin={{
            top: 10,
            right: 30,
            left: 0,
            bottom: 0,
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
    
    
    let val = "boxplot" + '_' +field
    console.log()
    const config = {
      width: 400,
      height: 500,
      data: displayData,
      xField: groupBy.length == 1 ? 'key' : 'key_as_string',
      yField: ['val.min', 'val.q1', 'val.q2', 'val.q3', 'val.max'],
      boxStyle: {
        stroke: '#545454',
        fill: '#333333',
        fillOpacity: 0.3,
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
    if (aggregation.length > 2) {
      return (
        <div>
          <h1>GroupBy parameters selected should be equal to 2 for scatter plot</h1>
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




