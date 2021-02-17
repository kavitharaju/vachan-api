'''CRUD operations with more text processing and linguistics'''

import sqlalchemy
#pylint: disable=E0401
#pylint gives import error if relative import is not used. But app(uvicorn) doesn't accept it
import db_models
import schemas
from custom_exceptions import NotAvailableException, TypeException

def get_text_from_bible(source_name, ref_start:schemas.Reference=None, 
	ref_end:schemas.Reference=None):
	'''fetched text contents from bible_cleaned tables to be used for translations apps 
	or for model building.
	Output format: [(id, sentance), (id, sentance), ....]'''
    if source_name not in db_models.dynamicTables:
        raise NotAvailableException('%s not found in database.'%source_name)
    if not source_name.endswith('_bible'):
        raise TypeException('The operation is supported only on bible')
    model_cls = db_models.dynamicTables[source_name+'_cleaned']
    ref_id_start = ref_id_end = None
    if ref_start:
    	book = db_models.BibleBook.filter(db_models.BibleBook.bookCode == ref_start.bookCode).first()
    	if not book:
    		raise NotAvailableException("Book %s, not found in database"%ref_start.bookCode)
    	ref_id_start = book.bookId*1000000 + ref_start.chapter*1000 + ref_start.verseNumber
    if ref_end:
    	book = db_models.BibleBook.filter(db_models.BibleBook.bookCode == ref_end.bookCode).first()
    	if not book:
    		raise NotAvailableException("Book %s, not found in database"%ref_end.bookCode)
    	ref_id_end = book.bookId*1000000 + ref_end.chapter*1000 + ref_end.verseNumber
    if not ref_id_start:
    	ref_id_start = 0
    if not ref_id_end:
    	ref_id_end = 999999999
    query = db_.query(model_cls).filter(model_cls.refId >= ref_id_start,
    	model_cls.refId <= ref_id_end, db_models.active == True)
	return query.all()

def get_text_from_commentary(source_name):
	'''fetched text contents from commentary tables to be used for translations apps 
	or for model building
	Output format: [(id, sentance), (id, sentance), ....]'''
	return []

def get_text_from_footnotes(source_name):
	'''fetched text contents from bible_footnotes tables to be used for translations apps 
	or for model building
	Output format: [(id, sentance), (id, sentance), ....]'''
	return []

def get_translation_suggestion(word, context, src_lang, trg_lang):
	'''find the context based translation suggestions for a word.
	Makes use of the learned model(trie) for the lang pair, based on translation memory
	output format: [(translation1, score1), (translation2, score2), ...]'''
	return []

def align_low_resource(sent1, sent2, lang1, lang2):
	'''attempts to find word alignment for 2 sentences.
	Tries following methhods to form the alignment
	- word similarity(with Levistein, if same script)
	- word similarity(with Levistein after romanization, if different script)
	- refers previously done alignments/translation memory for the lang pair
	output format: [(s1w1, s1pos1, s2w1,s2pos1), (s1w1, s1pos1, s2w2,s2pos2)]'''
	return []

def tokenize(sent_list, punctuations=punctuations):
	'''Get single word tokens and their occurances from input sentence list'''
	unique_tokens = {}
	for sent in sent_list:
		clean_sent = sent[1]
		for punct in punctuations:
			clean_sent = clean_sent.replace(punct, " ")
		clean_sent = re.sub(clean_sent, "[\s\n\r]+", " ")
		words = clean_sent.split(" ")
		start = 0
		for word in words:
			offset = sent[1].find(word, start)
			start = offset+1
			if word not in unique_tokens:
				unique_tokens[word] = [(sent[0], offset)]
			else: 
				unique_tokens[word].append((sent[0], offset))
	return unique_tokens




