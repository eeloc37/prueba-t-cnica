CREATE TABLE Cargo (
    id VARCHAR(24) NOT NULL PRIMARY KEY,
    company_name VARCHAR(130) NULL,
    company_id VARCHAR(24) NOT NULL,
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at DATETIME,
    paid_at DATETIME NULL
);