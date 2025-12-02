-- hardcode remove those that failed MRI QC checks
DELETE FROM MBI4mTBI_EM_winsorized
WHERE record_id = 179 or record_id = 228 or record_id = 239;

-- this selects from the imputed (EM) and winsorized (no outlier) data
-- this is also from the adherence report, so app usage was aggregated into this set

SELECT *
FROM MBI4mTBI_EM_winsorized
-- all we have to do is add a clause to exclude those that did not adhere (9599 app seconds)
WHERE session_duration_sum > 9599
-- ordering by randomization so that MBI and control groups are separate in the output
ORDER BY randomization ASC;

