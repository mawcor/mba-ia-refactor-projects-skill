const db = require('../config/database');

class PaymentModel {
    static async create(enrollmentId, amount, status) {
        await db.runAsync("INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [enrollmentId, amount, status]);
    }
}

module.exports = PaymentModel;
