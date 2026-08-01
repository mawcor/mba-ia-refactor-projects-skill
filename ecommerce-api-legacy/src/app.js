const express = require('express');
const { config } = require('./config/settings');
const dbInstance = require('./config/database');
const apiRoutes = require('./routes/api_routes');
const { errorHandler } = require('./utils/error_handler');

const app = express();
app.use(express.json());

// Init DB
dbInstance.initDb();

// Routes
app.use('/api', apiRoutes);

// Error handling middleware
app.use(errorHandler);

app.listen(config.port, () => {
    console.log(`Frankenstein LMS rodando na porta ${config.port}...`);
});
