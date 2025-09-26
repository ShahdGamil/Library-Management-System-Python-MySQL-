-- sql2.sql
DROP DATABASE IF EXISTS LibraryManagement;
CREATE DATABASE IF NOT EXISTS LibraryManagement;
USE LibraryManagement;

-- Set global timeout variables
SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_write_timeout = 600;
SET GLOBAL connect_timeout = 600;
SET GLOBAL wait_timeout = 600;
SET GLOBAL interactive_timeout = 600;

-- =============================================
-- TABLES
-- =============================================
CREATE TABLE Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    MemberDetails VARCHAR(255) NOT NULL,
    RegistrationDate DATE NOT NULL,
    Loan_History TEXT
) ENGINE=InnoDB AUTO_INCREMENT=1;

CREATE TABLE Books (
    Books_ID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    description TEXT,
    Publish_date DATE,
    book_category VARCHAR(50),
    Price DECIMAL(10,2),
    ISBN VARCHAR(13),
    AvailabilityStatus VARCHAR(20)
);

CREATE TABLE Author (
    Author_ID INT PRIMARY KEY AUTO_INCREMENT,
    Author_name VARCHAR(100),
    Email VARCHAR(100),
    phone_no VARCHAR(20)
);

CREATE TABLE Publisher (
    Publisher_ID INT PRIMARY KEY AUTO_INCREMENT,
    Pub_Name VARCHAR(100),
    language VARCHAR(50)
);

CREATE TABLE Staff (
    Staff_ID INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(100),
    address VARCHAR(255),
    phone_no VARCHAR(20)
);

CREATE TABLE Staff_Phone (
    Staff_ID INT NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    PRIMARY KEY (Staff_ID, phone_no),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);

CREATE TABLE Library_Events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(100),
    location VARCHAR(100),
    date DATE,
    description TEXT
);

CREATE TABLE Book_Request (
    Request_ID INT PRIMARY KEY AUTO_INCREMENT,
    request_date DATE
);

