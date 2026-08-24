Designed an interactive system that recommends Steam games to users based on their preferences and presents the results in a clear and interpretable way. We were able to visualize the relationship between our recommended games and the user's favorite game using a simplified graph.

Frontend (Interface):
- use tkinter library to form user interface
- allow user to enter their favorites game, genres and price range to allow us to filter for suitable games
- display results in the form of a list of games sorted from best to worst,  visual graph and a bar chart
- display comments from other gamers

Backend:
- cleaned datasets taken from GitHub and combined them to form a comprehensive dataset to filter through
- hide the actual graph ,connecting all games in the dataset, that is created upon running the program, to make it simpler for user to interpret data
- created: 
   -  user-game edges, which represent if a user reviewed or interacted with a game
   -  game-game edges, which represent if two games are considered sufficiently similar according to our         similarity function 
- developed a similarity computation that uses a Jaccard-style similarity measure to compare the tag sets of the two games
- visualized data using networkX, which creates a page that allows user to zoom, pan, reset axes and download png of graph
