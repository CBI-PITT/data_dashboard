/* import React, {useState, useEffect} from 'react'

function App() {
    const [data, setData] = useState([{}])
    useEffect(() => {
        fetch("/api/data").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
                console.log("checkcheck")
            }
        )
    }, [])
    return (
        <div>
            {(typeof data.cells === "undefined") ? (
                <p>Loading...</p>
            ): (
                data.cells.map((cells, i) => (
                    <p key={i}>{cells}</p>
                ))
            )}
        </div>
    )
}

export default App */


import './App.css';
import React, { useEffect, useState } from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

function getCate(props) {

    if (props !== undefined) {
        return (

            <div>
                <h3>Treatment</h3>
                <div>
                    {props.treatment.map((prop) => (


                        <label>
                            <input type="checkbox" />
                            {console.log("check" + prop)}
                            {prop}

                        </label>

                    ))}
                </div>
                <h3>Time_point</h3>
                <div>
                    {props.time_point.map((prop) => (

                        <label>
                            <input type="checkbox" />
                            {console.log("check" + prop)}
                            {prop}

                        </label>
                    ))}
                </div>


            </div>
        )
    }
}
function getConti(props) {

    if (props !== undefined) {

        return (
            <div>
                <h3>Age</h3>
                <div>
                    Min:
                    {console.log(props.age.min)}
                    {props.age.min}
                    Max:
                    {console.log(props.age.min)}
                    {props.age.max}
                </div>
            </div>
        )
    }
}

function App() {
    const url = ""
    const [continuous, setContinuous] = useState()
    const [categorical, setCategorical] = useState()
    const [sample, setSample] = useState()


    const mockData = {
        "categorical": { "treatment": ["eeev", "veev"], "time_point": [24, 48, 72, 96] },
        "continuous": { "age": { "min": 0.5, "max": 5 } }
    }
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
        setContinuous(mockData.continuous)
        setCategorical(mockData.categorical)
        console.log(continuous)

    }, [])


    /* setContinuous(mockData.continuous)
    setCategorical(mockData.categorical) */


    return (
        <div className="App">
            <header className="App-header">
                <h1>Klimstra</h1>
            </header>
            {
                console.log("we are here!")
            }
            <div className='mainSec'>
                <div className='filter'>
                    <div className='continuous'>
                        {getConti(continuous)}

                    </div>
                    <div className='categorical'>
                        {getCate(categorical)}
                    </div>

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


