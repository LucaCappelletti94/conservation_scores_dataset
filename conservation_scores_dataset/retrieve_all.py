from tqdm.auto import tqdm
from epigenomic_dataset import load_epigenomes
import compress_json
import os
from .extract import extract


def retrieve_all(
    assembly: str = "hg38",
    dataset: str = "fantom",
    window_size: int = 256,
    clear_download: bool = False,
    cache_directory: str = "conservation_scores_data"
):
    """Download and mines all data relative to conservation scores for HG38.

    Parameters
    ---------------------------
    assembly: str = "hg38",
        The assembly to retrieve.
    dataset: str = "fantom",
        The dataset to retrieve, currently FANTOM5 and ROADMAP are supported.
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
        window_size=window_size,
    )

    bed_path = os.path.join(
        cache_directory,
        dataset,
        assembly,
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
            main_path = os.path.join(
                cache_directory,
                dataset,
                assembly,
                type_name,
                specific_type,
                str(window_size)
            )

            os.makedirs(main_path, exist_ok=True)

            extract(
                bed_path,
                "{main_path}/bigwig.bw".format(main_path=main_path),
                "{main_path}/target.csv".format(main_path=main_path),
                url,
                clear_download=clear_download
            )
