CREATE TABLE companies (
    company_id VARCHAR(24) NOT NULL PRIMARY KEY,
    company_name VARCHAR(130) NOT NULL
);

CREATE TABLE charges (
    id VARCHAR(24) NOT NULL PRIMARY KEY,
    company_id VARCHAR(24) NOT NULL,
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at DATETIME,
    paid_at DATETIME NULL,
    CONSTRAINT fk_charges_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);