import React, { useState, useEffect } from "react";
import {
  Select,
  MenuItem,
  Table,
  TableContainer,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Paper,
  Typography,
} from "@mui/material";
import HOST from "../../config/path";
import Header from "../Dashboard/Component/layout/header";
const styles = {
  container: {
    maxWidth: "1800px",
    margin: "0 auto",
    overflowX: "hidden",
    padding: "16px",
  },
  root: {
    backgroundColor: "#f9f9f9",
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
    marginBottom: "20px",
    padding: "16px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
  },
  head: {
    backgroundColor: "#3498db", // Blue background color for table header
    color: "white", // Apply alternate row colors
  },
};

const YourComponent = () => {
  const [data, setData] = useState([]);
  const [selectedEsIndex, setSelectedEsIndex] = useState('');
  const [filteredData, setFilteredData] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch(HOST + '/indexInfo');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const jsonData = await response.json();
      setData(jsonData);

      const uniqueEsIndexes = [...new Set(jsonData.map(item => item.es_index))];
      if (uniqueEsIndexes.length > 0) {
        setSelectedEsIndex(uniqueEsIndexes[0]);
        filterDataByEsIndex(uniqueEsIndexes[0], jsonData);
      }
    } catch (error) {
      console.error('There was a problem fetching the data:', error);
    }
  };

  const handleChange = (event) => {
    const selectedValue = event.target.value;
    setSelectedEsIndex(selectedValue);
    filterDataByEsIndex(selectedValue, data);
  };

  const filterDataByEsIndex = (esIndex, allData) => {
    const filtered = allData.filter(item => item.es_index === esIndex);
    setFilteredData(filtered);
  };

  // Get unique keys for table headers
  const tableHeaders = [...new Set(data.flatMap(item => Object.keys(item)))];
  const isEven = (num) => num % 2 === 0;
  return (
    <div style={styles.container}>
      <Header />
      <Paper style={styles.root}>
        <Typography variant="h4" gutterBottom>
          Field Information
        </Typography>
        <Select
          value={selectedEsIndex}
          onChange={handleChange}
          variant="outlined"
          
        >
          {[...new Set(data.map(item => item.es_index))].map((esIndex) => (
            <MenuItem key={esIndex} value={esIndex}>
              {esIndex}
            </MenuItem>
          ))}
        </Select>
      </Paper>
      <TableContainer component={Paper} style={styles.tableContainer}>
        <Table >
          <TableHead style={styles.head}>
            <TableRow>
              {tableHeaders.map((header, index) => (
                <TableCell key={index}>{header}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredData.map((item, index) => (
                <TableRow key={index} style={{ backgroundColor: isEven(index) ? '#f9f9f9' : 'inherit' }}>
                {tableHeaders.map((header, idx) => (
                  <TableCell key={idx}>{item[header]}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default YourComponent;