CREATE TABLE Transactions (
    Transactions_ID INT PRIMARY KEY AUTO_INCREMENT,
    Transactions_Date DATE,
    Due_date DATE,
    Transaction_type VARCHAR(20),
    MemberID INT,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

CREATE TABLE Fines (
    FineID INT AUTO_INCREMENT PRIMARY KEY,
    OverDue_Days INT,
    fine_total DECIMAL(10,2),
    Paid_Status VARCHAR(20) DEFAULT 'Unpaid',
    payment_date DATE,
    Transactions_ID INT,
    FOREIGN KEY (Transactions_ID) REFERENCES Transactions(Transactions_ID)
);

CREATE TABLE Member_Phone (
    MemberID INT NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    PRIMARY KEY (MemberID, phone_no),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

CREATE TABLE Event_Member (
    MemberID INT NOT NULL,
    event_id INT NOT NULL,
    PRIMARY KEY (MemberID, event_id),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (event_id) REFERENCES Library_Events(event_id)
);

CREATE TABLE Event_Staff (
    event_id INT NOT NULL,
    Staff_ID INT NOT NULL,
    PRIMARY KEY (event_id, Staff_ID),
    FOREIGN KEY (event_id) REFERENCES Library_Events(event_id),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);

CREATE TABLE Transaction_Staff (
    Transaction_ID INT NOT NULL,
    Staff_ID INT NOT NULL,
    PRIMARY KEY (Transaction_ID, Staff_ID),
    FOREIGN KEY (Transaction_ID) REFERENCES Transactions(Transactions_ID),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);

CREATE TABLE Transaction_Book (
    Transaction_ID INT NOT NULL,
    Books_ID INT NOT NULL,
    PRIMARY KEY (Transaction_ID, Books_ID),
    FOREIGN KEY (Transaction_ID) REFERENCES Transactions(Transactions_ID),
    FOREIGN KEY (Books_ID) REFERENCES Books(Books_ID)
);

CREATE TABLE Transaction_Book_Request (
    Transaction_ID INT NOT NULL,
    Request_ID INT NOT NULL,
    PRIMARY KEY (Transaction_ID, Request_ID),
    FOREIGN KEY (Transaction_ID) REFERENCES Transactions(Transactions_ID),
    FOREIGN KEY (Request_ID) REFERENCES Book_Request(Request_ID)
);

CREATE TABLE Author_Book (
    Author_ID INT NOT NULL,
    Books_ID INT NOT NULL,
    PRIMARY KEY (Author_ID, Books_ID),
    FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID),
    FOREIGN KEY (Books_ID) REFERENCES Books(Books_ID)
);

CREATE TABLE Publisher_Book (
    Publisher_ID INT NOT NULL,
    Books_ID INT NOT NULL,
    PRIMARY KEY (Publisher_ID, Books_ID),
    FOREIGN KEY (Publisher_ID) REFERENCES Publisher(Publisher_ID),
    FOREIGN KEY (Books_ID) REFERENCES Books(Books_ID)
);

-- =============================================
-- INDEXES
-- =============================================
CREATE INDEX idx_transactions_date ON Transactions(Transactions_Date);
CREATE INDEX idx_transactions_member ON Transactions(MemberID);
CREATE INDEX idx_fines_transaction ON Fines(Transactions_ID);
CREATE INDEX idx_books_title ON Books(Title);
CREATE INDEX idx_books_category ON Books(book_category);

-- =============================================
-- FUNCTIONS FOR FINE CALCULATION
-- =============================================
DELIMITER $$

CREATE FUNCTION CalculateOverdueDays(due_date DATE, return_date DATE)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE overdue_days INT;
    SET overdue_days = DATEDIFF(COALESCE(return_date, CURDATE()), due_date);
    RETURN GREATEST(overdue_days, 0);
END$$

CREATE FUNCTION CalculateFine(due_date DATE, return_date DATE)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE days INT;
    DECLARE fine_rate DECIMAL(10,2) DEFAULT 1.50;
    SET days = CalculateOverdueDays(due_date, return_date);
    RETURN days * fine_rate;
END$$

DELIMITER ;

-- =============================================
-- INSERT SAMPLE DATA
-- =============================================
INSERT INTO Members (MemberDetails, RegistrationDate, Loan_History) VALUES 
    ('John Doe, john@example.com', '2024-01-10', 'Active member since 2024'),
    ('Jane Smith, jane@example.com', '2024-03-22', 'Regular borrower'),
    ('Bob Johnson, bob@example.com', '2024-02-15', 'New member');

INSERT INTO Books (Books_ID, Title, Publish_date, description, book_category, Price, ISBN, AvailabilityStatus) VALUES 
    (1, 'The Great Gatsby', '1925-04-10', 'Classic novel by F. Scott Fitzgerald', 'Fiction', 12.99, '9780743273565', 'Available'),
    (2, 'A Brief History of Time', '1988-06-01', 'Science book by Stephen Hawking', 'Science', 15.50, '9780553380163', 'Available'),
    (3, 'To Kill a Mockingbird', '1960-07-11', 'Classic American literature', 'Fiction', 13.99, '9780061120084', 'Available'),
    (4, '1984', '1949-06-08', 'Dystopian social science fiction novel', 'Fiction', 14.99, '9780451524935', 'Available');

INSERT INTO Author (Author_ID, Author_name, Email, phone_no) VALUES 
    (1, 'F. Scott Fitzgerald', 'fscott@example.com', '123-456-7890'),
    (2, 'Stephen Hawking', 'hawking@example.com', '987-654-3210'),
    (3, 'Harper Lee', 'hlee@example.com', '555-123-4567'),
    (4, 'George Orwell', 'gorwell@example.com', '444-987-6543');

INSERT INTO Publisher (Publisher_ID, Pub_Name, language) VALUES 
    (1, 'Scribner', 'English'),
    (2, 'Bantam Books', 'English'),
    (3, 'J.B. Lippincott & Co.', 'English'),
    (4, 'Secker & Warburg', 'English');

INSERT INTO Staff (Staff_ID, Email, address, phone_no) VALUES 
    (1, 'librarian1@library.com', '123 Library St', '111-222-3333'),
    (2, 'assistant@library.com', '456 Book Rd', '222-333-4444'),
    (3, 'manager@library.com', '789 Admin Ave', '333-444-5555');

INSERT INTO Staff_Phone (Staff_ID, phone_no) VALUES
    (1, '111-222-3333'),
    (2, '222-333-4444'),
    (3, '333-444-5555');

INSERT INTO Library_Events (event_id, event_name, location, date, description) VALUES 
    (1, 'Book Reading Session', 'Main Hall', '2025-06-15', 'Reading of classic literature'),
    (2, 'Science Talk', 'Auditorium', '2025-07-10', 'Talk on cosmology and physics'),
    (3, 'Author Meet & Greet', 'Conference Room', '2025-08-05', 'Meet local authors');

INSERT INTO Book_Request (Request_ID, request_date) VALUES 
    (1, '2025-05-10'),
    (2, '2025-05-11'),
    (3, '2025-05-12');

INSERT INTO Transactions (Transactions_ID, Transactions_Date, Due_date, Transaction_type, MemberID) VALUES 
    (1, '2025-05-01', '2025-05-15', 'Borrow', 1),
    (2, '2025-05-01', '2025-05-10', 'Borrow', 2),
    (3, '2025-05-20', '2025-06-03', 'Borrow', 1),
    (4, '2025-05-25', '2025-06-05', 'Return', 3),
    (5, '2025-05-10', '2025-05-15', 'Borrow', 2);

INSERT INTO Fines (OverDue_Days, fine_total, Paid_Status, payment_date, Transactions_ID) VALUES
    (DATEDIFF(CURDATE(), '2025-05-15'), DATEDIFF(CURDATE(), '2025-05-15') * 1.50, 'Unpaid', NULL, 1),
    (DATEDIFF(CURDATE(), '2025-05-10'), DATEDIFF(CURDATE(), '2025-05-10') * 1.50, 'Unpaid', NULL, 2),
    (0, 0.00, 'Paid', '2025-05-20', 3),
    (0, 0.00, 'Unpaid', NULL, 4),
    (DATEDIFF(CURDATE(), '2025-05-15'), DATEDIFF(CURDATE(), '2025-05-15') * 1.50, 'Unpaid', NULL, 5);

INSERT INTO Member_Phone (MemberID, phone_no) VALUES
    (1, '555-000-1111'),
    (2, '555-000-2222'),
    (3, '555-000-3333');

INSERT INTO Event_Member (MemberID, event_id) VALUES
    (1, 1),
    (2, 1),
    (2, 2),
    (3, 3);

INSERT INTO Event_Staff (event_id, Staff_ID) VALUES
    (1, 1),
    (2, 2),
    (3, 3);

INSERT INTO Transaction_Staff (Transaction_ID, Staff_ID) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (5, 2);

INSERT INTO Transaction_Book (Transaction_ID, Books_ID) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (5, 2);

INSERT INTO Transaction_Book_Request (Transaction_ID, Request_ID) VALUES
    (1, 1),
    (2, 2),
    (3, 3);

INSERT INTO Author_Book (Author_ID, Books_ID) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4);

