CREATE OR REPLACE FUNCTION prevent_reopening_closed_cases()
RETURNS TRIGGER AS $$
BEGIN
  -- Se o novo status for "Available"
  IF NEW.statusid = 1 THEN
    -- Verifica se o status atual é um dos finais
    IF OLD.statusid IN (3, 5, 7, 19) THEN
      RAISE EXCEPTION 'Cannot change status from % to Available. This status is considered final.', OLD.statusid;
    END IF;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


----------------------------------------------
CREATE TRIGGER trg_prevent_invalid_status_change
BEFORE UPDATE ON animals
FOR EACH ROW
WHEN (OLD.statusid IS DISTINCT FROM NEW.statusid)
EXECUTE FUNCTION prevent_reopening_closed_cases();


------------------------------------------------------

