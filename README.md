# LEGO

## Requirements
* Python >= 3.7
* requests library

Dependencies are managed using [Poetry](https://python-poetry.org/)

## Considerations

### First look
At first I have tried to locate Swagger or OpenAPI schemas at conventional locations, but couldn't find any.

Since there was no API definition available to me which I could have used to generate the API client skeleton, I have coded a small abstraction layer on top of the `requests` calls myself to make the code easier to read and easier to test without mocking.

I have realized early that the total piece count is provided for both the sets and the user inventories, so I could very easily eliminate those sets which were made up of more bricks than the user had in total.

### Data structure

I have also noticed that the data structure for a user's personal inventory was way too deep for my use case, so I have decided to flatten it out in a way that the quantities are stored per unique `(design ID, color)` combinations. 

Since these combinations are unique per user, I was able to use them as key values in a dictionary which held the brick types and the available quantities. Dictionary items can be inserted and queried in constant time, so it is a perfect choice for storing this type of data.

When I started working on the second challenge it become clear that the project needed to be organized better, otherwise maintainability and legibility would suffer in the long run. I've decided to refactor the project and adopt an object oriented approach which seemed like a good fit for the data I've been working with.

Since `NamedTuple` classes unfortunately don't support inheritance without hacky workarounds, I've decided to go with the `dataclasses` package. Here I have faced a problem, since normally dataclasses are mutable and as such, they can't be used for hashing. This was an issue because I was planning to use some of these classes (such as`InventoryItems`) as dictionary keys, and only those data types can be used as dictionary keys which are hashable. To achieve this, I had to set `frozen` property to `True` on these classes to enforce immutability, which also made them hashable.

### Network calls
Around line 30 in `main.py` I have made a decision to make a separate network call for each individual set to the API.

While this can be more costly than pulling all the sets in one go, storing it in memory, then processing it later (it definitely does now), but if the set database ever grew larger, pulling all sets might quickly become infeasible.

A workaround could be implementing paging on the API side, so that only a single page would be processed at a time.
