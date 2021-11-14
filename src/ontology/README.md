### Content related creation of Darwin Core imports:


dwcterms.owl: output OWL file of from [terms.csv](https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/terms/terms.csv), with DwC properties as data properties

dwciri.owl: output OWL file from [iri.csv](https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/iri/iri.csv), with DwC class as OWL classes

dwcrobot.py: code for converting terms.csv to dwcterms.csv OR iri.csv to dwciri.csv

dwcheader.csv: header row from terms.csv and iri.csv. They are currently the same. Could change. This file is not used in the code, but was used to manually generate label_row.csv.

dwclabel_row.csv: row of ROBOT formatted column headers to insert into terms.csv and iri.csv. They are currently the same. Could change.

The other contents of this directory are consistent with standard ODK output.

