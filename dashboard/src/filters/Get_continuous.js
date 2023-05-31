import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import { useState } from 'react';
import Typography from '@mui/material/Typography';
import * as React from 'react';



function setting(min, max) {
    return [{ value: min }, { value: max }]
}
function GetConti({key_Continuous, value_Continuous}) {
    // const key = ["Treatment", "Time_Point"]
    // const value = [["eeve", "weev", "vvev"], [24, 48, 72, 96]]
    // const [valueSlider,setValueSlider] = useState([])

    // const onChangeValue = (event,newValue) =>{
    //     setValueSlider(newValue)
    // }



    if (key_Continuous !== undefined && value_Continuous !== undefined) {
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

                    {key_Continuous.map((k, ind) => (
                        <div>


                            {/* <h2>
                                {k}
                            </h2> */}
                            <Typography  gutterBottom>
                                {k}
                            </Typography>
                            <div className='eachContinuousVar'>
                                {/* <div className='min'>{value[ind].min}</div> */}

                                <Box className='slider'>


                                    <Slider id={k} min={value_Continuous[ind].min} max={value_Continuous[ind].max} name={k} defaultValue={[value_Continuous[ind].min, value_Continuous[ind].max]}
                                        valueLabelDisplay="auto" size='small' marks={[{ value: value_Continuous[ind].min, label: value_Continuous[ind].min }, { value: value_Continuous[ind].max, label: value_Continuous[ind].max }]}></Slider>
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

export default GetConti;