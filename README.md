# Grand Tours Data Analysis

As an avid cyclist, I try to follow professional cycling closely, from grand
tours to one-day spring classics. Cycling inherently generates a wealth of
data, both from riders and the environments they ride. This makes it a
fascinating field to explore and apply data analysis skills.

Grand tours like the Tour de France (TDF) and Giro d'Italia have larger
audiences and seem to provide better databases for analysis. Therefore, I will
start with TDF analysis. The official TDF [website](https://www.letour.fr/en/)
offers a database for all tours dating back to 1903, but I find the
[ProCyclingStats](https://www.procyclingstats.com) website easier to scrape,
and it also contains more detailed information.

As expected, [Strava](https://www.strava.com) data is harder to obtain. First,
you need to compile a list of pro riders' Strava IDs, then retrieve the
activity IDs to scrape the available data. Unfortunately, not all professional
cyclists use Strava, and those who do often don't publish their power metrics.
However, some riders share their key metrics, providing valuable insights we
can learn from.

Before I continue with the scraping and data preparation details, I am listing some questions below to ensure I stay focused on the project and don't forget anything. This list will be updated as I come up with more questions.

## Questions about totals

- Average speed each year.
- Total distance, total ascent each year.
- Which cities they have gone? Pinpoint them on the map. Also from the
  pros strava uploads we can download and get the route for each year.

## Stage-wise questions

- How many stages has more climbing than average ? Like queen stage each year.
- How does the average speed changes at each stage at each year? This is connected to the recovery metrics of the riders.
- How does the time gaps change in each stage? What does it depend on climbs, flats, wind?
- There is a data section with how each stage ended e.g. sprint, solo or sth else. From this first get the distribution and then try to come up with a model.
- From strava segments data we can filter the downhill or flat segments and try to see if the aerodynamic tech really help on avg speed over the years.

## Pogi specific questions

Pogi obviously don't publish his power data on Strava. However we can still

- The original question was how much Pogi deviates from the standart? at each stage (may be in general time too)
- What about other deviations, like Lance, Indurain, Pantani... or in general the winners. Compare those with Pogi's dominance.
- Pogis performance after doing back to back tours?

## General Strava questions

- How many riders are using strava each year ? This is a two way question they might have strava now but may be they didn't have it at the time soooo might look for the strava uploads but that will take some time.
- From recovery day activities can we get anything related with rest of the tour?
- Who uses what? Garmin, Wahoo or some other device.
- We don't have weather data for older tours but it will be interesting to check the weather effects on speed and power.

## Segment based questions

- How does a rider's power output (watts) vary across different types of stages (mountain, time trial, flat)?
