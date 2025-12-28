-- CareConnect Reporting Queries 

USE careconnect;

-- query 1 (basic filter and comparison)
-- This query allows staff to view all upcoming appointments for the next 7 days.
-- This allows staff to plan accordingly.
SELECT
  a.appointment_id,
  a.start_datetime,
  a.end_datetime,
  a.status,
  a.reason,
  p.first_name AS patient_first,
  p.last_name  AS patient_last,
  mp.first_name AS provider_first,
  mp.last_name  AS provider_last,
  c.clinic_name
FROM appointment a
JOIN patient p ON p.patient_id = a.patient_id
JOIN medical_provider mp ON mp.provider_id = a.provider_id
JOIN clinic c ON c.clinic_id = a.clinic_id
WHERE a.start_datetime >= NOW()
  AND a.start_datetime < DATE_ADD(NOW(), INTERVAL 7 DAY)
ORDER BY a.start_datetime;

-- query 2 (basic filter and comparison)
-- This query allows staff to see all appointment of status "No-show" in the last 30 days.
-- This allows hospital management to understand the rate at which patients default on their appointments and can update the central government on if a PR campaign may be necessary.
SELECT
  a.appointment_id,
  a.start_datetime,
  p.first_name, p.last_name,
  mp.first_name AS provider_first, mp.last_name AS provider_last,
  c.clinic_name
FROM appointment a
JOIN patient p ON p.patient_id = a.patient_id
JOIN medical_provider mp ON mp.provider_id = a.provider_id
JOIN clinic c ON c.clinic_id = a.clinic_id
WHERE a.status = 'no_show'
  AND a.start_datetime >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY a.start_datetime DESC;

-- query 3 (inner join)
-- This query allows staff to pull a report on medical roviders along with their respective specialties, this allows the them to more easily direct patients.
SELECT
  mp.provider_id,
  mp.first_name,
  mp.last_name,
  s.specialty_name
FROM medical_provider mp
JOIN provider_specialty ps ON ps.provider_id = mp.provider_id
JOIN specialty s ON s.specialty_id = ps.specialty_id
ORDER BY mp.last_name, mp.first_name, s.specialty_name;

-- query 4 (left join)
-- This query allows staff to pull a report of all medical providers and their respective appointment counts. This allows the clinic to see each doctors workload and then allocate work appropiately,
SELECT
  mp.provider_id,
  mp.first_name,
  mp.last_name,
  COUNT(a.appointment_id) AS total_appointments
FROM medical_provider mp
LEFT JOIN appointment a ON a.provider_id = mp.provider_id
GROUP BY mp.provider_id, mp.first_name, mp.last_name
ORDER BY total_appointments DESC, mp.last_name, mp.first_name;

-- query 5 (group by and aggregation)
-- This query allows staff to pull a report of the no show rate of patients by a each medical provider.
-- This allows hospital management to know which doctors experience high no show rates and as such can launch programs to ensure these no show patients get the care that they need.
SELECT
  mp.provider_id,
  mp.first_name,
  mp.last_name,
  COUNT(*) AS total_appts,
  SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) AS no_shows,
  ROUND(100 * SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) / COUNT(*), 2) AS no_show_rate_pct
FROM appointment a
JOIN medical_provider mp ON mp.provider_id = a.provider_id
WHERE a.start_datetime >= DATE_SUB(NOW(), INTERVAL 60 DAY)
GROUP BY mp.provider_id, mp.first_name, mp.last_name
HAVING COUNT(*) >= 10
ORDER BY no_show_rate_pct DESC, total_appts DESC;

-- query 5 (group by and aggregation)
-- This report allows staff to see how many appoints are set at each clinic per day for the last 14 days. 
-- This is critical to understand which clinics have the most demand and as such the central body may be able to route more doctors to that area.
SELECT
  c.clinic_name,
  DATE(a.start_datetime) AS appt_date,
  COUNT(*) AS total_appointments
FROM appointment a
JOIN clinic c ON c.clinic_id = a.clinic_id
WHERE a.start_datetime >= DATE_SUB(NOW(), INTERVAL 14 DAY)
GROUP BY c.clinic_name, DATE(a.start_datetime)
ORDER BY appt_date DESC, total_appointments DESC;

-- query 7 (sorting and ordering and limit)
-- This query pull the top 10 most common appointment reasons in the last 90 days 
-- This report allows staff to find trends and as such plan accordingly for the future.
SELECT
  a.reason,
  COUNT(*) AS reason_count
FROM appointment a
WHERE a.start_datetime >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY a.reason
ORDER BY reason_count DESC
LIMIT 10;

-- query 8 (sorting and ordering and limit)
-- This query allows staff to pull the top 10 provider with the most appointments during this months 
-- This query allows management to see workload distrubution and then allocate work fairly. This also allows management to predict if a doctor may become or is already overworked.
SELECT
  mp.provider_id,
  mp.first_name,
  mp.last_name,
  COUNT(a.appointment_id) AS appt_count
FROM medical_provider mp
JOIN appointment a ON a.provider_id = mp.provider_id
WHERE a.start_datetime >= DATE_FORMAT(NOW(), '%Y-%m-01')
  AND a.start_datetime <  DATE_ADD(DATE_FORMAT(NOW(), '%Y-%m-01'), INTERVAL 1 MONTH)
GROUP BY mp.provider_id, mp.first_name, mp.last_name
ORDER BY appt_count DESC
LIMIT 10;

-- query 9 (multi-table using join and group by and subquery)
-- This query allows staff to see the no show rate of patients by specialties.
-- A high no show rate in a particular specialty may indicate that something is wrong with the processes in that particular department and that management may need to look into what improvements could be made.
SELECT
  s.specialty_name,
  totals.total_appts,
  totals.no_shows,
  ROUND(100 * totals.no_shows / totals.total_appts, 2) AS no_show_rate_pct
FROM specialty s
JOIN (
  SELECT
    ps.specialty_id,
    COUNT(*) AS total_appts,
    SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) AS no_shows
  FROM appointment a
  JOIN provider_specialty ps ON ps.provider_id = a.provider_id
  WHERE a.start_datetime >= DATE_SUB(NOW(), INTERVAL 90 DAY)
  GROUP BY ps.specialty_id
) AS totals
  ON totals.specialty_id = s.specialty_id
WHERE totals.total_appts >= 20
ORDER BY no_show_rate_pct DESC, totals.total_appts DESC;

-- query 10 (joins and groub by)
-- This query pull all medical providers who have an expired license by have appointments scheduled in the future.
-- This is critical for legal reasons as it would be catastophic if a doctor with an expired license is attending to patients.
SELECT
  mp.provider_id,
  mp.first_name,
  mp.last_name,
  ml.issue_date,
  ml.expiry_date,
  COUNT(a.appointment_id) AS future_scheduled_appts
FROM medical_provider mp
JOIN medical_license ml ON ml.provider_id = mp.provider_id
JOIN appointment a ON a.provider_id = mp.provider_id
WHERE ml.status = 'expired'
  AND a.status = 'scheduled'
  AND a.start_datetime > NOW()
GROUP BY mp.provider_id, mp.first_name, mp.last_name, ml.issue_date, ml.expiry_date
ORDER BY future_scheduled_appts DESC;
