'''Defines all API endpoints for the web server app'''

from typing import List
from fastapi import FastAPI, Query, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import crud
import db_models
import schemas
from logger import log
from database import SessionLocal, engine
from custom_exceptions import GenericException, DatabaseException
from custom_exceptions import NotAvailableException, AlreadyExistsException, TypeException



app = FastAPI()

######### Error Handling ##############

@app.exception_handler(Exception)
async def any_exception_handler(request, exc: Exception):
    '''logs and returns error details'''
    log.error("Request URL:%s %s,  from : %s",
        request.method ,request.url.path, request.client.host)
    log.exception("%s: %s",'Error', str(exc))
    if hasattr(exc, "status_code"):
        status_code=exc.status_code
    else:
        status_code = 500
    return JSONResponse(
        status_code =status_code,
        content={"error": 'Error', "details" : str(exc)},
    )

@app.exception_handler(GenericException)
async def generic_exception_handler(request, exc: GenericException):
    '''logs and returns error details'''
    log.error("Request URL:%s %s,  from : %s",
        request.method ,request.url.path, request.client.host)
    log.error("%s: %s",exc.name, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.name, "details" : exc.detail},
    )

@app.exception_handler(DatabaseException)
async def db_exception_handler(request, exc: DatabaseException):
    '''logs and returns error details'''
    log.error("Request URL:%s %s,  from : %s",
        request.method ,request.url.path, request.client.host)
    log.error("%s: %s",exc.name, exc.logging_info)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.name, "details" : exc.detail},
    )


@app.exception_handler(NotAvailableException)
async def na_exception_handler(request, exc: NotAvailableException):
    '''logs and returns error details'''
    log.error("Request URL:%s %s,  from : %s",
        request.method ,request.url.path, request.client.host)
    log.error("%s: %s",exc.name, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.name, "details" : exc.detail},
    )


@app.exception_handler(AlreadyExistsException)
async def exists_exception_handler(request, exc: AlreadyExistsException):
    '''logs and returns error details'''
    log.error("Request URL:%s %s,  from : %s",
        request.method ,request.url.path, request.client.host)
    log.error("%s: %s",exc.name, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.name, "details" : exc.detail},
    )

@app.exception_handler(TypeException)
async def type_exception_handler(request, exc: TypeException):
    '''logs and returns error details'''
    log.error("Request URL:%s %s,  from : %s",
        request.method ,request.url.path, request.client.host)
    log.error("%s: %s",exc.name, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.name, "details" : exc.detail},
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    '''logs and returns error details'''
    log.error("Request URL:%s %s, from : %s",
        request.method ,request.url.path, request.client.host)
    log.error("Http Error: %s", exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTP Error", "details": str(exc.detail)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    '''logs and returns error details'''
    log.error("Request URL:%s %s, from : %s",
        request.method ,request.url.path, request.client.host)
    log.error("Input Validation Error: %s", str(exc))
    return JSONResponse(
        status_code=422,
        content={"error": "Input Validation Error" ,"details": str(exc).replace("\n", ". ")}
    )
######################################################

def get_db():
    '''To start a DB connection(session)'''
    db_ = SessionLocal()
    try:
        yield db_
    finally:
        pass
        # db_.close()

db_models.map_all_dynamic_tables(db_= next(get_db()))
db_models.Base.metadata.create_all(bind=engine)


@app.get('/', response_model=schemas.NormalResponse, status_code=200)
def test():
    '''tests if app is running and the DB connection'''
    return {"message": "App is up and running"}



##### Content types #####

@app.get('/v2/contents', response_model=List[schemas.ContentType],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}},  status_code=200,
    tags=["Contents Types"])
