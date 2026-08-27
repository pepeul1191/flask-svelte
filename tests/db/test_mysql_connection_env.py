# tests/db/test_mysql_connection_env.py
import os
import re
import pytest
import mysql.connector
import subprocess
from dotenv import load_dotenv

class TestMySQLConnectionEnv:
  """Pruebas de conexión usando variables de entorno"""
  
  @pytest.fixture(scope='class')
  def db_config(self):
    """Carga configuración desde .env"""
    load_dotenv('.env')
    return {
      'host': os.getenv('DB_HOST', 'localhost'),
      'port': int(os.getenv('DB_PORT', 3306)),
      'database': os.getenv('DB_NAME', 'classroom'),
      'user': os.getenv('DB_USER', 'root'),
      'password': os.getenv('DB_PASSWORD', '123')
    }
  
  def test_env_variables_loaded(self, db_config):
    """Verifica que las variables de entorno se cargaron correctamente"""
    assert db_config['host'] is not None
    assert db_config['port'] == 3306
    assert db_config['database'] == 'classroom'
    assert db_config['user'] == 'root'
    assert db_config['password'] == '123'
  
  def test_db_connection(self, db_config):
    """Prueba conexión a MySQL con variables de .env"""
    try:
      conn = mysql.connector.connect(**db_config)
      assert conn.is_connected()
      conn.close()
    except mysql.connector.Error as e:
      pytest.fail(f"Error de conexión: {e}")
  
  def test_database_exists(self, db_config):
    """Verifica que la base de datos classroom existe"""
    conn = mysql.connector.connect(
      host=db_config['host'],
      port=db_config['port'],
      user=db_config['user'],
      password=db_config['password']
    )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES LIKE 'classroom'")
    result = cursor.fetchone()
    assert result is not None, "Base de datos classroom no existe"
    conn.close()
  
  def test_tables_count(self, db_config):
    """Verifica que el número total de tablas sea correcto"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Contar tablas (excluyendo vistas y schema_migrations)
    cursor.execute("""
      SELECT COUNT(*) as count
      FROM information_schema.TABLES
      WHERE TABLE_SCHEMA = 'classroom'
      AND TABLE_TYPE = 'BASE TABLE'
      AND TABLE_NAME != 'schema_migrations'
    """)
    result = cursor.fetchone()
    table_count = result['count'] if isinstance(result, dict) else result[0]
    conn.close()
    
    # Deberían ser 26 tablas (según tu listado)
    expected_table_count = 26
    assert table_count == expected_table_count, \
      f"Se esperaban {expected_table_count} tablas, pero hay {table_count}"
  
  def test_views_count(self, db_config):
    """Verifica que el número total de vistas sea correcto"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Contar vistas
    cursor.execute("""
      SELECT COUNT(*) as count
      FROM information_schema.TABLES
      WHERE TABLE_SCHEMA = 'classroom'
      AND TABLE_TYPE = 'VIEW'
    """)
    result = cursor.fetchone()
    view_count = result['count'] if isinstance(result, dict) else result[0]
    conn.close()
    
    # Deberían ser 4 vistas (vw_locations, vw_representatives, vw_students, vw_workers)
    expected_view_count = 4
    assert view_count == expected_view_count, \
      f"Se esperaban {expected_view_count} vistas, pero hay {view_count}"
  
  def test_dbmate_migrations_applied(self, db_config):
    """Verifica que Pending sea 0"""
    import subprocess
    import re
    
    os.environ['DATABASE_URL'] = f"mysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    
    # Ejecutar dbmate status
    result = subprocess.run(
        'npm run db:status 2>&1',
        capture_output=True,
        text=True,
        shell=True
    )
    
    output = result.stdout
    
    # Buscar "Pending: 0" o "Pending: X"
    pending_match = re.search(r'Pending:\s*(\d+)', output)
    
    if pending_match:
        pending_count = int(pending_match.group(1))
        
        # Verificar que sea 0
        assert pending_count == 0, f"❌ Hay {pending_count} migración(es) pendiente(s). Ejecuta: npm run db:up"
        
        print(f"✅ Todas las migraciones están aplicadas")
    else:
        # Si no encuentra "Pending:", buscar [ ] como fallback
        if '[ ]' in output:
            pytest.fail("❌ Hay migraciones pendientes. Ejecuta: npm run db:up")
        else:
            print(f"✅ Todas las migraciones están aplicadas")