INSERT INTO Publisher_Book (Publisher_ID, Books_ID) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4);
    
    
ALTER TABLE Books DROP COLUMN Publish_date;

ALTER TABLE Books ADD COLUMN Publisher_ID INT;

ALTER TABLE Books
ADD CONSTRAINT fk_publisher
FOREIGN KEY (Publisher_ID) REFERENCES Publisher(Publisher_ID);

-- Step 1: Add Publish_date to Publisher table
ALTER TABLE Publisher ADD COLUMN Publish_date DATE;

-- Step 2: Update Publish_date in Publisher with WHERE clause to avoid safe update error
UPDATE Publisher
SET Publish_date = CASE Publisher_ID
    WHEN 1 THEN '1925-04-10'  -- Scribner for The Great Gatsby
    WHEN 2 THEN '1988-06-01'  -- Bantam Books for A Brief History of Time
    WHEN 3 THEN '1960-07-11'  -- J.B. Lippincott & Co. for To Kill a Mockingbird
    WHEN 4 THEN '1949-06-08'  -- Secker & Warburg for 1984
END
WHERE Publisher_ID IN (1, 2, 3, 4);


-- Step 6: Update each book with its corresponding Publisher_ID
-- UPDATE Books SET Publisher_ID = 1 WHERE Books_ID = 1; -- Scribner
-- UPDATE Books SET Publisher_ID = 2 WHERE Books_ID = 2; -- Bantam Books
-- UPDATE Books SET Publisher_ID = 3 WHERE Books_ID = 3; -- J.B. Lippincott & Co.
-- UPDATE Books SET Publisher_ID = 4 WHERE Books_ID = 4; -- Secker & Warburg



-- =============================================
-- VERIFICATION QUERIES
-- =============================================
SHOW TABLES;

-- =============================================
-- ANALYTICAL QUERIES
-- =============================================
-- Query 1: Complete Transaction Overview
SELECT 
    t.Transactions_ID,
    t.Transactions_Date,
    t.Due_date,
    t.Transaction_type,
    m.MemberDetails,
    GROUP_CONCAT(DISTINCT b.Title SEPARATOR ', ') AS Books,
    GROUP_CONCAT(DISTINCT s.Staff_ID SEPARATOR ', ') AS StaffIDs,
    CalculateOverdueDays(t.Due_date, CURDATE()) AS Overdue_Days,
    CalculateFine(t.Due_date, CURDATE()) AS Calculated_Fine,
    MAX(f.Paid_Status) AS Paid_Status
FROM Transactions t
JOIN Members m ON t.MemberID = m.MemberID
LEFT JOIN Transaction_Book tb ON t.Transactions_ID = tb.Transaction_ID
LEFT JOIN Books b ON tb.Books_ID = b.Books_ID
LEFT JOIN Transaction_Staff ts ON t.Transactions_ID = ts.Transaction_ID
LEFT JOIN Staff s ON ts.Staff_ID = s.Staff_ID
LEFT JOIN Fines f ON t.Transactions_ID = f.Transactions_ID
GROUP BY t.Transactions_ID;

-- Query 2: Members with Above-Average Fines
SELECT 
    m.MemberDetails AS Member,
    COUNT(f.FineID) AS Number_of_Fines,
    COALESCE(SUM(f.fine_total), 0.00) AS Total_Fines
FROM Members m
LEFT JOIN Transactions t ON m.MemberID = t.MemberID
LEFT JOIN Fines f ON t.Transactions_ID = f.Transactions_ID
GROUP BY m.MemberID, m.MemberDetails
HAVING Total_Fines > (
    SELECT COALESCE(AVG(f2.fine_total), 0)
    FROM Fines f2
    WHERE f2.fine_total IS NOT NULL
)
ORDER BY Total_Fines DESC;



-- Query 3: Staff Performance
SELECT 
    s.Email AS Staff_Email,
    COUNT(DISTINCT es.event_id) AS Events_Managed,
    COUNT(DISTINCT ts.Transaction_ID) AS Transactions_Handled,
    GROUP_CONCAT(DISTINCT e.event_name SEPARATOR ', ') AS Events
FROM Staff s
LEFT JOIN Event_Staff es ON s.Staff_ID = es.Staff_ID
LEFT JOIN Library_Events e ON es.event_id = e.event_id
LEFT JOIN Transaction_Staff ts ON s.Staff_ID = ts.Staff_ID
GROUP BY s.Staff_ID, s.Email
ORDER BY Events_Managed DESC, Transactions_Handled DESC;


