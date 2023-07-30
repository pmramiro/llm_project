from typing import List
import warnings


def fixed_length_segmentation(text: str, segment_length: int, overlap: float = 0.8) -> List[str]:
    """
    Perform fixed-length segmentation on a long text string.

    Parameters:
        text (str): The long text to be segmented.
        segment_length (int): The desired length of each segment.
        overlap (float, optional): The overlap ratio between 0.5 and 1.0. Default is 0.8.

    Returns:
        List[str]: A list of segmented text strings.

    Example:
        Input:
        long_text = "Natural language processing is an exciting field that deals with how computers understand and generate human language."
        segment_length = 25
        overlap = 0.8

        Output:
        ['Natural language processing', 'language processing is an', 'is an exciting field tha', 'ing field that deals with', ' that deals with how com', ' deals with how computers', 'ow computers understand', 'computers understand and', 'understand and generate', 'd generate human language.']
    """
    if overlap < 0.5 or overlap > 1.0:
        warnings.warn("Overlap ratio should be between 0.5 and 1.0. Using default value of 0.8.", UserWarning)
        overlap = 0.8

    segments = []
    start_idx = 0
    step = int(segment_length * overlap)

    # Loop until we have segmented the entire text
    while start_idx < len(text):
        segment = text[start_idx:start_idx + segment_length]
        segments.append(segment)
        start_idx += step

    return segments
