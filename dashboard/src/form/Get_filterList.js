import React, { useEffect, useState } from 'react';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
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



function GetFilterList({ list, form_Data, set_FormData, formFrame, setkey_Category, setvalue_Category, setkey_Continuous, setvalue_Continuous, key_Category, value_Category, key_Continuous, value_Continuous }) {
    const handleChange = (event) => {
        const { name, value: value_choosen_filter_list } = event.target;
        //to do here
        console.log(event.target)
        console.log(form_Data.filter_list)
        set_FormData((prevFormData) => ({
            ...prevFormData,
            [name]: value_choosen_filter_list,
        }));
        let agent_cate_key = []
        let agent_cate_value = []
        let agent_conti_key = []
        let agent_conti_value = []
        let filter_return = formFrame.filter;

        // list.forEach(element => {
        //     if (event.target.value.includes(element)) {
        //         agent_cate_key.push(element)
        //         agent_cate_value.push(filter_return.categorical[element])
        //     }
        //     if (event.target.value.includes(element)) {
        //         agent_conti_key.push(element)
        //         agent_conti_value.push(filter_return.continuous[element])
        //     }
        // });
        // 
        // console.log(event.target.value)
        key_Category.forEach(key => {
            if(!value_choosen_filter_list.includes(key))
            {
                set_FormData((prevState) => ({
                    ...prevState,
                    filter: {
                        ...prevState.filter,
                        categorical: {
                            ...prevState.filter.categorical,
                            [key]: [],
                        },
                    },
                }))
            }
        });
        key_Continuous.forEach(key =>{
            if(!value_choosen_filter_list.includes(key))
            {
                set_FormData((prevState) => ({
                    ...prevState,
                    filter: {
                        ...prevState.filter,
                        continuous: {
                            ...prevState.filter.continuous,
                            [key]: formFrame.filter.continuous[key],
                        },
                    },
                }))
            }
        })
        
            event.target.value.forEach(element => {

                if (element in formFrame.filter.categorical) {
                    console.log('cate' + element)
                    agent_cate_key.push(element)
                    agent_cate_value.push(filter_return.categorical[element])
                }
                if (element in formFrame.filter.continuous) {
                    console.log('conti' + element)
                    agent_conti_key.push(element)
                    agent_conti_value.push(filter_return.continuous[element])
                }
            });
        // console.log(agent_cate_key,agent_cate_key)
        // for (let key in filter_return.categorical) {
        //     if (event.target.value.includes(key)) {
        //         agent_cate_key.push(key)
        //         agent_cate_value.push(filter_return.categorical[key])
        //     }
        // }
        // for (let key in filter_return.continuous) {
        //     if (event.target.value.includes(key)) {
        //         agent_conti_key.push(key)
        //         agent_conti_value.push(filter_return.continuous[key])
        //     }
        // }



        setkey_Category(agent_cate_key)
        setvalue_Category(agent_cate_value)
        setkey_Continuous(agent_conti_key)
        setvalue_Continuous(agent_conti_value)

        // const initial_cate = {};
        // agent_cate_key.forEach(item => {
        //     initial_cate[item] = [];
        // });

        // let update_upon_formFrame = { ...form_Data }
        // update_upon_formFrame.filter.categorical = initial_cate
        // update_upon_formFrame.filter.continuous = formFrame.filter.continuous
        // update_upon_formFrame.field = ''
        // update_upon_formFrame.aggregate = []
        // update_upon_formFrame.group_by = []
        // update_upon_formFrame.filter_list = []
        // set_FormData(update_upon_formFrame)
    };

    // useEffect(() => {
    //     setkey_Category([])
    //     setvalue_Category([])
    //     setkey_Continuous([])
    //     setvalue_Continuous([])
    // },[formFrame])

    if (list !== undefined) {
        list.sort((a, b) => a.localeCompare(b))
        return (

            <div>
                <FormControl sx={{ m: 1, width: '95%' }}>
                    <InputLabel id="groupBy-multiple-checkbox-label">Filter List</InputLabel>
                    <Select
                        labelId="groupBy-multiple-checkbox-label"
                        id="groupBy-multiple-checkbox"
                        multiple
                        value={form_Data.filter_list}
                        onChange={handleChange}
                        input={<OutlinedInput label="Tag" />}
                        renderValue={(selected) => (
                            selected.map((value) => (
                                <Chip key={value} label={value} />
                            ))
                        )}
                        MenuProps={MenuProps}
                        name='filter_list'
                    >
                        {list.map((name) => (
                            <MenuItem key={name} value={name}>
                                <Checkbox checked={form_Data.filter_list.indexOf(name) > -1} />
                                <ListItemText primary={name} />
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </div>


        )
    }
}

export default GetFilterList;