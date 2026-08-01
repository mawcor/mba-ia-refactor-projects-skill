function errorHandler(err, req, res, next) {
    console.error(err.stack);
    const status = err.status || 500;
    const message = err.message || "Internal Server Error";
    res.status(status).json({ error: message });
}

class AppError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
    }
}

module.exports = { errorHandler, AppError };
