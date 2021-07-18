Conservation scores dataset
===================================
Pipeline to automatically retrieve and preprocess conservation scores

Installing the package
-----------------------------------
As for any python package, simply run:

.. code:: shell

    pip install conservation_scores_dataset

Usage examples
------------------------------------
The following two usage examples will show both how to run the pipeline and how to retrieve the already pre-computed values stored within this GitHub repository.

Running the pipeline to retrieve the data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to run the pipeline yourself, after taking note that some preprocessed data are already available within this repository, consider that the downloaded file will require a total size of ADDSIZE.

After having installed the package, just run the following to retrieve all data relative to the FANTOM5 and ROADMAP datasets for enhancers and promoters:

.. code:: python

    from conservation_scores_dataset import retrieve_all
    retrieve_all()

It will display some loading bars showing you what the pipeline is doing at a given time, such as the following ones:

ADDIMAGE

Based on the main loop provided in the retrieve all file, other similar automati retrieval pipelines for other BED files can be trivially built.