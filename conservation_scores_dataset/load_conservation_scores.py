from typing import Tuple
import os
from downloaders import BaseDownloader
import pandas as pd


def load_conservation_scores(
    assembly: str = "hg38",
    conservation_scores: str = "phastCons",
    conservation_score_version: str = "phastCons17way",
    dataset: str = "fantom",
    region: str = "promoters",
    window_size: int = 256,
    root: str = "datasets",
    verbose: int = 2
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return epigenomic data and labels for given parameters.

    Parameters
    ----------------------------------------
    assembly: str = "hg38",
        The genomic assembly of the data to be retrieved.
    conservation_scores: str = "phastCons",
        The conservation scores.
    conservation_score_version: str = "phastCons17way",
        The conservation score versions.
    dataset: str = "fantom",
        Dataset to consider. By default fantom.
        Currently available datasets are
        listed in the repository README file.
    region: str = "promoters",
        Region to consider. By default promoters.
        Currently available region are
        listed in the repository README file.
    window_size: int = 256,
        Window size to consider. By default 256.
        Currently available window sizes are
        listed in the repository README file.
    root: str = "datasets"
        Where to store the downloaded data.
    verbose: int = 2,
        Verbosity level.

    Returns
    ----------------------------------------
    Return tuple with input and output DataFrames.
    """
    repository = "https://github.com/LucaCappelletti94/conservation_scores_dataset/blob/main/conservation_scores"
    get_parameter = "?raw=true"
    data_path_placeholder = "{{root}}/{assembly}/{conservation_scores}/{conservation_score_version}/{dataset}/{region}/{window_size}.tsv.xz".format(
        root=root,
        assembly=assembly,
        conservation_scores=conservation_scores,
        conservation_score_version=conservation_score_version,
        dataset=dataset,
        window_size=window_size,
        region=region,
    )
    data_path = data_path_placeholder.format(root=root)

    downloader = BaseDownloader(
        target_directory=root,
        verbose=verbose,
        auto_extract=False
    )

    urls = data_path_placeholder.format(root=repository)+get_parameter
    downloader.download(
        urls=urls,
        paths=data_path
    )

    X = pd.read_csv(
        data_path,
        low_memory=False,
        header=None,
    )

    X.columns = [
        "chrom",
        "chromStart",
        "chromEnd",
        "strand",
        "window_size",
        *[
            i
            for i in range(X.shape[1] - 5)
        ]
    ]

    return X
