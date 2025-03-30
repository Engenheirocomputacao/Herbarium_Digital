# Herbarium - Sistema de Gerenciamento de Fitoterápicos

## Testes e Integração Contínua

Este projeto utiliza testes automatizados e integração contínua para garantir a qualidade do código.

### Executando os Testes

Para executar os testes localmente, siga os passos abaixo:

1. Instale as dependências de desenvolvimento:

```bash
pip install -r requirements.txt
```

2. Execute os testes com o Django:

```bash
python manage.py test
```

3. Ou execute os testes com pytest para obter relatórios de cobertura:

```bash
pytest
```

### Cobertura de Código

Para gerar um relatório de cobertura de código:

```bash
coverage run --source='.' manage.py test
coverage report
```

Ou com pytest:

```bash
pytest --cov=.
```

### Integração Contínua

Este projeto utiliza GitHub Actions para integração contínua. A cada push ou pull request para as branches main ou master, os seguintes passos são executados automaticamente:

1. Execução de todos os testes em diferentes versões do Python (3.9, 3.10, 3.11, 3.12)
2. Geração de relatório de cobertura de código
3. Upload do relatório de cobertura para o Codecov

O arquivo de configuração da integração contínua está localizado em `.github/workflows/django-tests.yml`.