-- Query 4: Member Activity Analysis
SELECT 
    m.MemberID,
    m.MemberDetails,
    (
        SELECT COUNT(*)
        FROM Transactions t
        WHERE t.MemberID = m.MemberID
    ) AS Total_Transactions,
    (
        SELECT COUNT(*)
        FROM Event_Member em
        WHERE em.MemberID = m.MemberID
    ) AS Events_Attended,
    (
        SELECT COUNT(DISTINCT b.book_category)
        FROM Transactions t
        JOIN Transaction_Book tb ON t.Transactions_ID = tb.Transaction_ID
        JOIN Books b ON tb.Books_ID = b.Books_ID
        WHERE t.MemberID = m.MemberID
    ) AS Different_Categories_Borrowed,
    (
        SELECT COALESCE(SUM(f.fine_total), 0)
        FROM Transactions t
        LEFT JOIN Fines f ON t.Transactions_ID = f.Transactions_ID
        WHERE t.MemberID = m.MemberID
    ) AS Total_Fines
FROM Members m
HAVING Total_Transactions > 0
ORDER BY Total_Transactions DESC;

-- Query 5: Book Category Performance Analysis
WITH CategoryStats AS (
    SELECT 
        b.book_category,
        COUNT(DISTINCT tb.Transaction_ID) as borrow_count,
        COUNT(DISTINCT b.Books_ID) as total_books,
        AVG(b.Price) as avg_price
    FROM Books b
    LEFT JOIN Transaction_Book tb ON b.Books_ID = tb.Books_ID
    GROUP BY b.book_category
)
SELECT 
    cs.*,
    ROUND((cs.borrow_count / NULLIF(cs.total_books, 0)), 2) as utilization_ratio,
    RANK() OVER (ORDER BY cs.borrow_count DESC) as popularity_rank
FROM CategoryStats cs
ORDER BY utilization_ratio DESC;

-- query 6: books more famous
SELECT 
    b.Books_ID,
    b.Title,
    b.book_category,
    GROUP_CONCAT(DISTINCT a.Author_name) as Authors,
    COUNT(tb.Transaction_ID) as times_borrowed,
    FIRST_VALUE(b.Title) OVER (
        PARTITION BY b.book_category 
        ORDER BY COUNT(tb.Transaction_ID) DESC
    ) as most_popular_in_category,
    DENSE_RANK() OVER (
        ORDER BY COUNT(tb.Transaction_ID) DESC
    ) as popularity_rank,
    AVG(COUNT(tb.Transaction_ID)) OVER (
        PARTITION BY b.book_category
    ) as category_avg_borrows
FROM Books b
LEFT JOIN Transaction_Book tb ON b.Books_ID = tb.Books_ID
LEFT JOIN Author_Book ab ON b.Books_ID = ab.Books_ID
LEFT JOIN Author a ON ab.Author_ID = a.Author_ID
GROUP BY b.Books_ID, b.Title, b.book_category
ORDER BY times_borrowed DESC;



-- Query 7: Monthly Transaction Summary
SELECT 
    DATE_FORMAT(t.Transactions_Date, '%Y-%m') as month,
    COUNT(*) as total_transactions,
    COUNT(DISTINCT t.MemberID) as unique_members,
    COUNT(DISTINCT tb.Books_ID) as unique_books,
    SUM(COUNT(*)) OVER (
        ORDER BY DATE_FORMAT(t.Transactions_Date, '%Y-%m')
    ) as running_total_transactions,
    AVG(COUNT(*)) OVER (
        ORDER BY DATE_FORMAT(t.Transactions_Date, '%Y-%m')
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as three_month_moving_avg
FROM Transactions t
LEFT JOIN Transaction_Book tb ON t.Transactions_ID = tb.Transaction_ID
GROUP BY DATE_FORMAT(t.Transactions_Date, '%Y-%m')
ORDER BY month;

-- =============================================
-- SUMMARY STATISTICS
-- =============================================
SELECT 'Database Summary' AS Report;
SELECT COUNT(*) AS Total_Members FROM Members;
SELECT COUNT(*) AS Total_Books FROM Books;
SELECT COUNT(*) AS Total_Transactions FROM Transactions;
SELECT COUNT(*) AS Total_Active_Fines FROM Fines WHERE Paid_Status = 'Unpaid';

SET SQL_SAFE_UPDATES = 0;

UPDATE Fines
SET fine_total = OverDue_Days * 1.50
WHERE fine_total IS NULL AND Paid_Status = 'Unpaid';

SET SQL_SAFE_UPDATES = 1;

SELECT SUM(COALESCE(fine_total, 0.00)) AS Total_Outstanding_Fines
FROM Fines
WHERE Paid_Status = 'Unpaid';

-- =============================================
-- ENHANCED SUMMARY STATISTICS
-- =============================================
SELECT 'Enhanced Library Statistics Report' AS Report_Title;

SELECT 
    (SELECT COUNT(*) FROM Members) as Total_Members,
    (SELECT COUNT(*) FROM Books) as Total_Books,
    (SELECT COUNT(*) FROM Transactions) as Total_Transactions,
    (SELECT COUNT(DISTINCT book_category) FROM Books) as Total_Categories,
    (SELECT COUNT(*) FROM Library_Events) as Total_Events,
    (SELECT COUNT(*) FROM Staff) as Total_Staff;

SELECT 
    ROUND(SUM(CASE WHEN Paid_Status = 'Unpaid' THEN fine_total ELSE 0 END), 2) as Outstanding_Fines,
    ROUND(SUM(CASE WHEN Paid_Status = 'Paid' THEN fine_total ELSE 0 END), 2) as Collected_Fines,
    ROUND(AVG(fine_total), 2) as Average_Fine,
    COUNT(CASE WHEN Paid_Status = 'Unpaid' THEN 1 END) as Number_of_Unpaid_Fines
FROM Fines;

SELECT 
    book_category,
    COUNT(*) as Books_Count,
    ROUND(AVG(Price), 2) as Average_Price,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Books), 2) as Percentage_of_Collection
