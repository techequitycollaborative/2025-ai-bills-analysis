-- floor_votes.sql
-- Grab floor vote data for 2025 bills, with added columns for number of votes needed and vote margin

-- Store the table in the bill_analytics schema
DROP TABLE IF EXISTS bill_analytics.floor_votes_2025;

-- Calculate total_votes first in a CTE
CREATE TABLE bill_analytics.floor_votes_2025 AS
WITH vote_totals AS (
    SELECT 
        openstates_bill_id,
        motion_text,
        vote_date,
        vote_location,
        vote_result,
        vote_threshold,
        yes_count,
        no_count,
        other_count,
        CAST(yes_count AS INTEGER) + CAST(no_count AS INTEGER) + CAST(other_count AS INTEGER) AS total_votes
    FROM snapshot.bill_vote
),
-- Then calculate number of votes needed based on threshold
vote_threshold_calc AS (
    SELECT 
        openstates_bill_id,
        motion_text,
        vote_date,
        vote_location,
        vote_result,
        vote_threshold,
        yes_count,
        no_count,
        other_count,
        total_votes,
        -- Create a column for vote_threshold_num, which shows the number of votes needed based on the assembly/senate thresholds
        CASE 
            WHEN vote_threshold = '1/2' AND vote_location = 'Assembly' THEN 41
			WHEN vote_threshold = '2/3' AND vote_location = 'Assembly' THEN 54
			WHEN vote_threshold = '1/2' AND vote_location = 'Senate' THEN 21
            WHEN vote_threshold = '2/3' AND vote_location = 'Senate' THEN 27
           	ELSE NULL
        END AS vote_threshold_num    
    FROM vote_totals
)
-- Then create final table with vote margin and filter by 2025-2026 bills only
SELECT 
    vtc.openstates_bill_id,
    vtc.motion_text,
    vtc.vote_date,
    vtc.vote_location,
    vtc.vote_result,
    vtc.vote_threshold,
    vtc.yes_count,
    vtc.no_count,
    vtc.other_count,
    vtc.total_votes,
    vtc.vote_threshold_num,
    -- Create vote_margin column that is the yes votes minus the vote_threshold_num
    CAST(vtc.yes_count AS INTEGER) - vtc.vote_threshold_num AS vote_margin,
    b.leg_session
FROM vote_threshold_calc vtc
INNER JOIN bills_2025_2026 b 
    ON vtc.openstates_bill_id = b.openstates_bill_id
WHERE b.leg_session IS NOT NULL;