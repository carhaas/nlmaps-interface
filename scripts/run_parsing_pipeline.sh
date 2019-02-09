#!/bin/bash

# Preprocess question
python /srv/nlmaps/scripts/en2tok.py -i $1/question -o $1/tok

# Tag POIs and locations in the question, query_server.py is a nematus file: https://github.com/EdinburghNLP/nematus
# The first nematus model takes an English question and tags each word as a location (L), a POI (P) or as other (O)
python /srv/nlmaps/nematus/query_server.py -i $1/question -o $1/tagged -p 8081
python /srv/nlmaps/scripts/generate_locs_file.py -i $1/question -t $1/tagged

# For locations, get the highest ranked Nominatim area ID
python /srv/nlmaps/scripts/query_nominatim.py -i $1/tagged.locations -o $1/tagged.locations_nom

# Turn question into mrl
python /srv/nlmaps/nematus/query_server.py -i $1/this_question -o $1/loc.lin

# Turn linearised MRL into functionalised MRL (bracket structure), see https://github.com/carhaas/scripts_nlmaps
python /srv/nlmaps/scripts/functionalise.py -i $1/loc.lin -o $1/loc.mrl

# Re-insert the locations
python /srv/nlmaps/scripts/reinsert_locs.py -i $1/loc.mrl -l $1/tagged.locations_nom -p $1/tagged.pois -o $1/mrls

# Run query against OSM database, see https://github.com/carhaas/overpass-nlmaps
/srv/nlmaps/osm3s_v0.7.51/query_db -d /srv/nlmaps/db -f $1/mrls -a $1/answers -l $1/latlong

NOM=`cat $1/tagged.locations_nom`
LOC=`cat $1/tagged.locations`
perl -p -i -e "s|$NOM|$LOC|g" $1/latlong
perl -p -i -e "s|$NOM|$LOC|g" $1/mrls