FROM Books
GROUP BY book_category
ORDER BY Books_Count DESC;

-- =============================================
-- ADDITIONAL VIEWS FROM LIBRARY SCHEMA
-- =============================================
CREATE OR REPLACE VIEW vw_book_statistics AS
SELECT 
    b.Books_ID,
    b.Title,
    b.book_category,
    COUNT(tb.Transaction_ID) as times_borrowed,
    b.AvailabilityStatus,
    GROUP_CONCAT(DISTINCT a.Author_name) as authors
FROM Books b
LEFT JOIN Transaction_Book tb ON b.Books_ID = tb.Books_ID
LEFT JOIN Transactions t ON tb.Transaction_ID = t.Transactions_ID
LEFT JOIN Author_Book ab ON b.Books_ID = ab.Books_ID
LEFT JOIN Author a ON ab.Author_ID = a.Author_ID
WHERE t.Transaction_type = 'Borrow' OR t.Transaction_type IS NULL
GROUP BY b.Books_ID, b.Title, b.book_category, b.AvailabilityStatus;

CREATE OR REPLACE VIEW vw_member_activity AS
SELECT 
    m.MemberID,
    m.MemberDetails,
    COUNT(DISTINCT t.Transactions_ID) as total_transactions,
    COUNT(DISTINCT f.FineID) as total_fines,
    COALESCE(SUM(f.fine_total), 0) as total_fine_amount,
    COUNT(DISTINCT em.event_id) as events_attended
FROM Members m
LEFT JOIN Transactions t ON m.MemberID = t.MemberID
LEFT JOIN Fines f ON t.Transactions_ID = f.Transactions_ID
LEFT JOIN Event_Member em ON m.MemberID = em.MemberID
GROUP BY m.MemberID, m.MemberDetails;

CREATE OR REPLACE VIEW vw_overdue_books AS
SELECT 
    t.Transactions_ID,
    b.Title,
    m.MemberDetails,
    t.Due_date,
    DATEDIFF(CURDATE(), t.Due_date) as days_overdue,
    f.fine_total
FROM Transactions t
JOIN Transaction_Book tb ON t.Transactions_ID = tb.Transaction_ID
JOIN Books b ON tb.Books_ID = b.Books_ID
JOIN Members m ON t.MemberID = m.MemberID
LEFT JOIN Fines f ON t.Transactions_ID = f.Transactions_ID
WHERE t.Due_date < CURDATE() 
AND t.Transaction_type = 'Borrow'
AND NOT EXISTS (
    SELECT 1 
    FROM Transaction_Book tb2 
    JOIN Transactions t2 ON tb2.Transaction_ID = t2.Transactions_ID
    WHERE tb2.Books_ID = b.Books_ID 
    AND t2.Transaction_type = 'Return'
    AND t2.Transactions_Date >= t.Transactions_Date
);

-- =============================================
-- ADDITIONAL FUNCTIONS FROM LIBRARY SCHEMA
-- =============================================
DELIMITER $$

CREATE FUNCTION get_member_history(p_member_id INT) 
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE result TEXT;
    SELECT GROUP_CONCAT(
        CONCAT(
            b.Title, ' (', 
            t.Transactions_Date, ' to ', 
            t.Due_date, ')'
        ) SEPARATOR '; '
    ) INTO result
    FROM Transactions t
    JOIN Transaction_Book tb ON t.Transactions_ID = tb.Transaction_ID
    JOIN Books b ON tb.Books_ID = b.Books_ID
    WHERE t.MemberID = p_member_id
    AND t.Transaction_type = 'Borrow';
    
    RETURN COALESCE(result, 'No borrowing history');
END$$

CREATE FUNCTION get_library_statistics() 
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE total_books INT;
    DECLARE total_members INT;
    DECLARE total_transactions INT;
    DECLARE result TEXT;

    SELECT COUNT(*) INTO total_books FROM Books;
    SELECT COUNT(*) INTO total_members FROM Members;
    SELECT COUNT(*) INTO total_transactions FROM Transactions;
    
    SET result = CONCAT(
        'Total Books: ', total_books,
        ', Total Members: ', total_members,
        ', Total Transactions: ', total_transactions
    );
    
    RETURN result;
END$$

-- Function to get audit history
DELIMITER $$

