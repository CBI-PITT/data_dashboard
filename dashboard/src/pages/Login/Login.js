import React, { useState } from 'react';
import { TextField, Button, Typography, Paper, Box } from '@mui/material';

const Login = () => {
  const [account, setAccount] = useState('');
  const [password, setPassword] = useState('');

  const handleAccountChange = (event) => {
    setAccount(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    console.log('Account:', account);
    console.log('Password:', password);
    setAccount('');
    setPassword('');
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
    >
      <Paper elevation={3} style={{ padding: '20px', width: '100%', maxWidth: '400px' }}>
        <Typography variant="h5" align="center" gutterBottom>
          Login
        </Typography>
        <form onSubmit={handleFormSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="account"
            label="Account"
            name="account"
            autoComplete="account"
            value={account}
            onChange={handleAccountChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={handlePasswordChange}
          />
          <Box mt={2} display="flex" justifyContent="space-between">
            <Button
              type="submit"
              variant="contained"
              color="primary"
              size="large"
              style={{ width: '48%' }}
            >
              Sign In
            </Button>
            <Button
              variant="outlined"
              color="primary"
              size="large"
              style={{ width: '48%' }}
            >
              Sign Up
            </Button>
          </Box>
        </form>
      </Paper>
    </Box>
  );
};

export default Login;
