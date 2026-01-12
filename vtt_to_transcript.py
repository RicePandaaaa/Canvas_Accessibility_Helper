from typing import BinaryIO

def vtt_to_plain_text(file_object: BinaryIO, file_name: str) -> str | None:
    """
    Extracts the transcript text from a VTT file and places it in a plain text file.

    Args:
        file_object: The file-like object from Streamlit's file_uploader
        file_name: The name of the uploaded file

    Returns:
        str | None: The path to the converted plain text file or None if an error occurs.
    """
    # Read from the file object and decode
    content = file_object.read().decode('utf-8')
    
    # Split into lines and skip the first 2
    lines = content.split('\n')
    remaining_content = '\n'.join(lines[2:])
    
    # Split on blank lines
    chunks: list[str] = remaining_content.split('\n\n')
    
    # Only interested in the text, so for each chunk, first split on the newline
    # then take the last element, which is the transcript text
    transcript_text: list[str] = [chunk.split('\n')[-1] for chunk in chunks]
    
    # Remove the "<v ->" tag from the transcript text
    transcript_text: list[str] = [text.replace('<v ->', '') for text in transcript_text]
    
    # String sentences together using punctuation marks
    sentences: list[str] = []
    current_sentence = ""
    sentence_punctuations: list[str] = ['.', '!', '?']

    for text in transcript_text:
        # Skip empty text
        if not text:
            continue

        # If ending punctuation is found, add the text to the end of the current sentence
        if text[-1] in sentence_punctuations:
            current_sentence += text + " "
            sentences.append(current_sentence)
            current_sentence = ""
        else:
            # Add the text with a space after for the next text
            current_sentence += text + " "

    # Add any remaining sentence
    if current_sentence:
        sentences.append(current_sentence)

    # Create output file with sentences
    new_file_name: str = "converted_" + file_name.split('.')[0] + ".txt"

    with open(new_file_name, 'w') as output_file:
        output_file.writelines(sentences)
        return new_file_name

    return None