CREATE FUNCTION get_audit_history(entity_type VARCHAR(20), entity_id INT) 
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE result TEXT DEFAULT '';

    IF entity_type = 'Member' THEN
        SELECT GROUP_CONCAT(
            CONCAT(
                Action, ' on ', ChangeDate, '\n',
                CASE 
                    WHEN Action = 'UPDATE' THEN CONCAT('Old: ', OldDetails, '\nNew: ', NewDetails)
                    WHEN Action = 'INSERT' THEN CONCAT('New: ', NewDetails)
                    ELSE CONCAT('Deleted: ', OldDetails)
                END
            )
            ORDER BY ChangeDate DESC
            SEPARATOR '\n'
        ) INTO result
        FROM Members_Audit
        WHERE MemberID = entity_id;

    ELSEIF entity_type = 'Book' THEN
        SELECT GROUP_CONCAT(
            CONCAT(
                Action, ' on ', ChangeDate, '\n',
                CASE 
                    WHEN Action = 'UPDATE' THEN CONCAT('Old: ', OldDetails, '\nNew: ', NewDetails)
                    WHEN Action = 'INSERT' THEN CONCAT('New: ', NewDetails)
                    ELSE CONCAT('Deleted: ', OldDetails)
                END
            )
            ORDER BY ChangeDate DESC
            SEPARATOR '\n'
        ) INTO result
        FROM Books_Audit
        WHERE BookID = entity_id;

    ELSEIF entity_type = 'Staff' THEN
        SELECT GROUP_CONCAT(
            CONCAT(
                Action, ' on ', ChangeDate, '\n',
                CASE 
                    WHEN Action = 'UPDATE' THEN CONCAT('Old: ', OldDetails, '\nNew: ', NewDetails)
                    WHEN Action = 'INSERT' THEN CONCAT('New: ', NewDetails)
                    ELSE CONCAT('Deleted: ', OldDetails)
                END
            )
            ORDER BY ChangeDate DESC
            SEPARATOR '\n'
        ) INTO result
        FROM Staff_Audit
        WHERE StaffID = entity_id;
    END IF;

    RETURN COALESCE(result, 'No audit history found');
END$$

DELIMITER ;

-- =============================================
-- BASIC CRUD OPERATIONS FOR GUI
-- =============================================

-- Members CRUD
DELIMITER $$
CREATE PROCEDURE sp_insert_member(
    IN p_member_details VARCHAR(255),
    IN p_registration_date DATE,
    IN p_loan_history TEXT
)
BEGIN
    INSERT INTO Members (MemberDetails, RegistrationDate, Loan_History)
    VALUES (p_member_details, p_registration_date, p_loan_history);
    SELECT LAST_INSERT_ID() as MemberID;
END$$

DELIMITER $$
CREATE PROCEDURE sp_update_member(
    IN p_member_id INT,
    IN p_member_details VARCHAR(255),
    IN p_registration_date DATE,
    IN p_loan_history TEXT
)
BEGIN
    UPDATE Members 
    SET MemberDetails = p_member_details,
        RegistrationDate = p_registration_date,
        Loan_History = p_loan_history
    WHERE MemberID = p_member_id;
END$$


DELIMITER $$
CREATE PROCEDURE sp_delete_member(
    IN p_member_id INT
)
BEGIN
    -- Delete related fines
    DELETE FROM Fines 
    WHERE Transactions_ID IN (
        SELECT Transactions_ID 
        FROM Transactions 
        WHERE MemberID = p_member_id
    );

    -- Delete related transaction records
    DELETE FROM Transaction_Book_Request 
    WHERE Transaction_ID IN (
        SELECT Transactions_ID 
        FROM Transactions 
        WHERE MemberID = p_member_id
    );

    DELETE FROM Transaction_Book 
    WHERE Transaction_ID IN (
        SELECT Transactions_ID 
        FROM Transactions 
        WHERE MemberID = p_member_id
    );

    DELETE FROM Transaction_Staff 
    WHERE Transaction_ID IN (
        SELECT Transactions_ID 
        FROM Transactions 
        WHERE MemberID = p_member_id
    );

    -- Delete transactions
    DELETE FROM Transactions WHERE MemberID = p_member_id;
    
    -- Delete event participation
    DELETE FROM Event_Member WHERE MemberID = p_member_id;
    
    -- Delete phone numbers
    DELETE FROM Member_Phone WHERE MemberID = p_member_id;
    
    -- Finally delete the member
    DELETE FROM Members WHERE MemberID = p_member_id;
END$$

-- Books CRUD
DELIMITER $$
CREATE PROCEDURE sp_insert_book(
    IN p_title VARCHAR(255),
    IN p_isbn VARCHAR(13),
    IN p_category VARCHAR(50),
    IN p_status VARCHAR(20)
)
BEGIN
    INSERT INTO Books (Title, ISBN, book_category, AvailabilityStatus)
    VALUES (p_title, p_isbn, p_category, p_status);
    SELECT LAST_INSERT_ID() as Books_ID;
END$$

DELIMITER $$
CREATE PROCEDURE sp_update_book(
    IN p_book_id INT,
    IN p_title VARCHAR(255),
    IN p_isbn VARCHAR(13),
    IN p_category VARCHAR(50),
    IN p_status VARCHAR(20)
)
BEGIN
    UPDATE Books 
    SET Title = p_title,
        ISBN = p_isbn,
        book_category = p_category,
        AvailabilityStatus = p_status
    WHERE Books_ID = p_book_id;
END$$

DELIMITER $$
CREATE PROCEDURE sp_delete_book(
    IN p_book_id INT
)
BEGIN
    -- Delete related transaction records
    DELETE FROM Transaction_Book WHERE Books_ID = p_book_id;
    
    -- Delete author associations
    DELETE FROM Author_Book WHERE Books_ID = p_book_id;
    
    -- Delete publisher associations
    DELETE FROM Publisher_Book WHERE Books_ID = p_book_id;
    
    -- Finally delete the book
    DELETE FROM Books WHERE Books_ID = p_book_id;
