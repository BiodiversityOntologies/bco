## Customize Makefile settings for bco
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

imports/obi_import.owl: mirror/obi.owl imports/obi_terms_combined.txt
	if [ $(IMP) = true ]; then $(ROBOT) query -i $< --update ../sparql/preprocess-module.ru \
		extract -T imports/obi_terms_combined.txt --force true --copy-ontology-annotations true --intermediates minimal --individuals minimal --method BOT \
		query --update ../sparql/inject-subset-declaration.ru --update ../sparql/postprocess-module.ru \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@; fi
