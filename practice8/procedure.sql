CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
BEGIN
    IF p_name IS NULL OR TRIM(p_name) = '' THEN
        RAISE EXCEPTION 'Name cannot be empty';
    END IF;

    IF p_phone IS NULL
       OR p_phone !~ '^\+?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'Invalid phone number';
    END IF;

    SELECT c.id INTO v_id
    FROM contacts c
    WHERE c.first_name = TRIM(p_name)
    ORDER BY c.id
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE id = v_id;
    ELSE
        INSERT INTO contacts(first_name, phone)
        VALUES (TRIM(p_name), p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    IN p_names TEXT[],
    IN p_phones TEXT[],
    INOUT p_invalid TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
BEGIN
    p_invalid := ARRAY[]::TEXT[];

    IF array_length(p_names, 1)
       IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Array lengths must match';
    END IF;

    FOR i IN 1..COALESCE(array_length(p_names, 1), 0) LOOP

        IF p_names[i] IS NULL
           OR TRIM(p_names[i]) = ''
           OR p_phones[i] IS NULL
           OR p_phones[i] !~ '^\+?[0-9]{10,15}$'
        THEN
            p_invalid := array_append(
                p_invalid,
                COALESCE(p_names[i], 'NULL') || ': ' ||
                COALESCE(p_phones[i], 'NULL')
            );
        ELSE
            CALL upsert_contact(
                p_names[i]::VARCHAR,
                p_phones[i]::VARCHAR
            );
        END IF;

    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(
    p_value TEXT,
    p_type TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_value IS NULL OR TRIM(p_value) = '' THEN
        RAISE EXCEPTION 'Search value cannot be empty';
    END IF;

    IF p_type = 'name' THEN

        DELETE FROM contacts
        WHERE first_name = p_value;

    ELSIF p_type = 'phone' THEN

        DELETE FROM contacts
        WHERE phone = p_value;

    ELSE
        RAISE EXCEPTION 'Invalid delete type';
    END IF;
END;
$$;