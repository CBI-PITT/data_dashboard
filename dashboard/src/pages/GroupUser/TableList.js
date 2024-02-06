import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import HOST from "../../config/path";
import Modal from './JobModal';
import "./GroupUser.css"

const TableList = ({ selectedOption }) => {
  const [data, setData] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });
  const url_user = "/group_user/info/";
  const url_data = "/group_user/data/";
  const url_jobs = "/group_user/jobs/";
  useEffect(
    (id) => {
      // Fetch data from MySQL or your API here
      // Example: Fetching data using fetch
      let url = "";
      if (selectedOption === "user") {
        url = url_user;
      } else if (selectedOption === "mydata") {
        url = url_data;
      } else if (selectedOption === "myjob") {
        url = url_jobs;
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

  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleNewJobClick = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const newIndexButton = selectedOption !== 'user' && (
    <Button variant="contained" color="primary" style={{ marginTop: '20px' ,marginRight:'20px', float:"right"}}>
      New Index
    </Button>
  );

  const newJobButton = selectedOption !== 'user' && (
    <Button onClick={handleNewJobClick} variant="contained" color="primary" style={{ marginTop: '20px' ,marginRight:'20px', float:"right"}}>
      New Job JSON
    </Button>
  );

  return (
    <Paper elevation={2} style={{ padding: '20px', marginLeft: '20px' }}>
      <TableContainer >
      {selectedOption === 'mydata' ? newIndexButton : newJobButton}
        <Modal isOpen={isModalOpen} onClose={handleCloseModal} />
        <Table>
          <TableHead>{renderTableHeader()}</TableHead>
          <TableBody>{renderTableRows()}</TableBody>
        </Table>
      </TableContainer>
      
    </Paper>
  );
};

export default TableList;
