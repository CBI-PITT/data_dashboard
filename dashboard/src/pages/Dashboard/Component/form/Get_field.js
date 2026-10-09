
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
// function GetField({ list, form_Data, set_FormData }) {

//     // console.log(list)
//     if (list !== undefined) {
//         return (
//             // <div>
//             //     {
//             //         list.map((item) => (
//             //             <span>
//             //                 {item} /
//             //             </span>
//             //         ))
//             //     }
//             // </div>
//             // <label for="x_axis"> X axis:
//             //     <select id='x_axis' name="x">
//             //         {
//             //             list.map((item) => (
//             //                 <option value={item}>{item}</option>
//             //             ))
//             //         }
//             //     </select>
//             // </label>
//             <FormControl required sx={{ m: 1, minWidth: 120 }}>
//                 <InputLabel id="x-axis-required-label">Field</InputLabel>
//                 <Select
//                     labelId="x-axis-required-label"
//                     id="x-axis-required"
//                     // value=''
//                     defaultValue={''}
//                     label="field *"
//                     name="field"
//                     onChange={(event) => {
//                         console.log("component", event.target)

//                         const updatedFormData = { ...form_Data }
//                         updatedFormData.field = event.target.value
//                         // let newFormData = form_Data
//                         // newFormData.field = event.target.value
//                         set_FormData(updatedFormData)

//                         // formData.field = event.target.value
//                     }}
//                 >
//                     {
//                         list.map((item) => (
//                             <MenuItem value={item} key={item}>{item}</MenuItem>
//                         ))
//                     }


//                 </Select>

//             </FormControl>
//         )
//     }
// }

// export default GetField;



function GetField({ list, form_Data, set_FormData }) {

    // console.log(list)
    if (list !== undefined) {
        return (
            <FormControl required sx={{ m: 1, width: '95%' }}>
                <InputLabel id="x-axis-required-label">Y</InputLabel>
                <Select
                    labelId="x-axis-required-label"
                    id="x-axis-required"
                    // value=''
                    value={form_Data.field}
                    label="Y"
                    name="field"
                    onChange={(event) => {
                        const { name, value } = event.target;
                        set_FormData((prevFormData) => ({
                            ...prevFormData,
                            [name]: value,
                        }));
                    }}
                    renderValue={(selected) => (
                        <Chip label={selected} />
                    )}
                >
                    {
                        list.map((item) => (
                            <MenuItem value={item} key={item}>{item}</MenuItem>
                        ))
                    }
                </Select>

            </FormControl>
        )
    }
}

export default GetField;