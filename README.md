# Classification-Restaurant-using-Naive-Bayes-Method
classifying comments given to restaurants using the naive bayes method and comparing the results of lemmatization, stemming, gaussian, and multinomial with python.

compare results between lemmatization-gaussian, lemmatization-multinomial, stemming-gaussian, stemming-multinomial.

gaussian:
- calculate the feature probability of each term
- calculate the likelihood of each term (tf-idf) in each category
- calculate posterior probability

multinomial:
- calculate the prior or initial probability of the term appearing in each category
- calculate likelihood or conditional probability
- calculate the evidence or the probability of the emergence of the term
- calculate posterior
