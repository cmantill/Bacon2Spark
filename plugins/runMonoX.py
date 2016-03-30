#!/usr/bin/env python

# -------------------------------------------------------------
# Driver to run pre-selection in PySpark from a json bacon file
# PySpark is the python API for Spark
# -------------------------------------------------------------

import os,sys                                 # Python utilities
import optparse                               # Parse options
from pyspark import SparkConf, SparkContext   # Import pySpark - SparkConf for configuring Spark and SparkContext main entry point for Spark functionality
from pyspark.sql import SQLContext            # SQLContext: The entry point for working with structured data (rows and columns) in Spark. Allows the creation of DataFrame objects as well as the execution of SQL queries
from external import *                        # External Datum class 

import numpy as np                            # Import numpy
import matplotlib.pyplot as plt               # Import pyPlot

# -------------------------------------------------------------
# Main 
# -------------------------------------------------------------
def main():

    # Parse arguments
    usage = 'usage: ../spark-1.6.1-bin-hadoop1/bin/pyspark --master local[2] runMonoX.py %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option("-f", "--file", dest="filename", default="/home/criss/bacon_valid.jsons", help="Input file [default: %default]")
    (opt, args) = parser.parse_args()

    # Set SQL context
    conf = SparkConf().setAppName("test")                 # SparkConf object to set configuration properties 
    sc = SparkContext(conf=conf, pyFiles=['external.py']) # SparkContext constructor: Files listed here will be added to the PYTHONPATH and shipped to remote worker machines.
    sqlContext = SQLContext(sc)                           # Create SQLContext 

    # Create the data frame from the content of the input json file
    df = sqlContext.read.json(opt.filename)

    # Return conv to pick fields as conv.something from the dataframe - see Datum external class
    # conv is an RDD (Resilient Distributed Dataset) i.e. a distributed collection of objects in Spark, is Sparks primary abstraction 
    # Each RDD is split into multiple partitions, which may be computed on different nodes of the cluster. RDDs can contain any type of Python, Java, or Scala objects, including user-defined classes.
    # conv has methods as: __add__, __getattribute__, filter, flatMap, first, count, keys, collect
    conv = df.map(lambda row: Datum.convert(row.asDict()))

    # Each "event" in conv has the following fields:
    #['AK4CHS', 'AK4Puppi', 'AK8CHS', 'AddAK8CHS', 'AddCA15CHS', 'AddCA15Puppi', 'AddCA8Puppi', 'CA15CHS', 'CA15Puppi', 'CA8Puppi', 'Electron', 'GenEvtInfo', 'GenParticle', 'Info', 'LHEWeight', 'Muon', 'PV', 'Photon', 'Tau']
    # e.g. for datum in conv: datum.PV.chi2

    # Easy example: number of Muons - maybe apply some selection
    lazy = conv.map(lambda datum: len(datum.Muon))
    nMuons = []
    for numMuons in lazy.collect():
        print numMuons
        nMuons.append(numMuons)

    # lazy.collect is not iterable
    print dir(lazy.collect)
    try:                                                                                                                                                                                  
        some_object_iterator = iter(lazy.collect)                                                                                                                                                                                
    except TypeError, te:                                                                                                                                                                                                        
        print lazy.collect, 'is not iterable'  

    # Construct easy histogram
    # hist = np.histogram(nMuons,bins=[0,1,2])
    
    # Save histogram as figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(nMuons,10,color='blue',alpha=0.8)
    plt.show()

if __name__ == "__main__":
    sys.exit(main())

