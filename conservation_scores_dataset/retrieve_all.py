from tqdm.auto import tqdm
from epigenomic_dataset import load_epigenomes
import compress_json
import os
from .extract import extract


def retrieve_all(
    assembly: str = "hg38",
    dataset: str = "fantom",
    region: str = "promoters",
    window_size: int = 256,
    clear_download: bool = False,
    cache_directory: str = "conservation_scores"
):
    """Download and mines all data relative to conservation scores for HG38.

    Parameters
    ---------------------------
    assembly: str = "hg38",
        The assembly to retrieve.
    dataset: str = "fantom",
        The dataset to retrieve, currently FANTOM5 and ROADMAP are supported.
    region: str = "promoters",
        The region to retrieve the data for.
        It can either be "promoters" or "enhancers".
    window_size: int = 256,
        The window size to mine.
    clear_download: bool = False,
        Whether to clear the data once downloaded.
    """
    # Retrieving the epigenomic data
    # We retrieve the labels from here and not directly from crr labels
    # only because the labels are cached in load epigenomes and they
    # do not require further processing.
    _, y = load_epigenomes(
        assembly=assembly,
        dataset=dataset,
        region=region,
        window_size=window_size,
    )

    bed_path = os.path.join(
        cache_directory,
        dataset,
        assembly,
        region,
        "{}.bed".format(window_size)
    )

    os.makedirs(os.path.dirname(bed_path), exist_ok=True)

    bed = y.reset_index()[y.index.names]
    bed.to_csv(bed_path, sep="\t", header=False, index=False)

    urls = compress_json.local_load("urls.json")[assembly]
    for type_name, data_urls in tqdm(
        list(urls.items()),
        desc="Retrieve all types of data"
    ):
        for specific_type, url in tqdm(
            list(data_urls.items()),
            desc="Retrieve data of type {}".format(type_name)
        ):
            bigwig_path = os.path.join(
                cache_directory,
                assembly,
                type_name,
                "{}.bw".format(specific_type),
            )

            target_path = os.path.join(
                cache_directory,
                dataset,
                assembly,
                region,
                type_name,
                "{}.tsv".format(specific_type),
            )

            os.makedirs(os.path.dirname(bigwig_path), exist_ok=True)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            extract(
                bed_path,
                bigwig_path,
                target_path,
                url,
                clear_download=clear_download
            )
