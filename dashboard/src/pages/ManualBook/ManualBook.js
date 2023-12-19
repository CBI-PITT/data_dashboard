import React from "react";
import { Container, Typography, Paper } from '@mui/material';
export default function ManualBook(){
    return (
        <Container maxWidth="md">
          <Paper elevation={3} style={{ padding: '20px', minHeight: '80vh' }}>
            <Typography variant="h4" align="center" gutterBottom>
              Manual Book
            </Typography>
            <Typography variant="body1" gutterBottom>
              Welcome to the manual book. This is an example page.
              
            </Typography>
            {/* Add more Typography or other MUI components as needed for content */}
          </Paper>
        </Container>
      );
}