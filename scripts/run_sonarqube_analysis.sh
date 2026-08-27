#!/bin/bash
# scripts/run_sonar_aula.sh

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           📊 ANÁLISIS CON SONARQUBE - AULA VIRTUAL       ║"
echo "╚════════════════════════════════════════════════════════════╝"

# Cargar .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Verificar token
if [ -z "$SONAR_TOKEN" ]; then
    echo "❌ Error: SONAR_TOKEN no definido"
    exit 1
fi

# 1. Ejecutar pruebas
echo ""
echo "📝 1. Ejecutando pruebas..."
pytest tests/db/test_mysql_connection_env.py -v \
    --cov=. \
    --cov-report=xml:reports/coverage/coverage.xml

if [ ! -f "reports/coverage/coverage.xml" ]; then
    echo "❌ Error: No se generó coverage.xml"
    exit 1
fi

# 2. Ejecutar análisis con el nombre correcto
echo ""
echo "📊 2. Ejecutando análisis..."

docker run --rm \
  -v "$(pwd):/usr/src" \
  --add-host host.docker.internal:host-gateway \
  sonarsource/sonar-scanner-cli:latest \
  -Dsonar.host.url=http://host.docker.internal:9000 \
  -Dsonar.token="$SONAR_TOKEN" \
  -Dsonar.projectKey=classroom-app \
  -Dsonar.projectName="Aula Virtual" \
  -Dsonar.projectVersion=1.0 \
  -Dsonar.sources=. \
  -Dsonar.language=py \
  -Dsonar.exclusions="**/venv/**,**/tests/**,**/static/**,**/migrations/**,**/__pycache__/**,**/*.pyc" \
  -Dsonar.python.coverage.reportPaths=reports/coverage/coverage.xml

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Análisis completado exitosamente"
    echo "📊 Ver resultados en: http://localhost:9000/dashboard?id=classroom-app"
else
    echo "❌ Error en el análisis"
    exit 1
fi