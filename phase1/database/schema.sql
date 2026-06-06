CREATE TABLE IF NOT EXISTS banks (
    id SERIAL PRIMARY KEY,
    bank_name VARCHAR(160) NOT NULL UNIQUE,
    bank_type VARCHAR(80) NOT NULL,
    upi_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS outages (
    id SERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL REFERENCES banks(id) ON DELETE CASCADE,
    outage_type VARCHAR(80) NOT NULL,
    planned BOOLEAN NOT NULL DEFAULT FALSE,
    severity VARCHAR(40) NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes >= 0),
    source VARCHAR(240) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_outages_time_window CHECK (end_time >= start_time)
);

CREATE TABLE IF NOT EXISTS maintenance_notices (
    id SERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL REFERENCES banks(id) ON DELETE CASCADE,
    title VARCHAR(180) NOT NULL,
    description TEXT NOT NULL,
    maintenance_start TIMESTAMPTZ NOT NULL,
    maintenance_end TIMESTAMPTZ NOT NULL,
    source VARCHAR(240) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_maintenance_time_window CHECK (maintenance_end >= maintenance_start)
);

CREATE TABLE IF NOT EXISTS npci_statistics (
    id SERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL REFERENCES banks(id) ON DELETE CASCADE,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL CHECK (year BETWEEN 2000 AND 2100),
    success_rate NUMERIC(5, 2) NOT NULL CHECK (success_rate BETWEEN 0 AND 100),
    technical_decline NUMERIC(5, 2) NOT NULL CHECK (technical_decline BETWEEN 0 AND 100),
    business_decline NUMERIC(5, 2) NOT NULL CHECK (business_decline BETWEEN 0 AND 100),
    source VARCHAR(240) NOT NULL DEFAULT 'manual',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_npci_statistics_bank_month_year UNIQUE (bank_id, month, year)
);

CREATE INDEX IF NOT EXISTS ix_outages_bank_id ON outages(bank_id);
CREATE INDEX IF NOT EXISTS ix_outages_start_time ON outages(start_time);
CREATE INDEX IF NOT EXISTS ix_outages_planned ON outages(planned);
CREATE INDEX IF NOT EXISTS ix_maintenance_notices_bank_id ON maintenance_notices(bank_id);
CREATE INDEX IF NOT EXISTS ix_maintenance_notices_start ON maintenance_notices(maintenance_start);
CREATE INDEX IF NOT EXISTS ix_npci_statistics_bank_id ON npci_statistics(bank_id);
CREATE INDEX IF NOT EXISTS ix_npci_statistics_period ON npci_statistics(year, month);
