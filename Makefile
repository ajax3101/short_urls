init:
	cd app && sqlite3 db-urls.sqlite < init.sql

dev:
	cd app && FLASK_APP=app FLASK_ENV=development python -m flask run
	
run:
	cd app && FLASK_APP=app FLASK_ENV=production python -m flask run
