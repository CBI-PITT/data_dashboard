import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import { useState } from 'react';
import Typography from '@mui/material/Typography';
import * as React from 'react';



function setting(min, max) {
    return [{ value: min }, { value: max }]
}
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


                            <h2>
                                {k}
                            </h2>
                            <div className='eachContinuousVar'>
                                {/* <div className='min'>{value[ind].min}</div> */}

                                <Box className='slider'>


                                    <Slider id={k} min={value[ind].min} max={value[ind].max} name={k} defaultValue={[value[ind].min, value[ind].max]}
                                        valueLabelDisplay="auto" size='small' marks={[{ value: value[ind].min, label: value[ind].min }, { value: value[ind].max, label: value[ind].max }]}></Slider>
                                    {/* <Slider id={k} min={value[ind].min} max={value[ind].max} name={k} defaultValue={[value[ind].min, value[ind].max]}
                                        valueLabelDisplay="auto" size='small' ></Slider> */}
                                </Box>
                                {/* <div className='max'>{value[ind].max}</div> */}

                            </div>

                        </div>
                    ))}


                </center>
            </div>
        )
    }
}

export default getConti;