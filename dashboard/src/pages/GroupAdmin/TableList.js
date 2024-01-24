// import React, { useState, useEffect } from "react";
// import { Button } from "@mui/material";
// import {
//   Table,
//   TableBody,
//   TableCell,
//   TableContainer,
//   TableHead,
//   TableRow,
//   Paper,
// } from "@mui/material";
// import HOST from "../../config/path";

// const TableList = ({ selectedOption }) => {
//   const [data, setData] = useState([]);
//   const url_user = "/group_admin/info/";
//   const url_data = "/group_admin/data";
//   const url_job = "/group_admin/job";
//   const url_pipline = "/group_admin/pipline"
//   useEffect(
//     (id) => {
//       // Fetch data from MySQL or your API here
//       // Example: Fetching data using fetch
//       let url = "";
//       if (selectedOption === "user") {
//         url = url_user + id;
//       } else if (selectedOption === "mydata") {
//         url = url_data;
//       } else if (selectedOption === "myjob") {
//         url = url_job ;
//       }
//       else if (selectedOption === "mypipline") {
//         url = url_pipline ;
//       }
//       fetch(HOST + url)
//         .then((response) => response.json())
//         .then((result) => {
//           setData(result);
//         })
//         .catch((error) => {
//           console.error("Error fetching data:", error);
//         });
//     },
//     [selectedOption]
//   );

//   const columns = data.length > 0 ? Object.keys(data[0]) : [];

//   const generateTableContent = () => {
//     const commonTable = (
//       <TableContainer component={Paper}>
//         <Table>
//           <TableHead>
//             <TableRow>
//               {columns.map((column) => (
//                 <TableCell key={column}>{column}</TableCell>
//               ))}
//             </TableRow>
//           </TableHead>
//           <TableBody>
//             {data.map((row, index) => (
//               <TableRow key={index}>
//                 {columns.map((column) => (
//                   <TableCell key={column}>{row[column]}</TableCell>
//                 ))}
//               </TableRow>
//             ))}
//           </TableBody>
//         </Table>
//       </TableContainer>
//     );

//     let customContent = null;
//     let customButton = null;

//     if (selectedOption === "user") {
//       customContent = commonTable;
//     } else if (selectedOption === "mydata") {
//       customContent = commonTable;
//       customButton = (
//         <Button
//           variant="contained"
//           color="primary"
//           style={{ marginTop: "20px" }}
//         >
//           New Index
//         </Button>
//       );
//     } else if (selectedOption === "myjob") {
//       customContent = commonTable;
//       customButton = (
//         <Button
//           variant="contained"
//           color="primary"
//           style={{ marginTop: "20px" }}
//         >
//           New Job
//         </Button>
//       );
//     }
//     else if (selectedOption === "mypipline") {
//       customContent = commonTable;
//       customButton = (
//         <Button
//           variant="contained"
//           color="primary"
//           style={{ marginTop: "20px" }}
//         >
//           New Pipline
//         </Button>
//       );
//     }

//     return { customContent, customButton };
//   };

//   const { customContent, customButton } = generateTableContent();

//   return (
//     <Paper elevation={2} style={{ padding: "20px", marginLeft: "20px" }}>
//       {customContent}
//       {customButton}
//     </Paper>
//   );
// };

// export default TableList;
import React, { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
} from "@mui/material";
import HOST from "../../config/path";

const TableList = ({ selectedOption }) => {
  const [data, setData] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });
  const url_user = "/group_admin/info/";
  const url_data = "/group_admin/data";
  const url_job = "/group_admin/job";
  const url_pipline = "/group_admin/pipline";
  useEffect(
    (id) => {
      // Fetch data from MySQL or your API here
      // Example: Fetching data using fetch
      let url = "";
      if (selectedOption === "user") {
        url = url_user + id;
      } else if (selectedOption === "mydata") {
        url = url_data;
      } else if (selectedOption === "myjob") {
        url = url_job;
      } else if (selectedOption === "mypipline") {
        url = url_pipline;
      }
      fetch(HOST + url)
        .then((response) => response.json())
        .then((result) => {
          setData(result);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    [selectedOption]
  );

  const columns = data.length > 0 ? Object.keys(data[0]) : [];

  const requestSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedData = () => {
    if (sortConfig.key) {
      const sorted = [...data].sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
      return sorted;
    }
    return data;
  };

  const renderTableHeader = () => (
    <TableRow>
      {columns.map((column) => (
        <TableCell key={column}>
          <Button style={{ paddingLeft: 0 }} onClick={() => requestSort(column)}>
            {column}{' '}
            {sortConfig.key === column && (
              <span>{sortConfig.direction === 'asc' ? '▲' : '▼'}</span>
            )}
          </Button>
        </TableCell>
      ))}
    </TableRow>
  );

  const renderTableRows = () => (
    sortedData().map((row, index) => (
      <TableRow key={index}>
        {columns.map((column) => (
          <TableCell key={column}>{row[column]}</TableCell>
        ))}
      </TableRow>
    ))
  );

  const newIndexButton = selectedOption !== 'user' && (
    <Button variant="contained" color="primary" style={{ marginTop: '20px' ,marginRight:'20px', float:"right"}}>
      New {selectedOption === 'mydata' ? 'Index' : selectedOption.charAt(2).toUpperCase() + selectedOption.slice(3)}
    </Button>
  );

  return (
    <Paper elevation={2} style={{ padding: '20px', marginLeft: '20px' }}>
      <TableContainer >
      {newIndexButton}
        <Table>
          <TableHead>{renderTableHeader()}</TableHead>
          <TableBody>{renderTableRows()}</TableBody>
        </Table>
      </TableContainer>
      
    </Paper>
  );
};

export default TableList;
