import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import React, { PureComponent } from 'react';
function bar (displayData,x_axis,y_axis) {
    console.log("displayData",displayData)
    console.log("displayData",x_axis)
    console.log("displayData",y_axis)

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

export default bar;




