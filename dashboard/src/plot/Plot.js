import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,LineChart,
  Line, Brush,AreaChart, Area} from 'recharts';
import { PieChart, Pie } from 'recharts';
import React, { PureComponent } from 'react';
import COLORS from './colors';
import CoverImg from '../asset/CoverImg.png'

function Plot({displayData, x_axis, y_axis, plotChoice}) {
  // console.log("displayData", displayData)
  // console.log("displayData", x_axis)
  // console.log("displayData", y_axis)
  

  if (displayData === undefined) {
    // return <p>Loading....</p>
    return (
      <img src={CoverImg} className="coverImg"></img>
    )
    
  }
  if (plotChoice === "bar") {
    return (
      <ResponsiveContainer width="100%" aspect={2}>
        <BarChart

          data={displayData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={x_axis} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey={y_axis} fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    );
  }
  else if (plotChoice === "pie") {
    return (
      <ResponsiveContainer width="100%" aspect={2}>
        <PieChart width={400} height={400}>
          <Pie
            dataKey={y_axis}
            nameKey={x_axis}
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
          </Pie>



          <Tooltip />
          <Legend />
        </PieChart>

      </ResponsiveContainer>
    );
  }
  else if (plotChoice === "line")
  {
    return(
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
            <XAxis dataKey={x_axis} />
            <YAxis />
            <Tooltip />
            <Line type='monotone' dataKey={y_axis} stroke="#82ca9d" fill="#82ca9d" />
            <Brush />
            <Legend/>
          </LineChart>
        </ResponsiveContainer>
    )
  }
  else if(plotChoice === "area")
  {
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
          <XAxis dataKey={x_axis} />
          <YAxis />
          <Tooltip />
          <Area type="monotone" dataKey={y_axis} stroke="#8884d8" fill="#8884d8" />
          <Brush />
          <Legend/>
        </AreaChart>
      </ResponsiveContainer>
    );
  }

}

export default Plot;