def get_contents(content_type: str = Query(None), skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0), db_: Session = Depends(get_db)):
    '''fetches all the contents types supported and their details
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_contents')
    log.debug('contentType:%s, skip: %s, limit: %s',content_type, skip, limit)
    try:
        return crud.get_content_types(db_, content_type, skip, limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_contents')
        raise DatabaseException(exe) from exe
    except Exception as exe:
        log.exception('Error in get_contents')
        raise GenericException(str(exe)) from exe

@app.post('/v2/contents', response_model=schemas.ContentTypeUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Contents Types"])
def add_contents(content: schemas.ContentTypeCreate, db_: Session = Depends(get_db)):
    ''' Creates a new content type.
    Additional operations required:
        1. Add corresponding table creation functions to Database.
        2. Define input, output resources and all required APIs to handle this content'''
    log.info('In add_contents')
    log.debug('content: %s',content)
    try:
        if len(crud.get_content_types(db_, content.contentType)) > 0:
            raise AlreadyExistsException("%s already present"%(content.contentType))
        return {'message': "Content type created successfully",
        "data": crud.create_content_type(db_=db_, content=content)}
    except SQLAlchemyError as exe:
        log.exception('Error in add_contents')
        raise DatabaseException(exe) from exe
    except AlreadyExistsException as exe:
        log.exception('Error in add_contents')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in add_contents')
        raise GenericException(str(exe)) from exe

#################

##### languages #####

@app.get('/v2/languages',
    response_model=List[schemas.LanguageResponse],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Languages"])
def get_language(language_code : schemas.LangCodePattern = Query(None),
    language_name: str = Query(None),
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=0), db_: Session = Depends(get_db)):
    '''fetches all the languages supported in the DB, their code and other details.
    if query parameter, langauge_code is provided, returns details of that language if pressent
    and 404, if not found
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_language')
    log.debug('langauge_code:%s, language_name: %s, skip: %s, limit: %s',
        language_code, language_name, skip, limit)
    try:
        return crud.get_languages(db_, language_code, language_name, skip = skip, limit = limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_language')
        raise DatabaseException(exe) from exe
    except Exception as exe:
        log.exception('Error in get_language')
        raise GenericException(str(exe)) from exe

@app.post('/v2/languages', response_model=schemas.LanguageUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Languages"])
def add_language(lang_obj : schemas.LanguageCreate = Body(...), db_: Session = Depends(get_db)):
    ''' Creates a new language'''
    log.info('In add_language')
    log.debug('lang_obj: %s',lang_obj)
    try:
        if len(crud.get_languages(db_, language_code = lang_obj.code)) > 0:
            raise AlreadyExistsException("%s already present"%(lang_obj.code))
        return {'message': "Language created successfully",
        "data": crud.create_language(db_=db_, lang=lang_obj)}
    except SQLAlchemyError as exe:
        log.exception('Error in add_language')
        raise DatabaseException(exe) from exe
    except AlreadyExistsException as exe:
        log.exception('Error in add_language')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in add_language')
        raise GenericException(str(exe)) from exe

@app.put('/v2/languages', response_model=schemas.LanguageUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 404: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Languages"])
def edit_language(lang_obj: schemas.LanguageEdit = Body(...), db_: Session = Depends(get_db)):
    ''' Changes one or more fields of language'''
    log.info('In edit_language')
    log.debug('lang_obj: %s',lang_obj)
    try:
        if len(crud.get_languages(db_, language_id = lang_obj.languageId)) == 0:
            raise NotAvailableException("Language id %s not found"%(lang_obj.languageId))
        return {'message': "Language edited successfully",
        "data": crud.update_language(db_=db_, lang=lang_obj)}
    except SQLAlchemyError as exe:
        log.exception('Error in edit_language')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in edit_language')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in edit_language')
        raise GenericException(str(exe)) from exe

# ################################


##### Version #####

@app.get('/v2/versions',
    response_model=List[schemas.VersionResponse],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Versions"])
def get_version(version_abbreviation : schemas.VersionPattern = Query(None), #pylint: disable=too-many-arguments
    version_name: str = Query(None), revision : int = Query(None),
    metadata: schemas.MetaDataPattern = Query(None),
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=0), db_: Session = Depends(get_db)):
    '''Fetches all versions and their details.
    If param versionAbbreviation is present, returns details of that version if pressent
    and 404, if not found
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_version')
    log.debug('version_abbreviation:%s, skip: %s, limit: %s',
        version_abbreviation, skip, limit)
    try:
        return crud.get_versions(db_, version_abbreviation,
            version_name, revision, metadata, skip = skip, limit = limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_version')
        raise DatabaseException(exe) from exe
    except Exception as exe:
        log.exception('Error in get_version')
        raise GenericException(str(exe)) from exe

@app.post('/v2/versions', response_model=schemas.VersionUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Versions"])
def add_version(version_obj : schemas.VersionCreate = Body(...),
    db_: Session = Depends(get_db)):
    ''' Creates a new version '''
    log.info('In add_version')
    log.debug('version_obj: %s',version_obj)
    try:
        if not version_obj.revision:
            version_obj.revision = 1
        if len(crud.get_versions(db_, version_obj.versionAbbreviation,
            revision =version_obj.revision)) > 0:
            raise AlreadyExistsException("%s, %s already present"%(
                version_obj.versionAbbreviation, version_obj.revision))
        return {'message': "Version created successfully",
        "data": crud.create_version(db_=db_, version=version_obj)}
    except SQLAlchemyError as exe:
        log.exception('Error in add_version')
        raise DatabaseException(exe) from exe
    except AlreadyExistsException as exe:
        log.exception('Error in add_version')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in add_version')
        raise GenericException(str(exe)) from exe

@app.put('/v2/versions', response_model=schemas.VersionUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 404: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Versions"])
def edit_version(ver_obj: schemas.VersionEdit = Body(...), db_: Session = Depends(get_db)):
    ''' Changes one or more fields of version types table'''
    log.info('In edit_version')
    log.debug('ver_obj: %s',ver_obj)
    try:
        if len(crud.get_versions(db_, version_id = ver_obj.versionId)) == 0:
            raise NotAvailableException("Version id %s not found"%(ver_obj.versionId))
        return {'message': "Version edited successfully",
        "data": crud.update_version(db_=db_, version=ver_obj)}
    except SQLAlchemyError as exe:
        log.exception('Error in edit_version')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in edit_version')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in edit_version')
        raise GenericException(str(exe)) from exe


# ##### Source #####
@app.get('/v2/sources',
    response_model=List[schemas.SourceResponse],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Sources"])
def get_source(content_type: str = None, version_abbreviation: schemas.VersionPattern = None, #pylint: disable=too-many-arguments
    revision: int = None, language_code: schemas.LangCodePattern =None,
    metadata: schemas.MetaDataPattern = Query(None), active: bool = True,
    latest_revision: bool = True,
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=0), db_: Session = Depends(get_db)):
    '''Fetches all sources and their details.
    If one or more optional params are present, returns a filtered result if pressent
    and [], if not found.
    If revision is not explictly set or latest_revision is not set to False,
    then only the highest number revision from the avaliable list in each version would be returned.
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_source')
    log.debug('contentType:%s, versionAbbreviation: %s, revision: %s,\
        languageCode: %s, metadata: %s, latest_revision: %s, active: %s, skip: %s, limit: %s',
        content_type, version_abbreviation, revision, language_code, metadata, latest_revision,
        active, skip, limit)
    try:
        return crud.get_sources(db_, content_type, version_abbreviation, revision,
            language_code, metadata, latest_revision = latest_revision, active = active,
            skip = skip, limit = limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_source')
        raise DatabaseException(exe) from exe
    except Exception as exe:
        log.exception('Error in get_source')
        raise GenericException(str(exe)) from exe

@app.post('/v2/sources', response_model=schemas.SourceUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Sources"])
def add_source(source_obj : schemas.SourceCreate = Body(...),
    db_: Session = Depends(get_db)):
    ''' Creates a new source entry in sources table.
    Also creates all associtated tables for the content type. Not yet.
    '''
    log.info('In add_source')
    log.debug('source_obj: %s',source_obj)
    try:
        if not source_obj.revision:
            source_obj.revision = 1
        table_name = source_obj.language + "_" + source_obj.version + "_" +\
        source_obj.revision + "_" + source_obj.contentType
        if len(crud.get_sources(db_, table_name = table_name)) > 0:
            raise AlreadyExistsException("%s already present"%table_name)
        return {'message': "Source created successfully",
        "data": crud.create_source(db_=db_, source=source_obj, table_name=table_name,
            user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in add_source')
        raise DatabaseException(exe) from exe
    except AlreadyExistsException as exe:
        log.exception('Error in add_source')
        raise exe from exe
    except NotAvailableException as exe:
        log.exception('Error in add_source')
        raise exe from exe
    except GenericException as exe:
        log.exception('Error in add_source')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in add_source')
        raise GenericException(str(exe)) from exe

@app.put('/v2/sources', response_model=schemas.SourceUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 404: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Sources"])
def edit_source(source_obj: schemas.SourceEdit = Body(...), db_: Session = Depends(get_db)):
    ''' Changes one or more fields of source '''
    log.info('In edit_source')
    log.debug('source_obj: %s',source_obj)
    try:
        if len(crud.get_sources(db_, table_name = source_obj.sourceName)) == 0:
            raise NotAvailableException("Source %s not found"%(source_obj.sourceName))
        return {'message': "Source edited successfully",
        "data": crud.update_source(db_=db_, source=source_obj, user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in edit_source')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in edit_source')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in edit_source')
        raise GenericException(str(exe)) from exe

# # #################

# ############ Bible Books ##########


@app.get('/v2/lookup/bible/books',
    response_model=List[schemas.BibleBook],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Lookups"])
def get_bible_book(book_id: int = None, book_code: schemas.BookCodePattern = None, #pylint: disable=too-many-arguments
    book_name: str = None,
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=0), db_: Session = Depends(get_db)):
    ''' returns the list of book ids, codes and names.
    If any of the query params are provided the details of corresponding book
    will be returned
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_bible_book')
    log.debug('book_id: %s, book_code: %s, book_name: %s, skip: %s, limit: %s',
        book_id, book_code, book_name, skip, limit)
    try:
        return crud.get_bible_books(db_, book_id, book_code, book_name,
            skip = skip, limit = limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_bible_book')
        raise DatabaseException(exe) from exe
    except Exception as exe:
        log.exception('Error in get_bible_book')
        raise GenericException(str(exe)) from exe



# #### Bible #######


@app.post('/v2/bibles/{source_name}/books', response_model=schemas.BibleBookUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Bibles"])
def add_bible_book(source_name : schemas.TableNamePattern,
    books: List[schemas.BibleBookUpload] = Body(...), db_: Session = Depends(get_db)):
    '''Uploads a bible book. It update 2 tables: ..._bible, .._bible_cleaned'''
    log.info('In add_bible_book')
    log.debug('source_name: %s, books: %s',source_name, books)
    return {'message': "Bible books uploaded and processed successfully",
    "data": crud.upload_bible_books(db_=db_, source_name=source_name,
        books=books, user_id=None)}


@app.put('/v2/bibles/{source_name}/books', response_model=schemas.BibleBookUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 404: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Bibles"])
def edit_bible_book(source_name: schemas.TableNamePattern,
    books: List[schemas.BibleBookEdit] = Body(...), db_: Session = Depends(get_db)):
    '''Either changes the active status or Changes both usfm and json fields of bible book.
    In the second case, contents of the respective bible_clean and bible_tokens tables
    should be deleted and new data added.
    two fields are mandatory as usfm and json are interdependant'''
    log.info('In edit_bible_book')
    log.debug('source_name: %s, books: %s',source_name, books)
    return {'message': "Bible books updated successfully",
        "data": crud.update_bible_books(db_=db_, source_name=source_name,
        books=books, user_id=None)}

@app.get('/v2/bibles/{source_name}/books',
    response_model=List[schemas.BibleBookContent],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Bibles"])
def get_available_bible_book(source_name: schemas.TableNamePattern, #pylint: disable=too-many-arguments
    book_code: schemas.BookCodePattern=None, content_type: schemas.BookContentType=None,
    versification: bool=False, active: bool=True,
    skip: int=Query(0, ge=0), limit: int=Query(100, ge=0), db_: Session=Depends(get_db)):
    '''Fetches all the books available(has been uploaded) in the specified bible
    * returns all available(uploaded) books without bookCode and contentType
    * returns above details of one book: if bookCode is specified
    * versification can be set to true if the book structure is required(chapters in a book and
    verse numbers in each chapter)
    * returns the JSON, USFM and/or Audio contents also: if contentType is given
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_available_bible_book')
    log.debug('source_name: %s, book_code: %s, contentType: %s, versification:%s,\
        active:%s, skip: %s, limit: %s',
        source_name, book_code, content_type, versification, active, skip, limit)
    try:
        return crud.get_available_bible_books(db_, source_name, book_code, content_type,
            versification, active=active, skip = skip, limit = limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_available_bible_book')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in get_available_bible_book')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in get_available_bible_book')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in get_available_bible_book')
        raise GenericException(str(exe)) from exe


@app.get('/v2/bibles/{source_name}/verses',
    response_model=List[schemas.BibleVerse],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Bibles"])
def get_bible_verse(source_name: schemas.TableNamePattern, #pylint: disable=too-many-arguments
    book_code: schemas.BookCodePattern=None,  chapter: int=None, verse: int=None,
    last_verse: int=None, search_phrase: str=None, active: bool=True,
    skip: int=Query(0, ge=0), limit: int=Query(100, ge=0), db_: Session=Depends(get_db)):
    ''' Fetches the cleaned contents of bible, within a verse range, if specified.
    This API could be used for fetching,
     * all verses of a source : with out giving any query params.
     * all verses of a book: with only book_code
     * all verses of a chapter: with book_code and chapter
     * one verse: with bookCode, chapter and verse(without lastVerse).
     * any range of verses within a chapter: using verse and lastVerse appropriately
     * search for a query phrase in a bible and get matching verses: using search_phrase
     * skip=n: skips the first n objects in return list
     * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_bible_verse')
    log.debug('source_name: %s, book_code: %s, chapter: %s, verse:%s, last_verse:%s,\
        search_phrase:%s, active:%s, skip: %s, limit: %s',
        source_name, book_code, chapter, verse, last_verse, search_phrase, active, skip, limit)
    try:
        return crud.get_bible_verses(db_, source_name, book_code, chapter, verse, last_verse,
            search_phrase, active=active, skip = skip, limit = limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_bible_verse')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in get_bible_verse')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in get_bible_verse')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in get_bible_verse')
        raise GenericException(str(exe)) from exe


# # ########### Audio bible ###################

@app.post('/v2/bibles/{source_name}/audios', response_model=schemas.BibleBookUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Bibles"])
def add_audio_bible(source_name : schemas.TableNamePattern,
    audios: List[schemas.AudioBibleUpload] = Body(...), db_: Session = Depends(get_db)):
    '''uploads audio(links and related info, not files) for a bible'''
    log.info('In add_audio_bible')
    log.debug('source_name: %s, audios: %s',source_name, audios)
    return {'message': "Bible audios uploaded and processed successfully",
        "data": crud.upload_bible_audios(db_=db_, source_name=source_name,
        audios=audios, user_id=None)}


@app.put('/v2/bibles/{source_name}/audios', response_model=schemas.BibleBookUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 404: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Bibles"])
def edit_audio_bible(source_name: schemas.TableNamePattern,
    audios: List[schemas.AudioBibleEdit] = Body(...), db_: Session = Depends(get_db)):
    ''' Changes the mentioned fields of audio bible row.
    Name is used to identify row and cannot be changed'''
    log.info('In edit_audio_bible')
    log.debug('source_name: %s, audios: %s',source_name, audios)
    return {'message': "Bible audios uploaded and processed successfully",
        "data": crud.update_bible_audios(db_=db_, source_name=source_name,
        audios=audios, user_id=None)}

# # ##### Commentary #####

@app.get('/v2/commentaries/{source_name}',
    response_model=List[schemas.CommentaryResponse],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Commentaries"])
def get_commentary(source_name: schemas.TableNamePattern, book_code: schemas.BookCodePattern = None, #pylint: disable=too-many-arguments
    chapter: int = Query(None, ge=-1), verse: int = Query(None, ge=-1),
    last_verse: int = Query(None, ge=-1), active: bool = True,
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=0), db_: Session = Depends(get_db)):
    '''Fetches commentries under the specified source.
    Using the params bookCode, chapter, and verse the result set can be filtered as per need,
    like in the /v2/bibles/{sourceName}/verses API
    * Value 0 for verse and last_verse indicate chapter introduction and -1 indicate 
    chapter epilogue.
    * Similarly 0 for chapter means book introduction and -1 for chapter means book epilogue
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_commentary')
    log.debug('source_name: %s, book_code: %s, chapter: %s, verse:%s,\
        last_verse:%s, skip: %s, limit: %s',
        source_name, book_code, chapter, verse, last_verse, skip, limit)
    try:
        return crud.get_commentaries(db_, source_name, book_code, chapter, verse, last_verse,
            active=active, skip = skip, limit = limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_commentary')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in get_commentary')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in get_commentary')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in get_commentary')
        raise GenericException(str(exe)) from exe

@app.post('/v2/commentaries/{source_name}', response_model=schemas.CommentaryUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Commentaries"])
def add_commentary(source_name : schemas.TableNamePattern,
    commentaries: List[schemas.CommentaryCreate] = Body(...), db_: Session = Depends(get_db)):
    '''Uploads a list of commentaries.
    * Duplicate commentries are allowed for same verses,
    unless they have excalty same values for reference range.
    That is, if commentary is present for (gen, 1, 1-10) and
    new entries are made for (gen, 1, 1-20)
    or (gen, 1, 5-10), they will be accepted and added to DB
    * Value 0 for verse and last_verse indicate chapter introduction and
    -1 indicate chapter epilogue.
    * Similarly 0 for chapter means book introduction and -1 for chapter means book epilogue,
    verses fields can be null in these cases'''
    log.info('In add_commentary')
    log.debug('source_name: %s, commentaries: %s',source_name, commentaries)
    try:
        return {'message': "Commentaries added successfully",
        "data": crud.upload_commentaries(db_=db_, source_name=source_name,
            commentaries=commentaries, user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in add_commentary')
        raise DatabaseException(exe) from exe
    except AlreadyExistsException as exe:
        log.exception('Error in add_commentary')
        raise exe from exe
    except NotAvailableException as exe:
        log.exception('Error in add_commentary')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in add_commentary')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in add_commentary')
        raise GenericException(str(exe)) from exe


@app.put('/v2/commentaries/{source_name}', response_model=schemas.CommentaryUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 404: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Commentaries"])
def edit_commentary(source_name: schemas.TableNamePattern,
    commentaries: List[schemas.CommentaryEdit] = Body(...), db_: Session = Depends(get_db)):
    ''' Changes the commentary field to the given value in the row selected using
    book, chapter, verseStart and verseEnd values'''
    log.info('In edit_commentary')
    log.debug('source_name: %s, commentaries: %s',source_name, commentaries)
    try:
        return {'message': "Commentaries updated successfully",
        "data": crud.update_commentaries(db_=db_, source_name=source_name,
            commentaries=commentaries, user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in edit_commentary')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in edit_commentary')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in edit_commentary')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in edit_commentary')
        raise GenericException(str(exe)) from exe


# # ########### Dictionary ###################

@app.get('/v2/dictionaries/{source_name}',
    response_model=List[schemas.DictionaryWordResponse],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Dictionaries"])
def get_dictionary_word(source_name: schemas.TableNamePattern, search_word: str = None, #pylint: disable=too-many-arguments
    exact_match: bool=False, word_list_only: bool=False, details:str=None, active: bool=True,
    skip: int=Query(0, ge=0), limit: int=Query(100, ge=0), db_: Session=Depends(get_db)):
    '''fetches list of dictionary words and all available details about them.
    Using the searchIndex appropriately, it is possible to get
    * All words starting with a letter
    * All words starting with a substring
    * An exact word search, giving the whole word and setting exactMatch to True
    * Based on any key value pair in details, which should be specified as a dict/JSON like string
    * By setting the wordListOnly flag to True, only the words would be inlcuded
     in the return object, without the details
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_dictionary_word')
    log.debug('source_name: %s, search_word: %s, exact_match: %s, word_list_only:%s, details:%s\
        skip: %s, limit: %s', source_name, search_word, exact_match, word_list_only, details,
        skip, limit)
    try:
        return crud.get_dictionary_words(db_, source_name, search_word, exact_match=exact_match,
            word_list_only=word_list_only, details=details, active=active, skip=skip, limit=limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_dictionary_word')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in get_dictionary_word')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in get_dictionary_word')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in get_dictionary_word')
        raise GenericException(str(exe)) from exe


@app.post('/v2/dictionaries/{source_name}', response_model=schemas.DictionaryUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Dictionaries"])
def add_dictionary_word(source_name : schemas.TableNamePattern,
    dictionary_words: List[schemas.DictionaryWordCreate] = Body(...),
    db_: Session = Depends(get_db)):
    ''' uploads dictionay words and their details. 'Details' should be of JSON datatype and  have
    all the additional info we have for each word, as key-value pairs'''
    log.info('In add_dictionary_word')
    log.debug('source_name: %s, dictionary_words: %s',source_name, dictionary_words)
    try:
        return {'message': "Dictionary words added successfully",
        "data": crud.upload_dictionary_words(db_=db_, source_name=source_name,
            dictionary_words=dictionary_words, user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in add_dictionary_word')
        raise DatabaseException(exe) from exe
    except AlreadyExistsException as exe:
        log.exception('Error in add_dictionary_word')
        raise exe from exe
    except NotAvailableException as exe:
        log.exception('Error in add_dictionary_word')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in add_dictionary_word')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in add_dictionary_word')
        raise GenericException(str(exe)) from exe


@app.put('/v2/dictionaries/{source_name}', response_model=schemas.DictionaryUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 404: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Dictionaries"])
def edit_dictionary_word(source_name: schemas.TableNamePattern,
    dictionary_words: List[schemas.DictionaryWordEdit] = Body(...),
    db_: Session = Depends(get_db)):
    '''Updates the given fields mentioned in details object, of the specifed word'''
    log.info('In edit_dictionary_word')
    log.debug('source_name: %s, dictionary_words: %s',source_name, dictionary_words)
    try:
        return {'message': "Dictionary words updated successfully",
        "data": crud.update_dictionary_words(db_=db_, source_name=source_name,
            dictionary_words=dictionary_words, user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in edit_dictionary_word')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in edit_dictionary_word')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in edit_dictionary_word')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in edit_dictionary_word')
        raise GenericException(str(exe)) from exe
# # ###########################################

# # ########### Infographic ###################

@app.get('/v2/infographics/{source_name}',
    response_model=List[schemas.InfographicResponse],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Infographics"])
def get_infographic(source_name: schemas.TableNamePattern, book_code: schemas.BookCodePattern=None, #pylint: disable=too-many-arguments
    title: str=None, active: bool=True,
    skip: int=Query(0, ge=0), limit: int=Query(100, ge=0), db_: Session=Depends(get_db)):
    '''Fetches the infographics. Can use, bookCode and/or title to filter the results
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_infographic')
    log.debug('source_name: %s, book_code: %s skip: %s, limit: %s',
        source_name, book_code, skip, limit)
    try:
        return crud.get_infographics(db_, source_name, book_code, title,
        active=active, skip = skip, limit = limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_infographic')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in get_infographic')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in get_infographic')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in get_infographic')
        raise GenericException(str(exe)) from exe

@app.post('/v2/infographics/{source_name}', response_model=schemas.InfographicUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Infographics"])
def add_infographics(source_name : schemas.TableNamePattern,
    infographics: List[schemas.InfographicCreate] = Body(...), db_: Session = Depends(get_db)):
    '''Uploads a list of infograhics.'''
    log.info('In add_infographics')
    log.debug('source_name: %s, infographics: %s',source_name, infographics)
    try:
        return {'message': "Infographics added successfully",
        "data": crud.upload_infographics(db_=db_, source_name=source_name,
            infographics=infographics, user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in add_infographics')
        raise DatabaseException(exe) from exe
    except AlreadyExistsException as exe:
        log.exception('Error in add_infographics')
        raise exe from exe
    except NotAvailableException as exe:
        log.exception('Error in add_infographics')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in add_infographics')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in add_infographics')
        raise GenericException(str(exe)) from exe

@app.put('/v2/infographics/{source_name}', response_model=schemas.InfographicUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 404: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Infographics"])
def edit_infographics(source_name: schemas.TableNamePattern,
    infographics: List[schemas.InfographicEdit] = Body(...),
    db_: Session = Depends(get_db)):
    ''' Changes the infographic link to the given value in the row selected using
    book and title'''
    log.info('In edit_infographics')
    log.debug('source_name: %s, infographics: %s',source_name, infographics)
    try:
        return {'message': "Infographics updated successfully",
        "data": crud.update_infographics(db_=db_, source_name=source_name,
            infographics=infographics, user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in edit_infographics')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in edit_infographics')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in edit_infographics')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in edit_infographics')
        raise GenericException(str(exe)) from exe
# # ###########################################


# # ########### bible videos ###################

@app.get('/v2/biblevideos/{source_name}',
    response_model=List[schemas.BibleVideo],
    responses={502: {"model": schemas.ErrorResponse},
    422: {"model": schemas.ErrorResponse}}, status_code=200, tags=["Bible Videos"])
def get_bible_video(source_name: schemas.TableNamePattern, book_code: schemas.BookCodePattern=None, #pylint: disable=too-many-arguments
    title: str=None, theme: str=None, active: bool=True,
    skip: int=Query(0, ge=0), limit: int=Query(100, ge=0), db_: Session=Depends(get_db)):
    '''Fetches the Bible video details and URL.
    Can use the optional query params book, title and theme to filter the results
    * skip=n: skips the first n objects in return list
    * limit=n: limits the no. of items to be returned to n'''
    log.info('In get_bible_video')
    log.debug('source_name: %s, book_code: %s, title: %s, theme: %s, skip: %s, limit: %s',
        source_name, book_code, title, theme, skip, limit)
    try:
        return crud.get_bible_videos(db_, source_name, book_code, title, theme, active,
        skip=skip, limit=limit)
    except SQLAlchemyError as exe:
        log.exception('Error in get_bible_video')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in get_bible_video')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in get_bible_video')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in get_bible_video')
        raise GenericException(str(exe)) from exe

@app.post('/v2/biblevideos/{source_name}', response_model=schemas.BibleVideoUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 409: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Bible Videos"])
def add_bible_video(source_name : schemas.TableNamePattern,
    videos: List[schemas.BibleVideoUpload] = Body(...), db_: Session = Depends(get_db)):
    '''Uploads a list of bible video links and details.'''
    log.info('In add_bible_video')
    log.debug('source_name: %s, videos: %s',source_name, videos)
    try:
        return {'message': "Bible videos added successfully",
        "data": crud.upload_bible_videos(db_=db_, source_name=source_name,
            videos=videos, user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in add_bible_video')
        raise DatabaseException(exe) from exe
    except AlreadyExistsException as exe:
        log.exception('Error in add_bible_video')
        raise exe from exe
    except NotAvailableException as exe:
        log.exception('Error in add_bible_video')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in add_bible_video')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in add_bible_video')
        raise GenericException(str(exe)) from exe


@app.put('/v2/biblevideos/{source_name}', response_model=schemas.BibleVideoUpdateResponse,
    responses={502: {"model": schemas.ErrorResponse}, \
    422: {"model": schemas.ErrorResponse}, 404: {"model": schemas.ErrorResponse}},
    status_code=201, tags=["Bible Videos"])
def edit_bible_video(source_name: schemas.TableNamePattern,
    videos: List[schemas.BibleVideoEdit] = Body(...),
    db_: Session = Depends(get_db)):
    ''' Changes the selected rows of bible videos table. each row identified by '''
    log.info('In edit_bible_video')
    log.debug('source_name: %s, videos: %s',source_name, videos)
    try:
        return {'message': "Bible videos updated successfully",
        "data": crud.update_bible_videos(db_=db_, source_name=source_name,
            videos=videos, user_id=None)}
    except SQLAlchemyError as exe:
        log.exception('Error in edit_bible_video')
        raise DatabaseException(exe) from exe
    except NotAvailableException as exe:
        log.exception('Error in edit_bible_video')
        raise exe from exe
    except TypeException as exe:
        log.exception('Error in edit_bible_video')
        raise exe from exe
    except Exception as exe:
        log.exception('Error in edit_bible_video')
        raise GenericException(str(exe)) from exe
# # ###########################################
