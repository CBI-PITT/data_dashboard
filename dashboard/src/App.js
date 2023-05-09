import './App.css';
import React, { useEffect, useState } from 'react';
import axios from "axios";
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';

function get_X_axis(list) {
    console.log(list)
    if (list !== undefined) {
        return (
            <div>
                {
                    list.map((item) => (
                        <span>
                            {item} / 
                        </span>
                    ))
                }
            </div>
        )
    }
}

function get_Y_axis(list) {
    console.log(list)
    if (list !== undefined) {
        return (
            <div>
                {
                    list.map((item) => (
                        <span>
                            {item} / 
                        </span>
                    ))
                }
            </div>
        )
    }
}

function getCate(key, value) {
    // const key = ["Treatment", "Time_Point"]
    // const value = [["eeve", "weev", "vvev"], [24, 48, 72, 96]]
    if (key !== undefined && value !== undefined) {
        return (
            <div>
                {
                    key.map((k, ind) => (
                        <div>
                            <h2>{k}</h2>
                            {value[ind].map((v) => (
                                <label>
                                    <input type="checkbox" />
                                    {v}
                                </label>
                            ))}
                        </div>
                    ))
                }
            </div>
        )
    }
}

function getConti(key, value) {
    // const key = ["Treatment", "Time_Point"]
    // const value = [["eeve", "weev", "vvev"], [24, 48, 72, 96]]
    if (key !== undefined && value !== undefined) {
        return (
            <div>
                {
                    key.map((k, ind) => (
                        <div>
                            <h2>{k}</h2>
                            {/* {value[ind].map((v) => (
                                <label>
                                    <input type="checkbox" />
                                    {v}
                                </label>
                            ))} */}
                            <span>Min: {value[ind].min}</span>
                            <span>Max: {value[ind].max}</span>
                        </div>
                    ))
                }
            </div>
        )
    }
}

function get_GroupBy(list) {
    console.log(list)
    if (list !== undefined) {
        return (
            <div>
                {
                    list.map((item) => (
                        <span>
                            {item} / 
                        </span>
                    ))
                }
            </div>
        )
    }
}

function get_Agrregation(list) {
    console.log(list)
    if (list !== undefined) {
        return (
            <div>
                {
                    list.map((item) => (
                        <span>
                            {item} / 
                        </span>
                    ))
                }
            </div>
        )
    }
}

// function getCate(props) {
//     if (props !== undefined) {
//         return (
//             <div>
//                 <h3>Treatment</h3>
//                 <div>
//                     {props.treatment.map((prop) => (
//                         <label>
//                             <input type="checkbox" />
//                             {prop}
//                         </label>
//                     ))}
//                 </div>
//                 <h3>Time_point</h3>
//                 <div>
//                     {props.time_point.map((prop) => (

//                         <label>
//                             <input type="checkbox" />

//                             {prop}

//                         </label>
//                     ))}
//                 </div>
//             </div>
//         )
//     }
// }
// function getConti(props) {
//     if (props !== undefined) {
//         return (
//             <div>
//                 <h3>Age</h3>
//                 <div>
//                     Min:

//                     {props.age.min}
//                     Max:

//                     {props.age.max}
//                 </div>
//             </div>
//         )
//     }
// }


