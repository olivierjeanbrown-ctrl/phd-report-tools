-- only select variables of interest for interaction LMM model
SELECT record_id, cdrisc_72, cdrisc_4w, sex, calc_age, randomization FROM MBI4mTBIoutput
-- only include those that completed BOTH MRIs
where mri_comp = 1 AND mri_comp_2 = 1
-- only include those that adhered to the protocol (spent 9600 in app activities)
	AND session_duration_sum > 9600 
-- only include those with existing values for relevant variables (cdrisc)
	AND cdrisc_72 IS NOT NULL 
	AND cdrisc_4w IS NOT NULL
-- sort by randomization, specifically grouping MBIs first then Shams
ORDER BY randomization ASC;