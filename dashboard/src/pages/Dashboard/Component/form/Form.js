import GetAggregation from "./Get_aggregation";
import GetCate from "./Get_categorical";
import GetConti from "./Get_continuous";
import GetField from "./Get_field";
import GetGroupBy from "./Get_groupBy";
import GetFilterList from "./Get_filterList";
import Box from "@mui/material/Box";
import React, { useEffect, useState } from "react";
import Skeleton from "@mui/material/Skeleton";
import { Button, Paper, Alert } from "@mui/material";
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import SendIcon from "@mui/icons-material/Send";
import DeleteIcon from "@mui/icons-material/Delete";
import HOST from "../../../../config/path";
function Form({
  setDisplayData,
  setFormDataCurrent,
  type_fields_dict,
  setType_field_dict,
  formFrame,
  meta,
  setN_value,
  setOriginalArray,
  setSortCondition,
  setTopN,
}) {
  const [Field_axis_list, setField_axis_list] = useState();

  const [key_Category, setkey_Category] = useState([]);
  const [value_Category, setvalue_Category] = useState([]);
  const [key_Continuous, setkey_Continuous] = useState([]);
  const [value_Continuous, setvalue_Continuous] = useState([]);
  const [open, setOpen] = useState(false);
  const [GroupBy_list, setGroupBy_List] = useState();
  const [Aggregation_list, setAggregation_list] = useState();
  const [filter_list, setFilter_list] = useState();

  const url_query = "/api/query";

  const [formDataUpdated, setFormDataUpdated] = useState({
    filter_list: [],
    field: "",
    filter: { categorical: {}, continuous: {} },
    group_by: [],
    aggregate: [],
  });

  useEffect(() => {
    if (formFrame === undefined || formFrame === "dataset retrieving") {
      return;
    } else {
      setType_field_dict(formFrame.field);

      // let acronym_volume_return = formFrame.acronym_volume
      // setAcronym_volume(acronym_volume_return)

      let field_list_return = Object.keys(formFrame.field);
      setField_axis_list(field_list_return);

      let groupBy_list_return = formFrame.group_by;
      setGroupBy_List(groupBy_list_return);

      let aggregation_list_return = formFrame.aggregate;
      setAggregation_list(aggregation_list_return);
      
      let filter_list = formFrame.filter_list;
      setFilter_list(filter_list);

      let agent_cate_key = [];
      let agent_cate_value = [];
      let agent_conti_key = [];
      let agent_conti_value = [];
      let filter_return = formFrame.filter;
      for (let key in filter_return.categorical) {
        agent_cate_key.push(key);
        agent_cate_value.push(filter_return.categorical[key]);
      }
      for (let key in filter_return.continuous) {
        agent_conti_key.push(key);
        agent_conti_value.push(filter_return.continuous[key]);
      }

      // setkey_Category(agent_cate_key)
      // setvalue_Category(agent_cate_value)
      // setkey_Continuous(agent_conti_key)
      // setvalue_Continuous(agent_conti_value)

      const initial_cate = {};
      agent_cate_key.forEach((item) => {
        initial_cate[item] = [];
      });

      let update_upon_formFrame = { ...formDataUpdated };
      update_upon_formFrame.filter.categorical = initial_cate;
      update_upon_formFrame.filter.continuous = formFrame.filter.continuous;
      update_upon_formFrame.field = "";
      update_upon_formFrame.aggregate = [];
      update_upon_formFrame.group_by = [];
      update_upon_formFrame.filter_list = [];
      setFormDataUpdated(update_upon_formFrame);
      setkey_Category([]);
      setvalue_Category([]);
      setkey_Continuous([]);
      setvalue_Continuous([]);
    }
  }, [formFrame]);

  // useEffect(() => {
  //     for(let key in key_Category)
  //     {
  //         if(!filter_list.includes(key))
  //         {

  //         }
  //     }
  // },[filter_list])

  // useEffect(() => {
  //     const initial_cate = {};
  //     agent_cate_key.forEach(item => {
  //         initial_cate[item] = [];
  //     });
  //     let update_Cate = {...formDataUpdated}
  //     update_Cate.filter.categorical = initial_cate
  //     setFormDataUpdated(update_Cate)

  // }, [agent_cate_key.length, agent_cate_value.length])

  // if(formFrame === undefined)
  // {
  //     return
  // }

  // else {
  //     setType_field_dict(formFrame.field)
  //     let field_list_return = Object.keys(formFrame.field)
  //     setField_axis_list(field_list_return)

  //     let filter_return = formFrame.filter;
  //     // console.log(filter_return)
  //     let agent_cate_key = []
  //     let agent_cate_value = []
  //     let agent_conti_key = []
  //     let agent_conti_value = []
  //     for (let key in filter_return.categorical) {
  //         agent_cate_key.push(key)
  //         agent_cate_value.push(filter_return.categorical[key])
  //     }
  //     for (let key in filter_return.continuous) {
  //         agent_conti_key.push(key)
  //         agent_conti_value.push(filter_return.continuous[key])
  //     }
  //     // Filter setting
  //     setkey_Category(agent_cate_key)
  //     setvalue_Category(agent_cate_value)
  //     setkey_Continuous(agent_conti_key)
  //     setvalue_Continuous(agent_conti_value)

  //     let groupBy_list_return = formFrame.group_by
  //     setGroupBy_List(groupBy_list_return)

  //     let aggregation_list_return = formFrame.aggregate
  //     setAggregation_list(aggregation_list_return)
  // }

  // useEffect(() => {
  //     // Request for field list
  //     axios.get(HOST + url_field).then((response) => {
  //         setType_field_dict(response.data)

  //         let field_list_return = Object.keys(response.data)
  //         // console.log(type_fields_dict)

  //         setField_axis_list(field_list_return)
  //         // setY_axis_list(xyAxis_list_return)
  //         // console.log(X_axis_list)

  //     })
  //     // Request for filter(key,value)
  //     axios.get(HOST + url_filter).then((response) => {
  //         // console.log("filter return", response.data)
  //         // let filter_return = JSON.parse(response.data.replace(/\bNaN\b/g, "null"));
  //         let filter_return = response.data;
  //         // console.log(filter_return)
  //         let agent_cate_key = []
  //         let agent_cate_value = []
  //         let agent_conti_key = []
  //         let agent_conti_value = []
  //         for (let key in filter_return.categorical) {
  //             agent_cate_key.push(key)
  //             agent_cate_value.push(filter_return.categorical[key])
  //         }
  //         for (let key in filter_return.continuous) {
  //             agent_conti_key.push(key)
  //             agent_conti_value.push(filter_return.continuous[key])
  //         }
  //         // Filter setting
  //         setkey_Category(agent_cate_key)
  //         setvalue_Category(agent_cate_value)
  //         setkey_Continuous(agent_conti_key)
  //         setvalue_Continuous(agent_conti_value)
  //     });
  //     // Request for groupBy list
  //     axios.get(HOST + url_groupBy).then((response) => {
  //         // console.log("groupBy return", typeof (response.data))
  //         let groupBy_list_return = response.data
  //         setGroupBy_List(groupBy_list_return)
  //         //  console.log(GroupBy_list)
  //     })
  //     // Request for aggregation list
  //     axios.get(HOST + url_aggregation).then((response) => {
  //         // console.log(response.data.data)
  //         let aggregation_list_return = response.data.data
  //         setAggregation_list(aggregation_list_return)
  //         //  console.log(Agrregation_list)
  //     })
  // }, [])
  function calculateUniqueValues_key_array(array, position) {
    const uniqueValues = new Set();

    // Iterate through the array of objects
    array.forEach((obj) => {
      // Get the value at position 0 in the key array
      const valueAtIndex0 = obj.key[position];

      // Add the value to the set to maintain uniqueness
      uniqueValues.add(valueAtIndex0);
    });
    console.log("key_array", uniqueValues.size);
    return uniqueValues.size; // Return the count of unique values
  }
  function calculateUniqueValues_key_string(array) {
    const uniqueValues = new Set();

    // Iterate through the array of objects
    array.forEach((obj) => {
      // Get the value at position 0 in the key array
      const valueAtIndex0 = obj.key;

      // Add the value to the set to maintain uniqueness
      uniqueValues.add(valueAtIndex0);
    });
    console.log("key_string", uniqueValues.size);
    return uniqueValues.size; // Return the count of unique values
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    // console.log(event)
    setOpen(true);
    setN_value("Calculating...");

    let formData_boxplot_add = JSON.parse(JSON.stringify(formDataUpdated));

    if (type_fields_dict[formData_boxplot_add["field"]] !== "keyword") {
      formData_boxplot_add["aggregate"].push("boxplot");
    }
    var formData_send = JSON.stringify(formData_boxplot_add);

    // var formData_send = JSON.stringify(formData)
    // console.log(formDataUpdated)

    console.log("client request send", formData_send);

    fetch(HOST + url_query, {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: formData_send,
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("server data received", data);

        if (
          formData_boxplot_add.group_by.includes(meta.metadata_calculation_name)
        ) {
          if (formData_boxplot_add.group_by.length === 1) {
            setN_value(calculateUniqueValues_key_string(data));
          } else {
            setN_value(
              calculateUniqueValues_key_array(
                data,
                formDataUpdated.group_by.indexOf(meta.metadata_calculation_name)
              )
            );
          }
        }
        setDisplayData(data);
        setOriginalArray(data);
        
        setSortCondition('')
        setTopN('')
        setFormDataCurrent(formDataUpdated);
        setOpen(false);

        // console.log("setDisplayData", displayData)
      })
      .catch((error) => {
        console.log(error);
        // debugger;
      });
    let formData_n_value = JSON.parse(JSON.stringify(formDataUpdated));
    if (!formData_n_value.group_by.includes(meta.metadata_calculation_name)) {
      if (meta.metadata_calculation_name == null) {
        setN_value("Not Available");
        return;
      }

      // push metadata_calculation_name to the array
      formData_n_value.group_by.push(meta.metadata_calculation_name);
      formData_send = JSON.stringify(formData_n_value);
      console.log("client request send with metadata", formData_send);
      fetch(HOST + url_query, {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        body: formData_send,
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("server data received for N", data);
          setN_value(
            calculateUniqueValues_key_array(
              data,
              formData_n_value.group_by.indexOf(meta.metadata_calculation_name)
            )
          );
        })
        .catch((error) => {
          console.log(error);
          // debugger;
        });
    }
  };

  const handleReset = () => {
    const rest_formData = { ...formDataUpdated };
    rest_formData.field = "";
    let initial_cate = {};
    key_Category.forEach((item) => {
      initial_cate[item] = [];
    });
    rest_formData.filter.categorical = initial_cate;
    rest_formData.filter.continuous = formFrame.filter.continuous;
    console.log(key_Category);
    rest_formData.group_by = [];
    rest_formData.aggregate = [];

    setFormDataUpdated(rest_formData);
  };

  if (formFrame !== undefined && formFrame !== "dataset retrieving") {
    return (
      <Paper
        component={"form"}
        variant="elevation"
        elevation={10}
        className="form"
        style={{ backgroundColor: "#feeeed" }}
        onSubmit={handleSubmit}
      >
        <Backdrop
          sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
          open={open}
        >
          <CircularProgress color="inherit" />
        </Backdrop>
        <div className="form_main">
          <div className="filter_list">
            <br></br>
            <GetFilterList
              list={filter_list}
              form_Data={formDataUpdated}
              set_FormData={setFormDataUpdated}
              formFrame={formFrame}
              setkey_Category={setkey_Category}
              setvalue_Category={setvalue_Category}
              setkey_Continuous={setkey_Continuous}
              setvalue_Continuous={setvalue_Continuous}
              key_Category={key_Category}
              value_Category={value_Category}
              key_Continuous={key_Continuous}
              value_Continuous={value_Continuous}
            />
            <br></br>
          </div>
          <div className="filter">
            <div></div>
            <div className="continuous">
              <GetConti
                key_Continuous={key_Continuous}
                value_Continuous={value_Continuous}
                form_Data={formDataUpdated}
                set_FormData={setFormDataUpdated}
              />
            </div>

            <div className="categorical">
              <GetCate
                key_category={key_Category}
                value_category={value_Category}
                formData={formDataUpdated}
                set_FormData={setFormDataUpdated}
              />
            </div>
          </div>
          <div className="groupBy">
            <br></br>
            <GetGroupBy
              list={GroupBy_list}
              form_Data={formDataUpdated}
              set_FormData={setFormDataUpdated}
            />
            <br></br>
          </div>
          <div className="field">
            <br></br>
            <GetField
              list={Field_axis_list}
              form_Data={formDataUpdated}
              set_FormData={setFormDataUpdated}
            />
            <br></br>
            <br></br>
          </div>
          <div className="aggregation">
            <br></br>
            <GetAggregation
              list={Aggregation_list}
              form_Data={formDataUpdated}
              set_FormData={setFormDataUpdated}
              field_status={type_fields_dict[formDataUpdated.field]}
            />
            <br></br>
            <br></br>
          </div>
        </div>
        <br></br>
        <div>
          <Button
            type="reset"
            variant="contained"
            color="inherit"
            size="small"
            id="reset"
            endIcon={<DeleteIcon />}
            onClick={handleReset}
          >
            Reset
          </Button>
          <Button
            type="submit"
            variant="contained"
            color="inherit"
            size="small"
            id="send"
            endIcon={<SendIcon />}
          >
            Send
          </Button>
        </div>
        <br></br>
      </Paper>
    );
  } else {
    return (
      <div className="form">
        <Paper
          component={"form"}
          variant="elevation"
          elevation={10}
          className="form_data"
          style={{ backgroundColor: "#feeeed" }}
        >
          <br></br>
          {formFrame === "dataset retrieving" ? (
            <div>
              <Alert className="dataset_alert" severity="success">
                Dataset is retrieving — <strong>Please wait</strong>
              </Alert>
              <Box className="filter">
                <Skeleton animation="wave" variant="rounded" height={60} />
              </Box>
              <br></br>
              <Box className="groupBy">
                <Skeleton animation="wave" variant="rounded" height={60} />
              </Box>
              <br></br>
              <Box className="field">
                <Skeleton animation="wave" variant="rounded" height={60} />
              </Box>
              <br></br>
              <Box className="aggregation">
                <Skeleton animation="wave" variant="rounded" height={60} />
              </Box>

              <br></br>
            </div>
          ) : (
            <Alert className="dataset_alert" severity="info">
              Dataset is waiting to be selected —{" "}
              <strong>Please choose one!</strong>
            </Alert>
          )}
          <br></br>
        </Paper>
      </div>
    );
  }
}

export default Form;
