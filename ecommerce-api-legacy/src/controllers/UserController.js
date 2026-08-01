const UserModel = require('../models/UserModel');

class UserController {
    static async deleteUser(req, res, next) {
        try {
            const { id } = req.params;
            await UserModel.delete(id);
            res.status(200).json({ msg: "Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco." });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = UserController;
