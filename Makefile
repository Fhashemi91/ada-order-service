##
#  Product Service
#
# @file
# @version 0.1

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run: install
	python app.py

db_upgrade: install
	alembic -c daos/migrations/alembic.ini upgrade head

deploy:
	gcloud builds submit --tag gcr.io/ada-return/order-service
	gcloud run deploy --image gcr.io/ada-return/order-service --platform managed


# end
