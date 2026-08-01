const ReportModel = require('../models/ReportModel');

class ReportController {
    static async getFinancialReport(req, res, next) {
        try {
            const report = await ReportModel.getFinancialReport();
            res.status(200).json(report);
        } catch (error) {
            next(error);
        }
    }
}

module.exports = ReportController;
