# create Inverted Index given wikipedia documents

from iir_code.createindex import main
from iir_code.inverted_index import InvertedIndex
from iir_code.service.file_manager import FileManager

file_manager = FileManager()
inverted_index = InvertedIndex()

main()
