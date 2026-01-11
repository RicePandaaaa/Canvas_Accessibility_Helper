# Allow user to input file name
file_name = "pradip week 1 lecture video.vtt"

# Open the file
with open(file_name, 'r') as input_file:
    # Skip the first 2 lines
    next(input_file)
    next(input_file)

    # Split on blank lines (so \n\n)
    chunks = input_file.read().split('\n\n')
    

    # Only interested in the text, so for each chunk, first split on the newline
    # then take the last element, which is the transcript text
    transcript_text = [chunk.split('\n')[-1] for chunk in chunks]
    
    # Remove the "<v -> tag" from the transcript text
    transcript_text = [text.replace('<v ->', '') for text in transcript_text]
    
    # String sentences together using punctuation marks
    sentences = []
    current_sentence = ""
    sentence_punctuations = ['.', '!', '?']

    for text in transcript_text:
        # Skip empty text
        if not text:
            continue

        # If ending punctuation is found, add the text to the end of the current sentence and add to the sentences list
        if text[-1] in sentence_punctuations:
            current_sentence += text + "\n"
            sentences.append(current_sentence)
            current_sentence = ""
        else:
            # Add the text with a space after for the next text
            current_sentence += text + ""

    # Create output file with sentences
    new_file_name = "converted_" + file_name.split('.')[0] + ".txt"

    with open(new_file_name, 'w') as output_file:
        output_file.writelines(sentences)