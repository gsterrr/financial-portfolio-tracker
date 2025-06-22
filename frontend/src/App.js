import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Container,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider,
  CircularProgress
} from '@mui/material';
import { 
  Home as HomeIcon,
  Portfolio as PortfolioIcon,
  Apartment as PropertyIcon,
  TrendingUp as TrendingIcon,
  BarChart as BarChartIcon
} from '@mui/icons-material';

function Dashboard() {
  const [netWorth, setNetWorth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/net-worth')
      .then(response => response.json())
      .then(data => {
        setNetWorth(data);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box sx={{ flexGrow: 1, mt: 2 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Net Worth Overview
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h4" color="primary">
                ${netWorth.net_worth.toLocaleString()}
              </Typography>
              <Typography variant="subtitle1">
                Total Assets: ${netWorth.total_assets.toLocaleString()}<br/>
                Total Properties: ${netWorth.total_properties.toLocaleString()}
              </Typography>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Portfolio Distribution
            </Typography>
            {/* Chart will be implemented here */}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

function Assets() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/assets')
      .then(response => response.json())
      .then(data => {
        setAssets(data);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom>
        Assets
      </Typography>
      <List>
        {assets.map(asset => (
          <React.Fragment key={asset.id}>
            <ListItem>
              <ListItemText
                primary={`${asset.name} (${asset.symbol})`}
                secondary={
                  <React.Fragment>
                    <Typography
                      component="span"
                      variant="body2"
                      color="text.primary"
                    >
                      Quantity: {asset.quantity} | Value: ${asset.current_value.toFixed(2)}
                    </Typography>
                    <Typography
                      component="span"
                      variant="body2"
                      color={asset.roi >= 0 ? 'success.main' : 'error.main'}
                    >
                      ROI: {asset.roi.toFixed(2)}%
                    </Typography>
                  </React.Fragment>
                }
              />
            </ListItem>
            <Divider />
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
}

function Properties() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/properties')
      .then(response => response.json())
      .then(data => {
        setProperties(data);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom>
        Properties
      </Typography>
      <List>
        {properties.map(prop => (
          <React.Fragment key={prop.id}>
            <ListItem>
              <ListItemText
                primary={prop.address}
                secondary={
                  <React.Fragment>
                    <Typography
                      component="span"
                      variant="body2"
                      color="text.primary"
                    >
                      Value: ${prop.current_value.toFixed(2)} | ROI: {prop.roi.toFixed(2)}%
                    </Typography>
                    <Typography
                      component="span"
                      variant="body2"
                      color="text.secondary"
                    >
                      Rental Income: ${prop.rental_income ? prop.rental_income.toFixed(2) : 'N/A'}
                    </Typography>
                  </React.Fragment>
                }
              />
            </ListItem>
            <Divider />
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
}

function App() {
  return (
    <Router>
      <div>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
              Financial Tracker
            </Typography>
            <Button color="inherit" component={Link} to="/dashboard" startIcon={<HomeIcon />}>
              Dashboard
            </Button>
            <Button color="inherit" component={Link} to="/assets" startIcon={<PortfolioIcon />}>
              Assets
            </Button>
            <Button color="inherit" component={Link} to="/properties" startIcon={<PropertyIcon />}>
              Properties
            </Button>
          </Toolbar>
        </AppBar>
        
        <Container sx={{ mt: 4 }}>
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/assets" element={<Assets />} />
            <Route path="/properties" element={<Properties />} />
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </Container>
      </div>
    </Router>
  );
}

export default App;
