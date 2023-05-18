import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import { useState } from 'react';
import * as React from 'react';
function getConti(key, value) {
    // const key = ["Treatment", "Time_Point"]
    // const value = [["eeve", "weev", "vvev"], [24, 48, 72, 96]]
    // const [valueSlider,setValueSlider] = useState([])

    // const onChangeValue = (event,newValue) =>{
    //     setValueSlider(newValue)
    // }
    if (key !== undefined && value !== undefined) {
        return (
            // <div>
            //     {
            //         key.map((k, ind) => (
            //             <div>
            //                 <h2>{k}</h2>
            //                 {/* {value[ind].map((v) => (
            //                     <label>
            //                         <input type="checkbox" />
            //                         {v}
            //                     </label>
            //                 ))} */}
            //                 <span>Min: {value[ind].min}</span>
            //                 <span>Max: {value[ind].max}</span>
            //             </div>
            //         ))
            //     }
            // </div>
            <div>
                <center>

                    {key.map((k, ind) => (
                        <div>
                            <h2>{k}</h2>
                            <div>
                                {value[ind].min}
                                <Box className='slider'>

                                    {/* <input className='slider' type="range" id={k} min={value[ind].min} max={value[ind].max} name={k} /> */}
                                    <Slider id={k} min={value[ind].min} max={value[ind].max} name={k} defaultValue={[value[ind].min, value[ind].max]} 
                                        valueLabelDisplay="auto"></Slider>

                                </Box>
                                {value[ind].max}
                            </div>

                        </div>
                    ))}


                </center>
            </div>
        )
    }
}

export default getConti;