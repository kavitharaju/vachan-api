# API Refactoring


## Why API Refactoring ?

1. Poor code quality

	As we are working on adding features and fixing bugs on the V1 APIs we see lots of things which shouldn't be done the way it is, or could be done better. For example in many places in code, we form SQL queries by python string concatination. Because, these codes were written by different developers over a long time period and for a variety of needs, there are lots of inconsistancies, from naming of variables to implementation logic, which makes it hard to maintain. The code base includes (but uses or doesn't use) code portions written for the 
	* AgMT V1 APIs, 
	* The alignment app, 
	* AgMT V2 APIs (all the above mostly by Bijo)
	* VO apis (by Revant)
	All of which have been modified here and there, by Kavitha and Joel Johnson, as and when needs came.

2. In-consistancy in APIs

	Often it is very difficult to understand expected inputs, outputs and even fuctionality of an API or function. We usually read the code to understand what inputs be given, how it is processed and what are the values returned from an API. For example some APIs which were written earlier use form data input while recent ones use JSON data input. Also there is no consistancy in endpoint names, which makes it not possible to understand what an API does.

3. Use better coding practices

	Often several needs for standardizing the way we write code comes up as a need.
	* Use code linting
	* Use better libraries(like SQLAlchemy)

4. Lack of good documentation

	The lack of documentation has been a big problem. The attempt of creating a swagger documentation, with Savitha's help, wasn't very successful. Though she created one, it was not being effectively updated and maintained and more importantly not being used.

5. No tests

	Often the APIs were developed by the UI developer itself and were only tested using the UI manually. There were no proper test cases created(neither for UI nor for API) at the time of implementation. An Attempt was made to add tests for these APIs afterwards, again with Savitha's and Joel Johnson's help. But, it wasn't effective either. Though tests were written, it hardly check for the possible flaws, and we are often finding them when issues comes up from user end. The problem of tests not being defined during the definition and implementaion of APIs is very evident.

6. Database changes

	The whole DB design was once reviewed and revised to solve many of the issues it had and also to make it more standardized and scalable. Sticking to those design decisions, now we see
	* some issues that were not fixed at that time(like an un-necessary translation_projects_lookup table which does no good but just increases the number of joins required)
	* some principles then decided upon, are not followed when new contents were added to DB (naming tables and fields, how tables are connected together etc)
	* some changes we feel are required in newly added data(bookcodes should be JSON array and not comma separated string, which column should have the NOT NULL constaint etc)

## Why Vachan-API Version 2

* Each of the above listed issue is very important and needs to be fixed as early as possible. But each requires a complete code review and revisal/rewritting. So it is better to do all at once in one go. Other wise it would result in unnecessay extra work, like if we first refine all the tests and documentation and then later change the APIs, all effort spend on tests and docs are wasted and it will have to be redone.

* If we could stick to the APIs and revise only the underlying implementaion, then the clients wouldn't be affected with the changes. But the inputs, endpoints, outputs all need to be 
standardized. 

It is important to have the V1 APIs as it is, as currently 3 clients(AgMT, VO and VO App) are using them. So we can have a better parallel version 2 and let the clients switch versions on their conviniance.

A rough time estimate for carrying out this process would be as follows: **6 Months** for the design, development and testing of V2, and another **6 months** for allowing the client projects to transition to the newer APIs, until which the vachan-api V1 should be maintained and supported.


## API Endpoint Design for vachan-api Version 2

### Main Principles followed 
* Uniformity
	> Attempted to bring uniformity in how each resource is 
	> * stored in Database
	> * accessed via GET, PUT and POST methods
	> * given end-point names(using plurals, following same pattern etc) and input-output objects names and structure
* Scalability
	> Considers new data and processing requiremnts that would come in future
	> * Dynamically creating new tables
	> * Provision to add new contents and edit contents in all tables
	> * Keeping flexibility of schema with JSON objects in places where variation can be expected
* Human readability/understandability of input output values
	> have tried to avoid the use of id values as much as possible in inputs and outputs.
	> Uses language Codes, book Codes, source names etc in place of number ids we used in V1
* Better Error Messages
	> * use consistent error message patterns thought out the App
	> * use http_status codes to indicate type of error
* Data validation
	> Make use of the input and output datatype validation provisions in the Fast API as much as possible
	> * specifies expected datatype like int, string etc
	> * defines patterns for special cases like, language code, book code, source name etc
	> * defines JSON strutures of Body parameters as well as output objects
* Documentation
	> Using FastApi we can generate swagger and redoc documentation automatically if necessary steps are followed while writing codes.
	> * using meaningful function names
	> * adding description for every API as comments in the required format
	> * defining and specifying all inputs and output format for every API 
	> Following these practices, we will have good quality API documentaion which will become very useful for our API clients, especially if we expect external clients