function App() {
    const urlPrefix = "http://127.0.0.1:5000"
    const url_xyAxis = "/api/get-xy"
    const url_filter = "/api/filters"
    const url_groupBy = "/api/get-group-by"
    const url_aggregation = "/api/get-aggregate"
    const url_query = "/api/query"

    //Initialize columns section
    const [X_axis_list, setX_axis_list] = useState()
    const [Y_axis_list, setY_axis_list] = useState()

    //Initialize filter section
    const [key_Category, setkey_Category] = useState()
    const [value_Category, setvalue_Category] = useState()
    const [key_Continuous, setkey_Continuous] = useState()
    const [value_Continuous, setvalue_Continuous] = useState()

    //Initialize GroupBy section
    const [GroupBy_list, setGroupBy_List] = useState()

    //Initialize Agrregation section
    const [Agrregation_list, setAgrregation_list] = useState()

    useEffect(() => {

        // Request for xy axis list
        axios.get(urlPrefix + url_xyAxis).then((response) => {
            let xyAxis_list_return = response.data.data
            // console.log(xyAxis_list_return)
            setX_axis_list(xyAxis_list_return)
            setY_axis_list(xyAxis_list_return)
            // console.log(X_axis_list)
        })

        // Request for filter(key,value)
        axios.get(urlPrefix + url_filter).then((response) => {

             console.log("filter return", typeof(response.data))

            let filter_return = JSON.parse(response.data.replace(/\bNaN\b/g, "null"));
            // console.log(filter_return)
            let agent_cate_key = []
            let agent_cate_value = []
            let agent_conti_key = []
            let agent_conti_value = []

            for (let key in filter_return.categorical) {

                agent_cate_key.push(key)
                agent_cate_value.push(filter_return.categorical[key])
            }

            for (let key in filter_return.continuous) {
                agent_conti_key.push(key)
                agent_conti_value.push(filter_return.continuous[key])
            }

            // Filter setting
            setkey_Category(agent_cate_key)
            setvalue_Category(agent_cate_value)
            setkey_Continuous(agent_conti_key)
            setvalue_Continuous(agent_conti_value)
        });

        // Request for groupBy list
        axios.get(urlPrefix + url_groupBy).then((response) => {
             console.log("groupBy return", typeof(response.data.data))
            let groupBy_list_return = response.data.data
            setGroupBy_List(groupBy_list_return)
            //  console.log(GroupBy_list)
        })

        // Request for aggregation list
        axios.get(urlPrefix + url_aggregation).then((response) => {
            // console.log(response.data.data)
            let aggregation_list_return = response.data.data
            setAgrregation_list(aggregation_list_return)
            //  console.log(Agrregation_list)
        })


        // console.log("X_axis_list" + X_axis_list)
        // console.log("Y_axis_list" + Y_axis_list)
        // console.log("key_Category" + key_Category)
        // console.log("key_Continuous" + key_Continuous)
        // console.log("GroupBy_list: " + GroupBy_list)
        // console.log("Agrregation_list" + Agrregation_list)


        // const mockData = {
        //     "X_axis_list": ["cellId"],
        //     "Y_axis_list": ["Time_Point"],
        //     "categorical": { "Treatment": ["eeev", "veev", "weev"], "Time_point": [24, 48, 72, 96], "Route": ['subcutaneous'] },
        //     "continuous": { "Age": { "min": 0.5, "max": 5 }, "Metadata": { "min": 1, "max": 29 } },
        //     "GroupBy_list": ["Treatment"],
        //     "Aggregation_list": ["value"]
        // }
        // var agent_cate_key = []
        // var agent_cate_value = []
        // var agent_conti_key = []
        // var agent_conti_value = []
        // for (var key in mockData.categorical) {
        //     agent_cate_key.push(key)
        //     agent_cate_value.push(mockData.categorical[key])
        // }

        // for (var key in mockData.continuous) {
        //     agent_conti_key.push(key)
        //     agent_conti_value.push(mockData.continuous[key])
        // }
        // Columns (X_axis_list, Y_axis_list) setting
        // setX_axis_list(mockData.X_axis_list)
        // setY_axis_list(mockData.Y_axis_list)
        // console.log("X_axis_list is :" + X_axis_list)

        // Filter setting
        // setkey_Category(agent_cate_key)
        // setvalue_Category(agent_cate_value)
        // setkey_Continuous(agent_conti_key)
        // setvalue_Continuous(agent_conti_value)
        // console.log(agent_cate_key)

        //GroupBy list setting
        // setGroupBY_List(mockData.GroupBy_list)

        // //Aggregation list setting
        // setAgrregation_list(mockData.Aggregation_list)
    }, [])





    return (
        <div className="App">
            <header className="App-header">
                <h1>Klimstra</h1>
            </header>
            <div className='main_sec'>
                <div className='selection_container'>
                    <div className='columns'>
                        {get_X_axis(X_axis_list)}
                        {get_Y_axis(Y_axis_list)}
                    </div>
                    <div className='filter'>
                        <div className='continuous'>
                            {getConti(key_Continuous, value_Continuous)}
                        </div>
                        <div className='categorical'>
                            {getCate(key_Category, value_Category)}
                        </div>
                    </div>
                    <div className='groupBy'>
                        {get_GroupBy(GroupBy_list)}
                    </div>
                    <div className='aggregation'>
                        {get_Agrregation(Agrregation_list)}
                    </div>
                    <br></br>
                    <div>
                        <button>submit</button>
                    </div>
                </div>
                <div className='display_container'>

                </div>
            </div>

            <div>
            </div>

        </div>
    );
}

export default App;


