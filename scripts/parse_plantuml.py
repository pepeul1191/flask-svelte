# scripts/parse_plantuml.py
import re
from pathlib import Path

class PlantUMLParser:
  """Parsea el archivo PlantUML para generar pruebas automáticas"""
  
  def __init__(self, plantuml_file):
    self.plantuml_file = plantuml_file
    self.tables = {}
    self.relationships = []
    self.parse()
  
  def parse(self):
    """Extrae tablas y relaciones del PlantUML"""
    with open(self.plantuml_file, 'r') as f:
      content = f.read()
    
    # Extraer tablas
    table_pattern = r'table\s+(\w+)\s*\{([^}]*)\}'
    for match in re.finditer(table_pattern, content):
      table_name = match.group(1)
      columns = self._parse_columns(match.group(2))
      self.tables[table_name] = columns
    
    # Extraer relaciones
    rel_pattern = r'(\w+)\s*\|\|\s*--\s*\{\|\}\s*(\w+)|(\w+)\s*\}\{\s*--\s*\|\|\s*(\w+)'
    for match in re.finditer(rel_pattern, content):
      # Determinar tipo de relación
      if match.group(1) and match.group(2):
        self.relationships.append({
          'from': match.group(1),
          'to': match.group(2),
          'type': 'one-to-many'
        })
      elif match.group(3) and match.group(4):
        self.relationships.append({
          'from': match.group(4),
          'to': match.group(3),
          'type': 'one-to-many'
        })
  
  def _parse_columns(self, columns_text):
    """Parsea columnas de una tabla"""
    columns = []
    for line in columns_text.strip().split('\n'):
      line = line.strip()
      if not line:
        continue
      
      # Detectar PK
      is_pk = 'PK' in line
      # Detectar FK
      is_fk = 'FK' in line
      
      # Extraer nombre y tipo
      parts = line.split()
      if len(parts) >= 2:
        col_name = parts[0]
        col_type = parts[1]
        columns.append({
          'name': col_name,
          'type': col_type,
          'is_pk': is_pk,
          'is_fk': is_fk
        })
    return columns
  
  def get_all_tables(self):
    """Retorna todas las tablas"""
    return list(self.tables.keys())
  
  def get_table_columns(self, table_name):
    """Retorna columnas de una tabla"""
    return self.tables.get(table_name, [])
  
  def get_relationships(self):
    """Retorna todas las relaciones"""
    return self.relationships
  
  def get_pk_columns(self, table_name):
    """Retorna columnas PK de una tabla"""
    return [col for col in self.tables.get(table_name, []) if col['is_pk']]
  
  def get_fk_columns(self, table_name):
    """Retorna columnas FK de una tabla"""
    return [col for col in self.tables.get(table_name, []) if col['is_fk']]