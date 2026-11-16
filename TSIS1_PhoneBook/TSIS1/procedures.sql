CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id FROM contacts
    WHERE first_name = p_contact_name ORDER BY id LIMIT 1;
    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;
    IF p_type NOT IN ('home', 'work', 'mobile') OR p_type IS NULL THEN
        RAISE EXCEPTION 'Phone type must be home, work or mobile';
    END IF;
    IF p_phone IS NULL OR p_phone !~ '^\+?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'Invalid phone number';
    END IF;
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR, p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
    v_group_id INTEGER;
BEGIN
    SELECT id INTO v_id FROM contacts
    WHERE first_name = p_contact_name ORDER BY id LIMIT 1;
    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;
    IF p_group_name IS NULL OR TRIM(p_group_name) = '' THEN
        RAISE EXCEPTION 'Group name cannot be empty';
    END IF;
    INSERT INTO groups (name) VALUES (TRIM(p_group_name))
    ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = TRIM(p_group_name);
    UPDATE contacts SET group_id = v_group_id WHERE id = v_id;
END;
$$;

DROP FUNCTION IF EXISTS search_contacts(TEXT);
CREATE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INTEGER, first_name VARCHAR, surname VARCHAR, phone VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.surname,
           COALESCE((SELECT string_agg(p.phone, ', ' ORDER BY p.id)
                     FROM phones p WHERE p.contact_id = c.id), c.phone, '')::VARCHAR
    FROM contacts c
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.surname ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR EXISTS (
           SELECT 1 FROM phones p
           WHERE p.contact_id = c.id AND p.phone ILIKE '%' || p_query || '%'
       )
       OR c.phone ILIKE '%' || p_query || '%'
    ORDER BY c.id;
END;
$$;
