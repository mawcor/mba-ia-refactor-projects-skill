const db = require('../config/database');

class CourseModel {
    static async getActiveById(id) {
        return await db.getAsync("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
    }
}

module.exports = CourseModel;
