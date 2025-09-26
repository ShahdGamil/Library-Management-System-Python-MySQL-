-- database_updates.sql
SET SQL_SAFE_UPDATES = 0;

-- Add payment_date column if it doesn't exist
SELECT COUNT(*) INTO @exists 
FROM information_schema.columns 
WHERE table_schema = 'LibraryManagement'
AND table_name = 'Fines' 
AND column_name = 'payment_date';

SET @addColumn = IF(@exists = 0,
    'ALTER TABLE Fines ADD COLUMN payment_date DATE',
    'SELECT "Column already exists"');

PREPARE stmt FROM @addColumn;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Update existing paid fines with a payment date if null
UPDATE Fines f
INNER JOIN Transactions t ON f.Transactions_ID = t.Transactions_ID
SET f.payment_date = COALESCE(f.payment_date, t.Transactions_Date)
WHERE f.Paid_Status = 'Paid' 
AND f.payment_date IS NULL;

-- Drop existing views
DROP VIEW IF EXISTS vw_book_statistics;
DROP VIEW IF EXISTS vw_member_activity;
DROP VIEW IF EXISTS vw_overdue_books;
DROP VIEW IF EXISTS vw_financial_summary;
DROP VIEW IF EXISTS vw_library_statistics;

-- Create enhanced book statistics view
CREATE OR REPLACE VIEW vw_book_statistics AS
SELECT 
    b.Books_ID,
    b.Title,
    b.ISBN,
    b.book_category,
    b.AvailabilityStatus,
    COUNT(DISTINCT tb.Transaction_ID) as times_borrowed,
    GROUP_CONCAT(DISTINCT a.Author_name SEPARATOR ', ') as authors
FROM 
    Books b
    LEFT JOIN Transaction_Book tb ON b.Books_ID = tb.Books_ID
    LEFT JOIN Author_Book ab ON b.Books_ID = ab.Books_ID
    LEFT JOIN Author a ON ab.Author_ID = a.Author_ID
GROUP BY 
    b.Books_ID, b.Title, b.ISBN, b.book_category, b.AvailabilityStatus;

-- Create enhanced member activity view
CREATE OR REPLACE VIEW vw_member_activity AS
SELECT 
    m.MemberID,
    m.MemberDetails,
    COUNT(DISTINCT t.Transactions_ID) as total_transactions,
    COUNT(DISTINCT f.FineID) as total_fines,
    COALESCE(SUM(f.fine_total), 0) as total_fine_amount,
    COUNT(DISTINCT em.event_id) as events_attended,
    MAX(t.Transactions_Date) as last_transaction_date
FROM 
    Members m
    LEFT JOIN Transactions t ON m.MemberID = t.MemberID
    LEFT JOIN Fines f ON t.Transactions_ID = f.Transactions_ID
    LEFT JOIN Event_Member em ON m.MemberID = em.MemberID
GROUP BY 
    m.MemberID, m.MemberDetails;

-- Create enhanced overdue books view
CREATE OR REPLACE VIEW vw_overdue_books AS
SELECT 
    b.Books_ID,
    b.Title,
    m.MemberID,
    m.MemberDetails,
    t.Transactions_ID,
    t.Due_date,
    DATEDIFF(CURRENT_DATE, t.Due_date) as days_overdue,
    f.fine_total,
    mp.phone_no as contact_number
FROM 
    Books b
    JOIN Transaction_Book tb ON b.Books_ID = tb.Books_ID
    JOIN Transactions t ON tb.Transaction_ID = t.Transactions_ID
    JOIN Members m ON t.MemberID = m.MemberID
    LEFT JOIN Fines f ON t.Transactions_ID = f.Transactions_ID
    LEFT JOIN Member_Phone mp ON m.MemberID = mp.MemberID
WHERE 
    t.Due_date < CURRENT_DATE
    AND t.Transaction_type = 'Borrow'
    AND NOT EXISTS (
        SELECT 1 
        FROM Transaction_Book tb2 
        JOIN Transactions t2 ON tb2.Transaction_ID = t2.Transactions_ID
        WHERE tb2.Books_ID = b.Books_ID 
        AND t2.Transaction_type = 'Return'
        AND t2.Transactions_Date >= t.Transactions_Date
    );

-- Create financial summary view
CREATE OR REPLACE VIEW vw_financial_summary AS
SELECT 
    DATE_FORMAT(COALESCE(f.payment_date, t.Transactions_Date), '%Y-%m') as month,
    COUNT(DISTINCT f.FineID) as total_fines,
    COALESCE(SUM(CASE WHEN f.Paid_Status = 'Paid' THEN f.fine_total ELSE 0 END), 0) as collected_amount,
    COALESCE(SUM(CASE WHEN f.Paid_Status = 'Unpaid' THEN f.fine_total ELSE 0 END), 0) as pending_amount
FROM 
    Fines f
    JOIN Transactions t ON f.Transactions_ID = t.Transactions_ID
GROUP BY 
    DATE_FORMAT(COALESCE(f.payment_date, t.Transactions_Date), '%Y-%m');

-- Create library statistics view
CREATE OR REPLACE VIEW vw_library_statistics AS
SELECT
    (SELECT COUNT(*) FROM Books) as total_books,
    (SELECT COUNT(*) FROM Members) as total_members,
    (SELECT COUNT(*) FROM Transactions) as total_transactions,
    (
        SELECT COUNT(*)
        FROM Transactions t
        WHERE t.Transaction_type = 'Borrow'
        AND NOT EXISTS (
            SELECT 1 FROM Transactions t2
            WHERE t2.MemberID = t.MemberID
            AND t2.Transaction_type = 'Return'
            AND t2.Transactions_Date >= t.Transactions_Date
        )
    ) as active_loans,
    (
        SELECT COUNT(*)
        FROM Transactions t
        WHERE t.Due_date < CURRENT_DATE
        AND t.Transaction_type = 'Borrow'
        AND NOT EXISTS (
            SELECT 1 FROM Transactions t2
            WHERE t2.MemberID = t.MemberID
            AND t2.Transaction_type = 'Return'
            AND t2.Transactions_Date >= t.Transactions_Date
        )
    ) as overdue_books,
    (
        SELECT COALESCE(SUM(fine_total), 0)
        FROM Fines
        WHERE Paid_Status = 'Unpaid'
    ) as total_unpaid_fines;

SET SQL_SAFE_UPDATES = 1;