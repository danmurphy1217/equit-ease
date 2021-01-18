setup:
	( \
		python3 -m venv venv; \
		source venv/bin/activate; \
		pip3 install -r requirements.txt \
	)
clean:
	find . -name '*.pyc' -exec rm -rf {} \;
	find . -name '*.DS_Store' -exec rm {} \;
	find . -type dir -name '__pycache__' -delete;
clear-py:
	rm -rf build dist equit_ease_dmurphy1217.egg-info;