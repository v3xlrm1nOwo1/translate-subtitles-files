import googletrans
import argparse
import sys
import re
import os


def translate(text, source_lang, destination_lang):
    translator = googletrans.Translator()
    translation = translator.translate(text=text, src=source_lang, dest=destination_lang)
    return translation


def vtt(text, source_lang, destination_lang):
    if re.search("^[a-zA-Z]", text) is not None and not text.startswith('WEBVTT'):
        result = translate(text, source_lang=source_lang, destination_lang=destination_lang)
        translation = result.text + '\n'
    else:
        translation = text
        
    return translation


def ass(text, source_lang, destination_lang):    
    if text.startswith('Dialogue'):
        text_ = text[::-1]
        a, b = text_.find(',,'), text_.find('}')
        
        if a < b or b == -1:
            right = text_[a: ][::-1]
            left = text_[: a][::-1]
             
        elif b < a or a == -1:
            right = text_[b: ][::-1]
            left = text_[: b][::-1]
            
        left = translate(left, source_lang=source_lang, destination_lang=destination_lang)
        text = right + left.text
        translation = text + '\n'
        
    else:
        translation = text
            
    return translation


def open_translation_file(file_path, file_extension, source_lang, destination_lang):
    translation = ''
    with open(file_path, 'r', encoding='utf-8') as f:

        if file_extension == 'vtt':
            for line in f.readlines():
                translation += vtt(line, source_lang, destination_lang)
                
        elif file_extension == 'ass':
            for line in f.readlines():
                translation += ass(line, source_lang, destination_lang)
    return translation
     
        
def write_translation_file(file_name, translation):
    file_name = f'Translation - {file_name}'
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(translation)
        return os.path.abspath(file_name)


def main():
    parser = argparse.ArgumentParser(prog='translated_subtitles', description="Translate Subtitles Files")
    parser.add_argument('-file_name', dest="file_name", help='Translation file name', required=True)
    parser.add_argument('-src_lang', dest="source_lang", help='Source language', required=True)
    parser.add_argument('-dest_lang', dest="destination_lang", help="Destination language", required=True)

    args = parser.parse_args()

    file_name = args.file_name
    source_lang = args.source_lang
    destination_lang = args.destination_lang
    
    languages = googletrans.LANGCODES
    source_lang = languages[source_lang]
    destination_lang = languages[destination_lang]
    
    file_extension = file_name[file_name.find('.')+1: ]
    file_path = os.path.abspath(file_name)
    
    translation = open_translation_file(file_path=file_path, file_extension=file_extension, source_lang=source_lang, destination_lang=destination_lang)
    translation_file = write_translation_file(file_name=file_name, translation=translation)
    print(f'> Translation file path: {translation_file}')
    sys.exit(0)

if __name__ == '__main__':
    main()
