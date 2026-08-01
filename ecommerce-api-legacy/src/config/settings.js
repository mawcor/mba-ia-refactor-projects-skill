require('dotenv').config();

const config = {
    dbUser: process.env.DB_USER || "admin_master",
    dbPass: process.env.DB_PASS || "default_dev_pass", 
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || "default_dev_key",
    smtpUser: process.env.SMTP_USER || "no-reply@fullcycle.com.br",
    port: process.env.PORT || 3000
};

module.exports = { config };
