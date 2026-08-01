const db = require('../config/database');

class ReportModel {
    static async getFinancialReport() {
        const query = `
            SELECT c.id as course_id, c.title as course, 
                   u.name as student, 
                   p.amount as paid, 
                   p.status 
            FROM courses c
            LEFT JOIN enrollments e ON c.id = e.course_id
            LEFT JOIN payments p ON e.id = p.enrollment_id
            LEFT JOIN users u ON e.user_id = u.id
        `;
        const rows = await db.allAsync(query);
        
        // Group rows by course
        const reportMap = {};
        for (const row of rows) {
            if (!reportMap[row.course_id]) {
                reportMap[row.course_id] = {
                    course: row.course,
                    revenue: 0,
                    students: []
                };
            }
            
            if (row.status === 'PAID') {
                reportMap[row.course_id].revenue += row.paid;
            }
            
            if (row.student) {
                reportMap[row.course_id].students.push({
                    student: row.student,
                    paid: row.paid || 0
                });
            }
        }
        
        return Object.values(reportMap);
    }
}

module.exports = ReportModel;
