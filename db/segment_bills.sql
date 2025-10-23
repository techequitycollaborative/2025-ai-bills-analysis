-- segment_bills.sql
-- Grab AI bills from 2025 for further analysis.

-- Create the schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS bill_analytics;

-- Create table
CREATE TABLE bill_analytics.ai_bills_2025 AS
SELECT * 
FROM public.bills_2025_2026
WHERE bill_number IN (
  'AB 682', 'SB 58', 'SB 813', 'SB 57', 'AB 316', 'SB 361', 'SB 384', 'SB 420', 
  'SB 11', 'AB 512', 'AB 489', 'SB 243', 'AB 446', 'AB 979', 'SB 468', 'SB 857', 
  'SB 53', 'AB 2', 'SB 238', 'AB 302', 'AB 222', 'AB 566', 'SB 295', 'AB 33', 
  'AB 1018', 'SB 47', 'AB 1221', 'AB 970', 'AB 1337', 'AB 1064', 'SB 503', 'AB 325', 
  'AB 1053', 'AB 502', 'SB 274', 'SB 241', 'SB 7', 'AB 621', 'AB 887', 'AB 1137', 
  'AB 93', 'AB 1159', 'SB 690', 'SB 52', 'SB 833', 'AB 1331', 'AB 1355', 'AB 279', 
  'SB 435', 'SB 524', 'AB 1405', 'AB 1242', 'SB 579', 'AB 322', 'SB 366', 'AB 1043', 
  'AB 392', 'AB 853', 'AB 723', 'AB 56', 'AB 412', 'SB 259', 'AB 410', 'SB 253', 
  'SB 620', 'SB 69', 'AB 1095', 'SB 44', 'AB 45', 'SB 763', 'SB 354'
);
