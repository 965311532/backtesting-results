# What is this?

This repository contains the results of a research project I conducted to determine the actual performance of a trading person that was selling thir trading signals (at the time, I'm not sure if they're still in business).

## Why?

At the time, I was curious to determine whether it'd be possible to pass a [prop firm challenge](https://www.investopedia.com/terms/p/proprietarytrading.asp) using such paid signals, but I was a bit skeptical of the results claimed by this individual.

## How?

I built a simple [backtesting engine](https://github.com/965311532/signals-backtesting), which parsed the Telegram messages into serialized trade signals, and then ran it through the engine to determine the result of the trade. I then put the results into a notebook to play with the numbers and determine the results.

These metrics were taken into consideration:
- Overall cumulative results
- Monthly cumulative results
- Total drawdown
- Daily drawdown
- Trading frequency
- Custom "Challenge Pass" metric
- And more

You can check out the notebook [here](https://nbviewer.org/github/965311532/backtesting-results/blob/master/backtesting-results.ipynb?flush-cache=True).

## Screenshots

These are some example screenshots from the analysis:

![Cumulative Result Example](data/cumres-eg.png)
![Drawdown Example](data/dd-eg.png)
![Streak Distribution Example](data/streak-dist.png)

## So what did you find?

The analysis was somewhat inconclusive, as there wasn't enough evidence to determine that they were lying or that they were really profitable as they claimed. I think I can say with some degree of certainty that prop firm challenges are strategically too hard to be beaten by traders in general, let alone by a distributed strategy of doubtful performance.
