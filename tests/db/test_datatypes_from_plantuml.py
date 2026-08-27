# tests/db/test_datatypes_from_plantuml.py
import pytest
from scripts.parse_plantuml import PlantUMLParser

class TestDataTypesFromPlantUML:
  """Pruebas de tipos de datos desde PlantUML"""
  
  @pytest.fixture(scope='class')
  def schema(self):
    return PlantUMLParser('docs/db_diagram_sql.puml')
  
  def test_column_data_types(self, test_db, schema):
    """Verifica que los tipos de datos coincidan con el diagrama"""
    
    # Mapeo de tipos esperados
    expected_types = {
      'sexs': {
        'id': 'int',
        'name': 'varchar(45)'
      },
      'persons': {
        'id': 'int',
        'names': 'varchar(45)',
        'lastNames': 'varchar(45)',
        'documentNumber': 'varchar(12)',
        'imageUrl': 'varchar(70)',
        'birthDate': 'date',
        'created': 'datetime',
        'updated': 'datetime',
        'sex_id': 'int',
        'document_type_id': 'int'
      },
      'workers': {
        'id': 'int',
        'code': 'int',
        'bio': 'text',
        'email': 'varchar(100)',
        'user_id': 'int',
        'person_id': 'int'
      },
      'students': {
        'id': 'int',
        'code': 'int',
        'email': 'varchar(100)',
        'user_id': 'int',
        'person_id': 'int'
      },
      'courses': {
        'id': 'int',
        'name': 'varchar(45)',
        'code': 'varchar(10)',
        'description': 'text',
        'sylabus_url': 'varchar(100)',
        'level_id': 'int',
        'branch_id': 'int',
        'worker_id': 'int'
      },
      'sections': {
        'id': 'int',
        'name': 'varchar(45)',
        'description': 'text',
        'image_url': 'varchar(100)',
        'course_id': 'int'
      },
      'evaluation_types': {
        'id': 'int',
        'name': 'varchar(50)',
        'icon': 'varchar(15)'
      },
      'adverts': {
        'id': 'int',
        'header': 'varchar(45)',
        'description': 'text',
        'created': 'datetime',
        'updated': 'datetime',
        'published_from': 'datetime',
        'published_to': 'datetime',
        'visible': 'tinyint(1)',
        'section_id': 'int',
        'worker_id': 'int'
      }
    }
    
    for table_name, columns in expected_types.items():
      test_db.execute(f"SHOW COLUMNS FROM {table_name}")
      db_columns = {row['Field']: row['Type'] for row in test_db.cursor.fetchall()}
      
      for col_name, expected_type in columns.items():
        if col_name in db_columns:
          db_type = db_columns[col_name].lower()
          # Verificar que el tipo sea compatible
          expected = expected_type.lower()
          if 'varchar' in expected:
            assert 'varchar' in db_type, \
              f"Tipo incorrecto en {table_name}.{col_name}. Esperado: {expected}, Actual: {db_type}"
          elif 'text' in expected:
            assert 'text' in db_type or 'blob' in db_type, \
              f"Tipo incorrecto en {table_name}.{col_name}. Esperado: {expected}, Actual: {db_type}"
          elif 'datetime' in expected:
            assert 'datetime' in db_type, \
              f"Tipo incorrecto en {table_name}.{col_name}. Esperado: {expected}, Actual: {db_type}"
          elif 'date' in expected:
            assert 'date' in db_type, \
              f"Tipo incorrecto en {table_name}.{col_name}. Esperado: {expected}, Actual: {db_type}"
          elif 'int' in expected:
            assert 'int' in db_type or 'bigint' in db_type, \
              f"Tipo incorrecto en {table_name}.{col_name}. Esperado: {expected}, Actual: {db_type}"
          elif 'decimal' in expected:
            assert 'decimal' in db_type, \
              f"Tipo incorrecto en {table_name}.{col_name}. Esperado: {expected}, Actual: {db_type}"
          elif 'boolean' in expected or 'tinyint(1)' in expected:
            assert 'tinyint' in db_type, \
              f"Tipo incorrecto en {table_name}.{col_name}. Esperado: {expected}, Actual: {db_type}"
  
  def test_string_lengths(self, test_db):
    """Verifica longitudes de campos VARCHAR importantes"""
    test_db.execute("""
      SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
      FROM information_schema.COLUMNS
      WHERE TABLE_SCHEMA = 'classroom'
      AND DATA_TYPE = 'varchar'
    """)
    
    varchar_columns = test_db.cursor.fetchall()
    
    # Verificar longitudes específicas
    expected_lengths = {
      ('sexs', 'name'): 45,
      ('document_types', 'name'): 20,
      ('departments', 'name'): 45,
      ('provinces', 'name'): 45,
      ('districts', 'name'): 45,
      ('persons', 'names'): 45,
      ('persons', 'lastNames'): 45,
      ('persons', 'documentNumber'): 12,
      ('persons', 'imageUrl'): 70,
      ('workers', 'email'): 100,
      ('students', 'email'): 100,
      ('representatives', 'email'): 100,
      ('courses', 'name'): 45,
      ('courses', 'code'): 10,
      ('courses', 'sylabus_url'): 100,
      ('sections', 'name'): 45,
      ('sections', 'image_url'): 100,
      ('evaluation_types', 'name'): 50,
      ('evaluation_types', 'icon'): 15,
      ('adverts', 'header'): 45,
      ('phones', 'description'): 40,
      ('phones', 'phone'): 20,
      ('addresses', 'description'): 40,
      ('addresses', 'address'): 255,
      ('folders', 'title'): 100,
      ('documents', 'title'): 100,
      ('documents', 'url'): 255
    }
    
    for col in varchar_columns:
      key = (col['TABLE_NAME'], col['COLUMN_NAME'])
      if key in expected_lengths:
        expected = expected_lengths[key]
        actual = col['CHARACTER_MAXIMUM_LENGTH']
        assert actual == expected or actual >= expected, \
          f"Longitud incorrecta en {col['TABLE_NAME']}.{col['COLUMN_NAME']}. " \
          f"Esperado: {expected}, Actual: {actual}"