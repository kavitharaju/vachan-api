# Scripture Buritto

1. [confidentiality](https://docs.burrito.bible/en/v0.2.0-beta/#confidentiality-options)
 The Confidentiality section includes three options, 1. unrestricted, 2. restricted, 3. private. May be we can use these values for role based access control on DB resources. some roles are also defined [here](https://docs.burrito.bible/en/v0.3.0-alpha.2/schema_docs/agency.html)
 

2. [Languages](https://docs.burrito.bible/en/v0.3.0-alpha.2/schema_docs/language.html#language)
 Here 2 letter language codes are used. In our database we use 3 letter codes. Either add 2 also in Db and use it for export, or switch to 2 letter codes entirely. Make sure our minority lanugages also have this 2 letter code representations.

3. [wordAlignment](https://docs.burrito.bible/en/v0.3.0-alpha.2/schema_docs/parascriptural-word_alignment.html#flavor-details-parascriptural-word-alignment)
Contains only meta data specifications
 
4. [textTranslation](https://docs.burrito.bible/en/v0.3.0-alpha.2/schema_docs/scripture-text_translation.html)
Contains only meta data specifications

5. [Ingredients](https://docs.burrito.bible/en/v0.3.0-alpha.2/schema_docs/ingredient.html#ingredient)
I assume it is in the ingredients file the actual content is goining to be, as the other file is only metadata. But we dont have any specification about this file. Are they supposed to be USFM files, for out use-case?


### Issues
1. The [json links](https://burrito.bible/schema/numbering_system.schema.json) on the documentation gets redirected to the home page. Where can I get the definitions of enums ?
