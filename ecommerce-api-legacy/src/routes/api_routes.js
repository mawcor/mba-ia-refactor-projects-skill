const express = require('express');
const router = express.Router();
const CheckoutController = require('../controllers/CheckoutController');
const ReportController = require('../controllers/ReportController');
const UserController = require('../controllers/UserController');

router.post('/checkout', CheckoutController.processCheckout);
router.get('/admin/financial-report', ReportController.getFinancialReport);
router.delete('/users/:id', UserController.deleteUser);

module.exports = router;
