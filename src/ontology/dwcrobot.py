#!/usr/bin/env python3
"""
Author : Ramona L. Walls <rlwalls2008@gmail.com>
Date   : 2021-14-31
Purpose: Reformat a CSV file with Darwin Core terms into the format needed to convert it to OWL using ROBOT.
"""

#Steps:
#Load mirror/terms.csv or mirror/iri.csv
#Concatenate 'DWC:' to each ID in column 2
#Change the "rfd-type" column to the appropriate OWL type
#Insert a term label row, as needed by ROBOT, as row 2 into the CSV file.
#Save output to a CSV file.
#By default, converts terms.csv to dwcterms.csv. To convert iri.csv to dwciri.csv, just specify the input and output.


import argparse, os, pandas, re


# --------------------------------------------------
def get_args():
    """Get command-line arguments to input files"""

    parser = argparse.ArgumentParser(
        description='get command line arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i',
                        '--inputfile',
                        metavar='string',
                        help='input CSV file with terms',
                        type=str,
                        default='mirror/terms.csv')

    parser.add_argument('-l',
                        '--labels',
                        help='file containing the label row for robot',
                        metavar='string',
                        type=str,
                        default='dwclabel_row.csv')

    parser.add_argument('-o',
                        '--outputfile',
                        help='modified output file',
                        metavar='string',
                        type=str,
                        default='../modules/dwcterms.csv')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """reformat the DwC terms or iri file"""

    args = get_args()
    outfile = args.outputfile
    infile = pandas.read_csv(args.inputfile)
    labels = pandas.read_csv(args.labels)
    #need to fix dcterms:description property
    rlabels = list(labels)
    robotlabels = list()
    #get rid of "Unnamed:" column headers created by pandas
    for x in rlabels:
        y = re.sub('Unnamed: [0-9]+', '', x)
        robotlabels.append(y)
    new = infile
    #replace term_localName column with robot formatted ID column
    ID = new['term_localName']
    IDlist = []
    for id in ID:
        newid = 'DWC:'+id
        IDlist.append(newid)
    #The True statement below overwrites the existing DF "new")
    new.insert(1, 'ID', IDlist, True)
    new.drop(columns = ['term_localName'], inplace=True)
    new.rename(columns = {'ID': 'term_localName'}, inplace=True)
    #replace rdf_type column with robot formatted TYPE column, using owl:DataProperty or owl:ObjectProperty. 
    #The rdf type for class is interpretted correctly already.
    #The type for DwCType is http://purl.org/dc/dcam/VocabularyEncodingScheme. This is interpretted as an individual.
    #However, since DwCType is deprecated, I will ignore it for now.
    if args.inputfile == 'mirror/terms.csv':
        type = 'owl:DataProperty'
    else:
        type = 'owl:ObjectProperty'
    tp = new['rdf_type']
    tplist = []
    for t in tp:
        z = re.sub('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property', type, t)
        tplist.append(z)
    new.insert(13, 'Type', tplist, True)
    new.drop(columns = ['rdf_type'], inplace=True)
    #Insert the second row of robot labels and fix the index
    new.loc[-1] = robotlabels
    new.index = new.index + 1
    new =  new.sort_index()
    new.to_csv(outfile, index=False)

#TODO: write code to remove http://rs.tdwg.org/dwc/terms/attributes/UseWithIRI as the domain for IRI terms. I've done this manually for now.

# --------------------------------------------------
if __name__ == '__main__':
    main()
