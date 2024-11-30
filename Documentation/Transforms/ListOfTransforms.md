# Transforms available in `viewser`

- **rename** (`any/util.rename`)  
Allows you to rename transformed variables, especially in cases where the transformation added suffixes that are not user-friendly. Automatically called by all queryset columns in `viewser` to ensure that they are given the names requested by the user. 
 
- **ln** (`any/ops.ln`)  
Produces the natural logarithm of the variable or coefficient. A natural logarithm enhances readablity by reducing the dynamic range of the feature (dynamic range is the ratio between the largest and smallest values that a certain quantity can assume). Returns the natural log (ln) of (`1+feature values`), with the `1`+ ensuring that zero values of the feature are handled gracefully.

- **Boolean transforms**  
This class of transforms convert real features (input data variables) into dummy or boolean features, whose values can be 0 or 1 only. 

- **gte** (`any/bool.gte`)  
Returns 1 if feature values are greater than or equal to the supplied parameter, zero otherwise.
               
 - **lte** (`any/bool.lte`)             
Returns 1 if feature values are less than or equal to the supplied parameter, zero otherwise.
       
 - **in_range** (`any/bool.in_range`)                 
Returns 1 if feature values are in the supplied range, zero otherwise.

 - **Temporal transforms**   
A class of transforms that operates on the time-dimension of the data.  

    - **delta** (`any/temporal.delta`)  
    llows display of changes in a feature over a specified time (for example between 2005 and 2010) by subtracting the value of the start of the selected time period from the current value of the feature. This would give, for example, the change in value between 2005 and 2010 (*feature[now]-feature[now-time]*). 

    - **tlag** (`any/temporal.tlag`)   
    This transform is used to create a temporal lag of a feature (variable), meaning it includes information about the past (past values) toinform the present or future (predictions). This makes it possible to measure the effect over time. 

        In practice, the transformation plots/lags a set of observations of a feature/variable (for example country X in 1990) against a second set of observations for the same country in another year (e.g. country X in 1991).

        For example, a model may look for a relationship between feature A and feature B, but with the values of feature B lagged by 6 months, so that a relationship is found between the current value of A and the value of B six months ago. If the current value of B is then inserted into the model, it will produce a forecast of the value of A six months into the future.   
          
    - **tlead** (`any/temporal.tlead`)   
        This transformation is used to create a temporal lead of a feature (variable) – the opposite of a temporal lag - in that it informs past observations with present/future observations. This means that it will transform/change the past observations by whatever information on the future is added, hence it should be used very carefully. This transform is scarcely used in practice, since it is of limited use in forecasting.
          
    - **moving_average** (`any/temporal.moving_average`)        
        This transform creates a so called "moving average" of the feature in question over a specified time window (for example 10 years). This transformation can help with producing trendlines, as it smoothes out noise in the data by averaging over many timesteps, rather than emphasising each individual value. The time window extends into the past, hence displaying the development of a feature from time $t0$ over the last 10 years (or any other chosen time window) and does not include the averaged observations of future observations greater than $t0$. An example would be $t0=2010$ with a time window of the past 10 years, giving an average over the years 2000 to 2010.  

        - **moving_sum** (`any/temporal.moving_sum`)   
        This transform functions similarly to the moving average. Instead of taking the average value of the observations it creates a sum over the specified time window. The time window extends into the past, hence displaying the development of a feature from time $t0$ over the last 10 years (or any other chosen time window) and does not include the averaged observations of future observations greater than $t0$. An example would be $t0=2010$ with a time window of the past 10 years, giving an average over the years 2000 to 2010.   

        - **onset_possible** (`any/temporal.onset_possible`)         
        This transform helps to determines whether an onset of conflict (i.e. a transition from a state of peace to a state of conflict) is possible within a given time window (for example March 2009 until September 2009). It returns a value of 0 for every time step (month) when an onset is not possible and a value of 1 when it is. 

        - **onset** (`any/temporal.onset`)    
        This transform helps to locate an onset of conflict in a time series data, within a given time window (for example March 2009 until September 2009). It returns a 1 (conflict onset) for every time the feature is greater than 0, given in the previous time-step (month) the value was 0. It returns a 0  (no onset) if there is no onset.       

        - **entropy** (`any/temporal.entropy`)  
        In Statistics, entropy is used to quantify differences between expected values by taking the log of the inversion of the probability of surprise. Meaning it describes the average surprise we have per coin toss for example to receive heads. For a coin that has no affinity for heads or tails, the outcome of any number of tosses is difficult to predict. Why? Because there is no relationship between flipping and the outcome. This is the essence of entropy.   
        
          In Machine Learning and for the VIEWS project it has a bit of a more complicated focus. Here, the expected surprise equals the #randomness of information - how random or unpredictable is a certain outcome. The higher the entropy value, the higher the unpredictiveness. Entropy in physics and statistics is a measure of the disorder, unpredictability or changeability of a dataset. A smooth dataset where values do not change very much is said to have a low entropy, whereas a dataset containing lots of complex variation is said to have a high entropy. 
        
            The entropy transform computes the average value of the target feature in a sliding time window, and then adds up, for each individual value in the window, a measure of how different that value is from the average. The larger the result of this operation, the higher the changeability and thus the entropy of the data.

        - **cweq** (`any/temporal.cweq`)  
        Counts, moving forwards in time, while the feature is equal to a specified value, resetting to zero when the feature ceases to be equal to the value. This transform can be use in combination with the boolean transforms to, for example, count the lengths of periods of conflict

        - **time_since** (`any/temporal.time_since`)      
        This transform is similar to cweq. It also counts forward in time, and returns the time since the feature had a non-zero value. 

        - **decay** (`any/temporal.decay`)  
        When combined with `temporal.time_since`, computes an exponential time decay function whose value is 1 where the feature is non-zero, and decays exponentially into the future with the specified halflife. When a new non-zero value is encountered, the value of the decay function is set back to 1, and previous values are effectively forgotten.  
  
            This transform is designed for use with dummy features, since it takes account only of whether the raw feature is non-zero.  
            
            For decay functions that can be applied to real features, see temporal.tree_lag.
   
        - **tree_lag** (`any/temporal.tree_lag`)              
        This transform is an alternative to the straightforward temporal lag and to the temporal decay. From a given point in time, it computes a weighted sum over the values of the feature over all past times, where the weight give to a particular value depends on how far back in time that value lies, and several weighting functions can be selected. Unlike the standard temporal lag, this transform has an infinitely long memory, and unlike the temporal_decay transform, it never forgets any past events, and can be used with either dummy or real features.   

 - **`missing` transforms**  
    These transforms deal in very simple ways with the issue of missing data, where the values of a feature for some times or locations are unknown or unavailable, and are represented by a placeholder, usually `NaN`, short for `Not a Number`. It is usually necessary to replace NaNs with numbers, because most mathematical operations or transforms cannot accept a `NaN` as an input value.

 - **replace_na** (`any/missing.replace_na`)   
    This is the simplest missing transform, and just replaces missing values  a zero value. 
 
 - **fill** (`any/missing.fill`)    
    Fills missing values in a column or table in a slightly more sophisticated way than replace_na. This is done so that missing values are filled in with values which are more presentative of the data which is actually present in the dataset. Two optional arguments can be passed with this transformation. First, in which direction to fill, i.e. from the past past  (so-called forward-filling) or from the future (backward filling). If there is a gap in the dataset with missing data, forward-filling copies the last known value before the gap into the empty values, whereas backward-filling copies in the first known value after the gap. The second parameter controls whether only missing values within the temporal range of the dataframe should be filled or missing observations which are outside the current range should be added as well.
                  
 
 -  **extrapolate** (`any/missing.extrapolate`)  
    This transform also deals with missing observations, and is a further improvement over missing.fill. When a gap in the data is encountered, the last known value before the gap and the first known value after it are used to fill in values that smoothly (linearly) progress between these values across the gap. This transform can also be used to extend the range of data, e.g. extrapolating a model that only has available data from 2000 to 2010 into 2013, which is done simply by propagating the last known value into the future.


 - **mean** (`any/unit.mean`)                   
    This produces the mean value of a variable, by summing up all values and dividing them by the number of observations. Returns a series where all values are equal to the mean of the non-zero values of the feature (taken over all timesteps usually equal to one month in the feature).
 
 -  **demean** (`any/unit.demean`)                      
    This subtracts from each value of the feature the mean of the feature's non-zero values.
 
 - **rollmax** (`any/unit.rollmax`)            
    This transform produces the rolling maximum of the feature within a predefined time-span (for example 6 months). A rolling maximum is produced by taking the highest value and applying it to all time-steps (months) until a new maximum is met, which it is then replaced with. For the months April till September (April = 3.7), May =3.2, June = 3.4, July = 3.6, August = 4, September = 3,9) the rolling maximum for example would be 3.7 for April till July, in August the maximum value is 4 though, so the rolling maximum will take the value of 4 for the months of August and September. 
 
 - **`spatial` transforms**  
