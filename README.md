# LEGO

## Requirements
* Modern Python
* requests library

Dependencies are managed using [Poetry](https://python-poetry.org/)

## Considerations

### First look
At first I have tried to locate Swagger or OpenAPI schemas at conventional locations, but couldn't find any.

Since there was no API definition which I could have used to generate the API client skeleton, I have coded a small abstraction layer on top of the `requests` calls myself to make the code easier to read and easier to test without mocking.

For most other languages, I would have probably built the model out using a bunch of dataclasses, so that the typing system can help during coding and the compiler can validate the code. However, in Python it's not considered very idiomatic, so I have decided not to do that.

I have realized early that the total piece count is provided by both the sets and the user inventory, so I could very easily eliminate those sets which were made up of less bricks than the user had in total.

### Data structure

I have also noticed that the data structure for a user's personal inventory was way too deep for my use case, so I have decided to flatten it out in a way that the quantities are stored per unique `(design ID, color)` combinations. 

Since these combinations are unique per user, I was able to use them as key values in a dictionary. Dictionary items can be inserted and queried in constant time, so it is a perfect choice for storing the available amounts of a specific piece.

### Network calls
Around line 40 in `main.py` I have made a decision to make a separate network call for each individual set to the API.

While this can be more costly than pulling all the sets in one go, storing it in memory, then processing it later (it definitely does now), but if the set database ever grew larger, pulling all sets might quickly become infeasible.

A workaround could be implementing paging on the API side, so that only a single page would be processed at a time.

### Misc
`flatten_pieces()` is a generator function, which is useful if someone wants to process data in chunks. For this amount of data it really doesn't make any sense to use it, but since it doesn't hurt legibility and allows for better scaling, I have left it in.
