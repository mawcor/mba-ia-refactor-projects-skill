const db = require('../config/database');

class AuditLogModel {
    static async create(action) {
        await db.runAsync("INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", [action]);
    }
}

module.exports = AuditLogModel;
