CREATE OR REPLACE VIEW animal_available_view AS
SELECT
  a.name AS animal_name,
  a.sex,
  o.name AS organization_name,
  o.city,
  o.state,
  o.email AS organization_email,
  o.phone,
  st.name AS status_animal
FROM
  Animals a
JOIN
  Organizations o ON a.organizationid = o.id
JOIN 
  statuses st ON a.statusid = st.id
WHERE
  st.name LIKE 'Available'
