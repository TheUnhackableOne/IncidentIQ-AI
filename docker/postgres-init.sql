-- Create IncidentIQ database
CREATE DATABASE incidentiq;

-- Connect to incidentiq database
\c incidentiq;

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create tables (will be managed by Alembic migrations)
-- This is a placeholder for initial setup
