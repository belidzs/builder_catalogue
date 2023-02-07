# LEGO Coding Challenge

## Requirements
* Python >= 3.7
* `requests` library

Dependencies are managed using [Poetry](https://python-poetry.org/)

## Considerations

### First Look
At first I have tried to locate Swagger or OpenAPI schemas at conventional locations, but couldn't find any.

Since there was no API definition available to me which I could have used to generate the API client skeleton, I have coded a small abstraction layer on top of the `requests` calls myself to make the code easier to read and easier to test without mocking. This has eventually became the `api` module.

### Data Structure
I have also noticed that the data structure for a user's personal inventory was way too deep for my use case, so I have decided to flatten it out in a way that the quantities are stored per unique `(design ID, color)` combinations. 

Since these combinations are unique per user, I was able to use them as key values in a dictionary which held the available quantities for each design-color combo. As dictionary items can be inserted and queried in constant time, it is a perfect choice for storing this type of data.

When I started working on the second challenge it become clear that the project needed to be better organized, otherwise maintainability and legibility could in the long run. I've decided to refactor the project and adopt an object oriented approach which seemed like a good fit for the data I've been working with.

Since `NamedTuple` classes don't support inheritance without hacky workarounds, I've decided to go with the `dataclasses` package. Here I have faced a problem, since normally dataclasses are mutable and as such, they can't be used for hashing. This was an issue because I was planning to use some of these classes (such as `InventoryItem`) as dictionary keys, and only those data types can be used as dictionary keys which are hashable. To achieve this, I had to set `frozen` property to `True` on these classes to enforce immutability, which also made them hashable.

### Network Calls
Around line 30 in `main.py` I have made a decision to make a separate network call for each individual set to the API.

While in some cases this can be more costly than pulling all the sets in one go, storing it in memory, then processing it later (it definitely does now), if the set database ever grew larger, pulling all sets can quickly become infeasible.

A viable workaround would be to implement paging on the API side, so that only a single page should be processed at a time, but there were no need to call the API for each individual record.

### Optimization
I have realized that the total piece count is provided for both the individual sets and the users' inventories, so I could eliminate some of the unbuildable sets early just by comparing these two numbers.

### Project Structure
The project is divided into two reusable modules and the main entrypoint.

* The `api` module contains an abstraction over the remote service and it is also responsible for converting JSON responses into typed objects
* The `model` module contains the data model implemented as dataclasses
* The `main.py` file is the main entrypoint of the application. It also contains some implementation details for the challenges.
