# wiki_racer
### Behaviour
Finds the shortest path between two articles on wikipedia navigating through other articles available as links on each article only.

Takes 2 required command line arguments, start_url and target_url. 

Prints the shortest path and number of steps involved to the terminal.

### Current limitations
Because my hardware does ~200-300 requests per minute, and wikipedia has ~7 million articles, this can take A LONG time to execute (weeks) for just 1 result.

I can see a few ways to solve this issue. One way is to get a map of the entire site, getting a list of every unique article link that occurs in every article, which would be quite time consuming to produce myself and prone to becoming out of date. This could be sped up using a multithreaded approach, where many requests could be sent and responses processed concurrently so long I ensure that no request with a higher page depth is processed before all of the current depth are finished processing.
