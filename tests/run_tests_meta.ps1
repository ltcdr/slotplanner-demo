cd ..

pytest -vv --html=ci_artifacts/report.html --self-contained-html --junitxml=ci_artifacts/junit.xml --cov=services --cov-report=html:coverage/htmlcov --cov-report=xml:coverage/coverage.xml
