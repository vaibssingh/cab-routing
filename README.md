# Cab Routing  
Approach for solution:
- Read the file and store the coordinate values for the passengers, cabs and final destination.
- Depending on the number of passengers, create their location grouping [lat, long] using k-means cluterization.
- Once the coordinate groups are obtained, find the total distance of each of the available cab from their current location
- Add the distance to the destination to the above distance as well.
- From the list of distances for each group to their respective destination + cab distance, find the route with minimum distance
and print that out
