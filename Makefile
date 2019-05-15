init:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	mkdir -p data

install:
	venv/bin/pip install -r requirements.txt

clean:
	rm -rf venv dist

run:
	venv/bin/python transform.py --infile data-raw/GEOBOX4-3.TXT --outfile dist/Goeggingen_1.shp
	venv/bin/python transform.py --i data-raw/GEOBOX4-4.TXT --o dist/Goeggingen_2.shp
	venv/bin/python transform.py --i data-raw/GEOBOX4-4.TXT --o dist/Goeggingen_2_date_filtered.shp --date 60319
