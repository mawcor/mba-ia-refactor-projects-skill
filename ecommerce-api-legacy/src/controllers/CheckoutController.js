const CourseModel = require('../models/CourseModel');
const UserModel = require('../models/UserModel');
const EnrollmentModel = require('../models/EnrollmentModel');
const PaymentModel = require('../models/PaymentModel');
const AuditLogModel = require('../models/AuditLogModel');
const { badCrypto } = require('../utils/crypto');
const { logAndCache } = require('../utils/cache');
const { AppError } = require('../utils/error_handler');

class CheckoutController {
    static async processCheckout(req, res, next) {
        try {
            const { usr: u, eml: e, pwd: p, c_id: cid, card: cc } = req.body;

            if (!u || !e || !cid || !cc) {
                throw new AppError("Bad Request", 400);
            }

            const course = await CourseModel.getActiveById(cid);
            if (!course) {
                throw new AppError("Curso não encontrado", 404);
            }

            let user = await UserModel.findByEmail(e);
            let userId;

            if (!user) {
                const hash = badCrypto(p || "123456");
                userId = await UserModel.create(u, e, hash);
            } else {
                userId = user.id;
            }

            // Payment logic
            const status = cc.startsWith("4") ? "PAID" : "DENIED";
            if (status === "DENIED") {
                throw new AppError("Pagamento recusado", 400);
            }

            const enrollmentId = await EnrollmentModel.create(userId, cid);
            await PaymentModel.create(enrollmentId, course.price, status);
            await AuditLogModel.create(`Checkout curso ${cid} por ${userId}`);

            logAndCache(`last_checkout_${userId}`, course.title);

            res.status(200).json({ msg: "Sucesso", enrollment_id: enrollmentId });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = CheckoutController;