END$$

-- Staff CRUD
DELIMITER $$
CREATE PROCEDURE sp_insert_staff(
    IN p_email VARCHAR(100),
    IN p_address VARCHAR(255),
    IN p_phone VARCHAR(20)
)
BEGIN
    INSERT INTO Staff (Email, address, phone_no)
    VALUES (p_email, p_address, p_phone);
    
    SET @new_staff_id = LAST_INSERT_ID();
    
    -- Add phone number to Staff_Phone
    INSERT INTO Staff_Phone (Staff_ID, phone_no)
    VALUES (@new_staff_id, p_phone);
    
    SELECT @new_staff_id as Staff_ID;
END$$

DELIMITER $$

CREATE PROCEDURE sp_update_staff(
    IN p_staff_id INT,
    IN p_email VARCHAR(100),
    IN p_address VARCHAR(255),
    IN p_phone VARCHAR(20)
)
BEGIN
    UPDATE Staff 
    SET Email = p_email,
        address = p_address,
        phone_no = p_phone
    WHERE Staff_ID = p_staff_id;
    
    -- Update phone in Staff_Phone
    UPDATE Staff_Phone 
    SET phone_no = p_phone
    WHERE Staff_ID = p_staff_id;
END$$

DELIMITER $$

CREATE PROCEDURE sp_delete_staff(
    IN p_staff_id INT
)
BEGIN
    -- Delete from Event_Staff
    DELETE FROM Event_Staff WHERE Staff_ID = p_staff_id;
    
    -- Delete from Transaction_Staff
    DELETE FROM Transaction_Staff WHERE Staff_ID = p_staff_id;
    
    -- Delete from Staff_Phone
    DELETE FROM Staff_Phone WHERE Staff_ID = p_staff_id;
    
    -- Finally delete the staff
    DELETE FROM Staff WHERE Staff_ID = p_staff_id;
END$$

-- Select Queries

DELIMITER $$
CREATE PROCEDURE sp_select_members(
    IN p_search_term VARCHAR(255)
)
BEGIN
    SELECT 
        m.*,
        GROUP_CONCAT(DISTINCT mp.phone_no) as phone_numbers,
        COUNT(DISTINCT t.Transactions_ID) as total_transactions,
        COUNT(DISTINCT em.event_id) as events_attended
    FROM Members m
    LEFT JOIN Member_Phone mp ON m.MemberID = mp.MemberID
    LEFT JOIN Transactions t ON m.MemberID = t.MemberID
    LEFT JOIN Event_Member em ON m.MemberID = em.MemberID
    WHERE m.MemberDetails LIKE CONCAT('%', p_search_term, '%')
    GROUP BY m.MemberID;
END$$

CREATE PROCEDURE sp_select_books(
    IN p_category VARCHAR(50)
)
BEGIN
    SELECT 
        b.*,
        GROUP_CONCAT(DISTINCT a.Author_name) as authors,
        COUNT(DISTINCT tb.Transaction_ID) as times_borrowed
    FROM Books b
    LEFT JOIN Author_Book ab ON b.Books_ID = ab.Books_ID
    LEFT JOIN Author a ON ab.Author_ID = a.Author_ID
    LEFT JOIN Transaction_Book tb ON b.Books_ID = tb.Books_ID
    WHERE (p_category IS NULL OR b.book_category = p_category)
    GROUP BY b.Books_ID;
END$$

CREATE PROCEDURE sp_select_staff(
    IN p_search_term VARCHAR(255)
)
BEGIN
    SELECT 
        s.*,
        COUNT(DISTINCT ts.Transaction_ID) as transactions_handled,
        COUNT(DISTINCT es.event_id) as events_managed
    FROM Staff s
    LEFT JOIN Transaction_Staff ts ON s.Staff_ID = ts.Staff_ID
    LEFT JOIN Event_Staff es ON s.Staff_ID = es.Staff_ID
    WHERE s.Email LIKE CONCAT('%', p_search_term, '%')
        OR s.address LIKE CONCAT('%', p_search_term, '%')
        OR s.phone_no LIKE CONCAT('%', p_search_term, '%')
    GROUP BY s.Staff_ID;
END$$

DELIMITER ;

-- Create audit tables to track changes
CREATE TABLE IF NOT EXISTS Members_Audit (
    AuditID INT PRIMARY KEY AUTO_INCREMENT,
    MemberID INT,
    Action VARCHAR(20),
    ChangeDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    OldDetails TEXT,
    NewDetails TEXT
);

CREATE TABLE IF NOT EXISTS Books_Audit (
    AuditID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
    Action VARCHAR(20),
    ChangeDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    OldDetails TEXT,
    NewDetails TEXT
);

CREATE TABLE IF NOT EXISTS Staff_Audit (
    AuditID INT PRIMARY KEY AUTO_INCREMENT,
    StaffID INT,
    Action VARCHAR(20),
    ChangeDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    OldDetails TEXT,
    NewDetails TEXT
);

DELIMITER $$

-- Members Triggers
CREATE TRIGGER members_after_insert 
AFTER INSERT ON Members
FOR EACH ROW
BEGIN
    INSERT INTO Members_Audit (MemberID, Action, NewDetails)
    VALUES (NEW.MemberID, 'INSERT', 
            CONCAT('Details: ', NEW.MemberDetails, 
                   ', RegDate: ', NEW.RegistrationDate,
                   ', History: ', COALESCE(NEW.Loan_History, 'None')));
