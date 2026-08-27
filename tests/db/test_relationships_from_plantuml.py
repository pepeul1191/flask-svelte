# tests/db/test_relationships_from_plantuml.py
import pytest
from scripts.parse_plantuml import PlantUMLParser

class TestRelationshipsFromPlantUML:
  """Pruebas de relaciones generadas desde PlantUML"""
  
  @pytest.fixture(scope='class')
  def schema(self):
    return PlantUMLParser('docs/db_diagram_sql.puml')
  
  def test_foreign_keys_exist(self, test_db, schema):
    """Verifica que todas las FK del diagrama estén definidas"""
    expected_fks = [
      ('provinces', 'departments', 'department_id'),
      ('districts', 'provinces', 'province_id'),
      ('persons', 'sexs', 'sex_id'),
      ('persons', 'document_types', 'document_type_id'),
      ('phones', 'persons', 'person_id'),
      ('addresses', 'persons', 'person_id'),
      ('addresses', 'districts', 'district_id'),
      ('workers', 'persons', 'person_id'),
      ('students', 'persons', 'person_id'),
      ('representatives', 'persons', 'person_id'),
      ('representatives_students_roles', 'representatives', 'representative_id'),
      ('representatives_students_roles', 'students', 'student_id'),
      ('representatives_students_roles', 'representative_roles', 'representative_role_id'),
      ('courses', 'levels', 'level_id'),
      ('courses', 'course_branches', 'branch_id'),
      ('courses', 'workers', 'worker_id'),
      ('sections', 'courses', 'course_id'),
      ('sections_workers_roles', 'sections', 'section_id'),
      ('sections_workers_roles', 'workers', 'worker_id'),
      ('sections_workers_roles', 'worker_roles', 'worker_role_id'),
      ('sections_students', 'sections', 'section_id'),
      ('sections_students', 'students', 'student_id'),
      ('folders', 'folders', 'parent_id'),
      ('documents', 'folders', 'folder_id'),
      ('folder_common_materials', 'courses', 'course_id'),
      ('folder_section_materials', 'sections', 'section_id'),
      ('section_evaluations', 'sections', 'section_id'),
      ('section_evaluations', 'workers', 'worker_id'),
      ('section_evaluations', 'evaluation_types', 'evaluation_type_id'),
      ('evaluation_documents', 'section_evaluations', 'section_evaluation_id'),
      ('evaluation_documents', 'documents', 'document_id'),
      ('section_evaluation_grades', 'section_evaluations', 'section_evaluation_id'),
      ('section_evaluation_grades', 'students', 'student_id'),
      ('section_evaluation_submissions', 'section_evaluations', 'section_evaluation_id'),
      ('section_evaluation_submissions', 'students', 'student_id'),
      ('submission_documents', 'section_evaluation_submissions', 'submission_id'),
      ('submission_documents', 'documents', 'document_id'),
      ('adverts', 'sections', 'section_id'),
      ('adverts', 'workers', 'worker_id')
    ]
    
    for table, referenced_table, fk_column in expected_fks:
      test_db.execute(f"""
        SELECT COUNT(*) as count
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_NAME = '{table}'
        AND COLUMN_NAME = '{fk_column}'
        AND REFERENCED_TABLE_NAME = '{referenced_table}'
      """)
      result = test_db.cursor.fetchone()
      assert result['count'] > 0, \
        f"No existe FK de {table}.{fk_column} a {referenced_table}"
  
  def test_relationship_integrity(self, test_db):
    """Prueba integridad de relaciones principales"""
    
    # 1. Probar jerarquía ubicación
    test_db.execute("""
      INSERT INTO departments (id, name) VALUES (999, 'Test Dept')
    """)
    test_db.execute("""
      INSERT INTO provinces (id, name, department_id) VALUES (999, 'Test Prov', 999)
    """)
    test_db.execute("""
      INSERT INTO districts (id, name, province_id) VALUES (999, 'Test Dist', 999)
    """)
    test_db.commit()
    
    test_db.execute("""
      SELECT d.name, p.name, dist.name
      FROM departments d
      JOIN provinces p ON d.id = p.department_id
      JOIN districts dist ON p.id = dist.provincia_id
      WHERE d.id = 999
    """)
    result = test_db.cursor.fetchone()
    assert result is not None
    
    # Limpiar
    test_db.execute("DELETE FROM districts WHERE id = 999")
    test_db.execute("DELETE FROM provinces WHERE id = 999")
    test_db.execute("DELETE FROM departments WHERE id = 999")
    test_db.commit()
    
    # 2. Probar flujo persona -> estudiante
    test_db.execute("""
      INSERT INTO persons (id, names, lastNames, documentNumber) 
      VALUES (1000, 'Test', 'Student', '12345678')
    """)
    test_db.execute("""
      INSERT INTO students (id, person_id, code) 
      VALUES (1000, 1000, 2024001)
    """)
    test_db.commit()
    
    test_db.execute("""
      SELECT s.code, p.names
      FROM students s
      JOIN persons p ON s.person_id = p.id
      WHERE s.id = 1000
    """)
    result = test_db.cursor.fetchone()
    assert result is not None
    assert result['code'] == 2024001
    
    # Limpiar
    test_db.execute("DELETE FROM students WHERE id = 1000")
    test_db.execute("DELETE FROM persons WHERE id = 1000")
    test_db.commit()
  
  def test_cascade_behavior(self, test_db):
    """Verifica comportamiento CASCADE en relaciones"""
    test_db.execute("""
      SELECT 
        TABLE_NAME,
        REFERENCED_TABLE_NAME,
        DELETE_RULE,
        UPDATE_RULE
      FROM information_schema.REFERENTIAL_CONSTRAINTS
      WHERE CONSTRAINT_SCHEMA = 'classroom'
    """)
    
    constraints = test_db.cursor.fetchall()
    
    # Verificar que al menos existen constraints
    assert len(constraints) > 0, "No hay constraints definidas"
    
    # Verificar algunas relaciones críticas
    for constraint in constraints:
      if constraint['TABLE_NAME'] == 'students':
        assert constraint['DELETE_RULE'] in ['CASCADE', 'RESTRICT']