These transforms make use of the spatial relationships between different units of analysis, in particular the distances between them. The motivation behind using spatial lags is that what occurs in one country or grid cell is likely to influence what occurs in other countries and cells, and that influence is likely to be stronger between nearby locations and weaker between distant locations.

 - **countrylag** (`country_month/spatial.countrylag`)   
This transform preforms spatial lags at the country-level. It works in a similar way to spatial.lag, by placing a kernel at the location of each country and summing the values of neighbouring countries within the kernel. The kernel is defined by an inner radius and a width. An inner radius of 0 indicates that the sum should include the target country itself, 1 indicates that the target country should be left out of the sum but its neighbours are included, 2 indicates that the target country and its neighbours are left out of the sum, etc. The kernel width determines how far outwards from the inner radius the kernel extends. An inner radius of 1 and a width of 1, for example, indicates that the target country is excluded, but its neighbours are included. The transform takes a third argument which is the power to be used in weighting by distance (using the distances between the centroids of neighbouring countries and the centroid of the target country). The fourth argument is a flag indicating whether the distance weights are to be normalised (so that they sum to one).

 - **lag** (`priogrid_month/spatial.lag`)   
This transform produces a spatial lag using priogrid cells. A prio-grid cell is approximately 55 x 55 km in longitude and latitude. The transform is kernel-based, meaning it produces a square over the origin cell of interest and its area of influence, and requires four parameters: 
    - The inner limit of the kernel, for example 0 to include the target cell, 1 to include it
    - The width in the cells of the kernel, i.e. how many cells to count outwards from the inner radius
    - The value for the kernel power, i.e. the power used to weight kernel cells by distance from the target cell
    - The kernel norm, controlling whether the kernel weights should be scaled so that they sum to one  
    
        The simplest form is to do an unweighted sum over the eight cells surrounding every prio-grid cell, in which case both the values if the inner kernel and the kernel width are 1, and the other parameters are 0. Unweighted means that every cell is given the same importance.
 
- **treelag** (`priogrid_month/spatial.treelag`)       
    The spatial treelag transform is mainly different from the ordinary spatial lag in that there is no kernel - an approximate weighted sum over the whole pg grid is computed at every grid cell (ignoring the target cell itself). This is done by hierarchically aggregating cells into groups, with cells further away from the target cell being aggregated into larger groups than those nearby. The treelag transform in principle allows spatial relationships to be modelled over arbitrarily large distances.
 
