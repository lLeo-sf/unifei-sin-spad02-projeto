CREATE OR REPLACE VIEW organization_basic_info_view AS
SELECT
  name,
  url,
  citystate,
  type,
  phone,
  services
FROM
  organizations;
