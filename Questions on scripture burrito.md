Questions on [Alignment Scripture Burrito](https://docs.burrito.bible/en/v0.3.0/schema_docs/parascriptural-word_alignment.html) and the [example given](https://docs.burrito.bible/en/v0.3.0/examples/wordAlignment.html)

in the flavour 
- *autoAlignerVersion*: I assume that all the `suggestions` and `untranslated` in the draft can be considered auto-aligned. What should be the value given? A version number V2.0.0? Or a name, AutographaMT V2 ? or something like [software and user info](https://docs.burrito.bible/en/v0.3.0/schema_docs/software_and_user_info.html)
- *stopWord*: The value for this would always be true for our projects, right?
- *stemmer*: We can omit this property right?
- *manualAlignment -> user*: would this be a normal string or something like [software and user info](https://docs.burrito.bible/en/v0.3.0/schema_docs/software_and_user_info.html)
- *manualAlignment -> references*: As per my understanding, this would be very long list corresponding to all confirmed translations in the project. How can we specify start and end as intergers? The example looks like lid, we use refid as contextId in alignment json. But our start and end may not be at verse-level, but at word level. Or would this refer to the index number of segments array of alignment JSON? Then also those segments are verse/sentence level not word level.


in the meta
- generator would be vachan-api or vachan-engine right?


Should *idAuthorities* list all users of the project which can then be refered in manual alignment?

*identification*: this is where we can specify our project name right? 
- As we dont have concept of *revision* of project, I guess that can be omitted.
- I dont understand the value given in example for *primary*. It should be refering *idAuthorities*, right as given in the [schema](https://docs.burrito.bible/en/v0.3.0/schema_docs/identification.html)
