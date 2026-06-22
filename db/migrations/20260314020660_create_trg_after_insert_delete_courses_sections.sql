-- migrate:up

DROP TRIGGER IF EXISTS trg_courses_after_insert;
DROP TRIGGER IF EXISTS trg_courses_after_update;

CREATE TRIGGER trg_courses_after_insert
AFTER INSERT ON courses
FOR EACH ROW
BEGIN
    DECLARE new_folder_id INT;

    INSERT INTO folders (parent_id, title, description)
    VALUES (
        NULL,
        'root_course_folder',
        CONCAT('carpeta raiz del material común el curso ', NEW.name)
    );

    SET new_folder_id = LAST_INSERT_ID();

    INSERT INTO folder_common_materials (id, course_id)
    VALUES (new_folder_id, NEW.id);
END;

CREATE TRIGGER trg_courses_after_update
AFTER UPDATE ON courses
FOR EACH ROW
BEGIN
    IF OLD.name <> NEW.name THEN
        UPDATE folders f
        INNER JOIN folder_common_materials fcm ON f.id = fcm.id
        SET f.description = CONCAT(
            'carpeta raiz del material común el curso ',
            NEW.name
        )
        WHERE fcm.course_id = NEW.id
          AND f.title = 'root_course_folder';
    END IF;
END;


-- migrate:down

DROP TRIGGER IF EXISTS trg_courses_after_insert;
DROP TRIGGER IF EXISTS trg_courses_after_update;