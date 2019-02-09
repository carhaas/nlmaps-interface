# NLmaps Interface

This repository provides the source code to create the NLmaps interface as seen here: https://nlmaps.cl.uni-heidelberg.de/

To set it up, note the following points:

  * Search and replace /srv/nlmaps/ with the location where the files are stored on your system

  * To query nominatim, you need a API key which you can get here: https://developer.mapquest.com/documentation/open/
The key needs to be placed in the position of API_KEY in htdocs/index.html, cgi/query.cgi, in scripts/query_nominatim.py and htdocs/lib/leaflet/leafletembed.js

  * To connect your parser, see query.cgi line 95 and line 111 and replace the command to nematus with your own call pipeline. In line 95, we expect that the user location has been set and in line 111, we expect that the search location is supplied in the question. The entire pipeline should write the answer to a file called "answers" in the temp_dir created by query.cgi. Additionally it expects the mrl in a file called "mrls" and any additional information, each GPS coordinates in a file called "latlong". See scripts/run_parsing_pipeline.sh for an example.

  * To set up the OSM database to accept NLmaps MRL, see here: https://github.com/carhaas/overpass-nlmaps

  * For the NLmaps scripts to linearise and functionalise see: https://github.com/carhaas/scripts_nlmaps

  * The NLmaps corpus can be downloaded here: https://www.cl.uni-heidelberg.de/statnlpgroup/nlmaps/

  * Images have been removed due to copyright issues. The icon ("loading.gif" in index.html) that is displayed while a question is being processed can for example be obtained here: https://loading.io/