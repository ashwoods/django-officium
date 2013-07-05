.PHONY: test release doc

test:
	#flake8 shisan --ignore=E501,E127,E128,E124 --filename=*.py --exclude=static,migrations
	coverage run --branch --source=officium `which django-admin.py` test officium --settings=officium.tests.test_settings
	coverage report --omit=officium/test*

#release:
#	python setup.py sdist bdist_wheel register upload -s

#doc:
#	cd docs; make html; cd ..
