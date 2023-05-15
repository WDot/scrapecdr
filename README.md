# scrapecdr
Scraping Communicable Disease Reporting Requirements and Packaging in an API

To build and use the API, you need to add the following into the root directory:

MRCONSO.RRF
the "public_mm" directory of Metamap 2020

Then run "docker-compose up --build" to build and run the server. It should create a Nextjs website at localhost:3000 that renders a toy webpage that displays the JSON we have previously scraped from three Department of Health Communicable Disease Reporting websites: those for Hawaii, Indiana, and Ohio. The scrapers likely do not work now, as the webpages change somewhat frequently. The purpose of this demo is less to be a useful software and more to be an illustration: That this data, from multiple states and different Departments of Health, should be made available as an API to be consumed by applications rather than as webpages or documents to be read by people.

This work is to be presented at AMIA CIC 2023. If you find it useful, please cite us:



    @inproceedings{Dominguez2023,
	    title = {Machine-{Readable} {State}-{Level} {Communicable} {Disease} {Reporting}},
	    booktitle = {{AMIA} {CIC} 2023},
	    author = {{Dominguez, Miguel} and {Finnell, John T.}},
    }

