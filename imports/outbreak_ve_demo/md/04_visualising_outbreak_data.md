# Why Visualisation Matters

Data tables provide detail, but visualisations reveal patterns that are difficult to see in raw numbers.

## Comparing Risk Between Groups

R Code\
group \<- c(\"Vaccinated\", \"Unvaccinated\")\
cases \<- c(5, 25)\
population \<- c(500, 500)\
risk \<- cases / population\
barplot(risk, names.arg = group, col = c(\"steelblue\", \"tomato\"))

## Understanding the Epidemic Curve

Image :: resources/images/epidemic-curve.png\
Alt :: Epidemic curve showing progression of cases over time\
Caption :: Figure 1. Outbreak progression by group\
Width :: 70%

## Reading Visual Data

Tabs\
Bar Chart :: Highlights differences in risk between groups\
Epidemic Curve :: Shows how the outbreak evolves over time\
Combined Insight :: Both views are needed for full interpretation

## Reflection

SelfCheck\
Question :: Why is it useful to view both a chart and a table?\
Answer :: Each provides different insights --- charts show patterns, tables show detail

## Key Message

Callout :: tip\
Text :: Visualisation supports faster and clearer interpretation of complex data
