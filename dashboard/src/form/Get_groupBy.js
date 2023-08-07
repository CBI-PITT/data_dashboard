import * as React from 'react';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};



// function GetGroupBy({ list, form_Data, set_FormData }) {
//     const [groupBySelected, setGroupBySelected] = React.useState([])
//     const handleChange = (event) => {
//         setGroupBySelected(event.target.value)
//         // let newFormData = form_Data
//         // newFormData.group_by = event.target.value

//         const updatedFormData = { ...form_Data }
//         updatedFormData.group_by = event.target.value
//         set_FormData(updatedFormData)
//         // formData.group_by = event.target.value
//     };
//     // console.log(list)
//     if (list !== undefined) {
//         return (

//             <div>
//                 {/* <h2>Group By</h2>
//             //     <label for="groupBy">
//             //         <select id='groupBy' name="group_by" multiple size={3}>
//             //             {
//             //                 list.map((item) => (
//             //                     <option value={item}>{item}</option>
//             //                 ))
//             //             }
//             //         </select>
//             //     </label> */}

//                 <FormControl required sx={{ m: 1, width: '95%' }}>
//                     <InputLabel id="groupBy-multiple-checkbox-label">GroupBy</InputLabel>
//                     <Select
//                         labelId="groupBy-multiple-checkbox-label"
//                         id="groupBy-multiple-checkbox"
//                         multiple
//                         value={groupBySelected}
//                         onChange={handleChange}
//                         input={<OutlinedInput label="Tag" />}
//                         renderValue={(selected) => selected.join(', ')}
//                         MenuProps={MenuProps}
//                     >
//                         {list.map((name) => (
//                             <MenuItem key={name} value={name}>
//                                 <Checkbox checked={groupBySelected.indexOf(name) > -1} />
//                                 <ListItemText primary={name} />
//                             </MenuItem>
//                         ))}
//                     </Select>
//                 </FormControl>
//             </div>


//         )
//     }
// }

// export default GetGroupBy;

function GetGroupBy({ list, form_Data, set_FormData }) {
    // const [groupBySelected, setGroupBySelected] = React.useState([])
    const handleChange = (event) => {
        const { name, value } = event.target;
        set_FormData((prevFormData) => ({
            ...prevFormData,
            [name]: value,
        }));
    };
    // console.log(list)
    if (list !== undefined) {
        list.sort((a, b) => a.localeCompare(b))
        return (

            <div>
                <FormControl required sx={{ m: 1, width: '95%' }}>
                    <InputLabel id="groupBy-multiple-checkbox-label">GroupBy</InputLabel>
                    <Select
                        labelId="groupBy-multiple-checkbox-label"
                        id="groupBy-multiple-checkbox"
                        multiple
                        value={form_Data.group_by}
                        onChange={handleChange}
                        input={<OutlinedInput label="Tag" />}
                        renderValue={(selected) => selected.join(', ')}
                        MenuProps={MenuProps}
                        name='group_by'
                    >
                        {list.map((name) => (
                            <MenuItem key={name} value={name}>
                                <Checkbox checked={form_Data.group_by.indexOf(name) > -1} />
                                <ListItemText primary={name} />
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </div>


        )
    }
}

export default GetGroupBy;