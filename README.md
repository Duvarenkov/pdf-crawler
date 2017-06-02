# pdf-crawler

Endpoints:
- POST /upload/[SOME_NAME]

Allows uploading pdf files. Names file after `SOME_NAME` portion of url.
Returns a JSON with created Document object data.

- GET /urls

Returns a JSON with list of all urls data.

- GET /urls/[URL_TOKEN]

Returns a JSON with details of one url.

- GET /documents

Returns a JSON with list of all documents data.

- GET /documents/[DOCUMENT_TOKEN]

Returns a JSON with list of document's urls.
