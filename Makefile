run-server:
	cd server && uvicorn main:app --reload
test-server:
	cd server && pytest tests
server-install:
	cd server && pip install -r requirements.txt
server-env:
	cd server && python3 -m venv venv
run-front:
	cd front && npm start