END$$

CREATE TRIGGER members_after_update
AFTER UPDATE ON Members
FOR EACH ROW
BEGIN
    INSERT INTO Members_Audit (MemberID, Action, OldDetails, NewDetails)
    VALUES (NEW.MemberID, 'UPDATE',
            CONCAT('Details: ', OLD.MemberDetails, 
                   ', RegDate: ', OLD.RegistrationDate,
                   ', History: ', COALESCE(OLD.Loan_History, 'None')),
            CONCAT('Details: ', NEW.MemberDetails, 
                   ', RegDate: ', NEW.RegistrationDate,
                   ', History: ', COALESCE(NEW.Loan_History, 'None')));
END$$

CREATE TRIGGER members_after_delete
AFTER DELETE ON Members
FOR EACH ROW
BEGIN
    INSERT INTO Members_Audit (MemberID, Action, OldDetails)
    VALUES (OLD.MemberID, 'DELETE',
            CONCAT('Details: ', OLD.MemberDetails, 
                   ', RegDate: ', OLD.RegistrationDate,
                   ', History: ', COALESCE(OLD.Loan_History, 'None')));
END$$

-- Books Triggers
CREATE TRIGGER books_after_insert
AFTER INSERT ON Books
FOR EACH ROW
BEGIN
    INSERT INTO Books_Audit (BookID, Action, NewDetails)
    VALUES (NEW.Books_ID, 'INSERT',
            CONCAT('Title: ', NEW.Title,
                   ', ISBN: ', COALESCE(NEW.ISBN, 'None'),
                   ', Status: ', COALESCE(NEW.AvailabilityStatus, 'Unknown')));
END$$

CREATE TRIGGER books_after_update
AFTER UPDATE ON Books
FOR EACH ROW
BEGIN
    INSERT INTO Books_Audit (BookID, Action, OldDetails, NewDetails)
    VALUES (NEW.Books_ID, 'UPDATE',
            CONCAT('Title: ', OLD.Title,
                   ', ISBN: ', COALESCE(OLD.ISBN, 'None'),
                   ', Status: ', COALESCE(OLD.AvailabilityStatus, 'Unknown')),
            CONCAT('Title: ', NEW.Title,
                   ', ISBN: ', COALESCE(NEW.ISBN, 'None'),
                   ', Status: ', COALESCE(NEW.AvailabilityStatus, 'Unknown')));
END$$

CREATE TRIGGER books_after_delete
AFTER DELETE ON Books
FOR EACH ROW
BEGIN
    INSERT INTO Books_Audit (BookID, Action, OldDetails)
    VALUES (OLD.Books_ID, 'DELETE',
            CONCAT('Title: ', OLD.Title,
                   ', ISBN: ', COALESCE(OLD.ISBN, 'None'),
                   ', Status: ', COALESCE(OLD.AvailabilityStatus, 'Unknown')));
END$$

-- Staff Triggers
CREATE TRIGGER staff_after_insert
AFTER INSERT ON Staff
FOR EACH ROW
BEGIN
    INSERT INTO Staff_Audit (StaffID, Action, NewDetails)
    VALUES (NEW.Staff_ID, 'INSERT',
            CONCAT('Email: ', NEW.Email,
                   ', Address: ', COALESCE(NEW.address, 'None'),
                   ', Phone: ', COALESCE(NEW.phone_no, 'None')));
END$$

CREATE TRIGGER staff_after_update
AFTER UPDATE ON Staff
FOR EACH ROW
BEGIN
    INSERT INTO Staff_Audit (StaffID, Action, OldDetails, NewDetails)
    VALUES (NEW.Staff_ID, 'UPDATE',
            CONCAT('Email: ', OLD.Email,
                   ', Address: ', COALESCE(OLD.address, 'None'),
                   ', Phone: ', COALESCE(OLD.phone_no, 'None')),
            CONCAT('Email: ', NEW.Email,
                   ', Address: ', COALESCE(NEW.address, 'None'),
                   ', Phone: ', COALESCE(NEW.phone_no, 'None')));
END$$

CREATE TRIGGER staff_after_delete
AFTER DELETE ON Staff
FOR EACH ROW
BEGIN
    INSERT INTO Staff_Audit (StaffID, Action, OldDetails)
    VALUES (OLD.Staff_ID, 'DELETE',
            CONCAT('Email: ', OLD.Email,
                   ', Address: ', COALESCE(OLD.address, 'None'),
                   ', Phone: ', COALESCE(OLD.phone_no, 'None')));
END$$

DELIMITER ;

-- Create view for recent changes
CREATE OR REPLACE VIEW vw_recent_changes AS
SELECT 'Member' as EntityType, 
       MemberID as EntityID, 
       Action, 
       ChangeDate, 
       COALESCE(NewDetails, OldDetails) as Details
FROM Members_Audit
UNION ALL
SELECT 'Book', 
       BookID, 
       Action, 
       ChangeDate, 
       COALESCE(NewDetails, OldDetails)
FROM Books_Audit
UNION ALL
SELECT 'Staff', 
       StaffID, 
       Action, 
       ChangeDate, 
       COALESCE(NewDetails, OldDetails)
FROM Staff_Audit
ORDER BY ChangeDate DESC;

