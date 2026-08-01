const db = require('../config/database');

class UserModel {
    static async findByEmail(email) {
        return await db.getAsync("SELECT id FROM users WHERE email = ?", [email]);
    }

    static async create(name, email, pass) {
        const result = await db.runAsync("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", [name, email, pass]);
        return result.lastID;
    }

    static async delete(id) {
        await db.runAsync("DELETE FROM users WHERE id = ?", [id]);
    }
}

module.exports = UserModel;
