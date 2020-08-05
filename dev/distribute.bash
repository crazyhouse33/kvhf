bash -c "set -e ; cd ..; python3.7 setup.py sdist bdist_wheel; python3 -m twine upload --repository testpypi --skip-existing dist/*"
