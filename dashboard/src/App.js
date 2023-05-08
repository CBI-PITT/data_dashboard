


import './App.css';
import React, { useEffect, useState } from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';

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
function test() {
    return (<Box width={300}>
        <Slider
            size="small"
            defaultValue={70}
            aria-label="Small"
            valueLabelDisplay="auto"
        />
        <Slider defaultValue={50} aria-label="Default" valueLabelDisplay="auto" />
    </Box>)
}

function App() {
    const url = ""
    const [continuous, setContinuous] = useState()
    const [categorical, setCategorical] = useState()

    const [key_Category, setkey_Category] = useState()
    const [value_Category, setvalue_Category] = useState()
    const [key_Continuous, setkey_Continuous] = useState()
    const [value_Continuous, setvalue_Continuous] = useState()


    useEffect(() => {
        /* async () => {
          fetch(url).then(Response => {
            if (Response.ok) {
              return Response.json
            }
          }).then(Data => {
            setSample(Data)
          }
          ).catch(Error=>{
            throw(Error)
          })
        } */
        const mockData = {
            "categorical": { "Treatment": ["eeev", "veev", "weev"], "Time_point": [24, 48, 72, 96], "Route": ['subcutaneous'] },
            "continuous": { "Age": { "min": 0.5, "max": 5 }, "Metadata": { "min": 1, "max": 29 } }
        }
        var agent_cate_key = []
        var agent_cate_value = []
        var agent_conti_key = []
        var agent_conti_value = []
        for (var key in mockData.categorical) {
            agent_cate_key.push(key)
            agent_cate_value.push(mockData.categorical[key])
        }

        for (var key in mockData.continuous) {
            agent_conti_key.push(key)
            agent_conti_value.push(mockData.continuous[key])
        }

        setkey_Category(agent_cate_key)
        setvalue_Category(agent_cate_value)
        setkey_Continuous(agent_conti_key)
        setvalue_Continuous(agent_conti_value)
        console.log(agent_cate_key)
    }, [])


    /* setContinuous(mockData.continuous)
    setCategorical(mockData.categorical) */


    return (
        <div className="App">
            <header className="App-header">
                <h1>Klimstra</h1>
            </header>

            <div className='mainSec'>
                <div className='filter'>
                    <div className='continuous'>
                        {getConti(key_Continuous, value_Continuous)}
                    </div>
                    <div className='categorical'>
                        {getCate(key_Category, value_Category)}
                    </div>
                    <br></br>
                    <div>
                        <button>submit</button>
                    </div>
                </div>
                <div className='dispaly'>

                </div>
            </div>

            <div>
            </div>

        </div>
    );
}

export default App;


