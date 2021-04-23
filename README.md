# Guessb: Ferramenta para detectar comentários ofensivos no Facebook
Trabalho de Conclusão de Curso (TCC) do curso de Bacharel em Sistemas de Informação (BSI) da Universidade do Estado de Santa Catarina (UDESC) 2015/1.

## Resumo
Este trabalho apresenta a proposta de uma ferramenta Web que realizará mineração de opiniões - positivo, negativo ou neutro - na rede social online Facebook. Pode-se conceituar rede social como sendo um grupo de pessoas que interagem por intermédio
de qualquer mídia de comunicação. Análise de sentimento, mineração de opiniões ou análise de subjetividade é um campo de estudo dentro de inteligência artificial que busca extrair informações subjetivas como opiniões, sentimentos, escritos em
linguagem natural. Uma das técnicas bem difundidas em análise de sentimento é a técnica Naive Bayes, que é uma técnica de aprendizado de máquina supervisionado presente em uma biblioteca de mineração de texto, nomeada de NLTK-Trainer. 
A importância monitorar tais opiniões reside no fato de que organizações que fazem uso de redes socais necessitam monitorar seus produtos/serviços visando traçar estratégias com base nesses sentimentos. Para extrair dados do Facebook foi utilizado uma
biblioteca nomeada de Django-Facebook, que é uma implementação da Facebook Graph API. Por fim, com a finalidade de avaliar a ferramenta proposta, foram coletados 90 comentários igualmente distribuídos em positivos, negativos ou neutros. Ao final
observou-se que a ferramenta definiu as postagens em positiva, negativa ou neutra com grande percentual de acurácia, obtendo uma taxa média de acerto de 72% nesta classificação.

## Objetivos
Desenvolver uma ferramenta que, por intermédio de técnicas de aprendizagem de máquina, possa atribuir significado (negativo, positivo ou neutro) a postagens feitas na rede social Facebook em língua portuguesa do Brasil

### Ojbetivos específicos
- Identificar comentários ofensivos que fazem uso de adjetivos e verbos negativos cujo objeto é um único usuário, sem levar em consideração o contexto
(publicação);
- Apontar postagem de comentários ofensivos que não fazem uso de adjetivos negativos, porém, ainda assim, expressam conteúdo pejorativo a um usuário ou de organizações;
- Validar a ferramenta por intermédio de dados reais capturados da rede social Facebook e rotulados empiricamente em positivo (bom), negativo (ruim) ou neutro (objetivo).

## Tecnicas utilizadas
- Machine Learning
  - Supervised Machine Learning:
    - `DecisionTreeClassifier`
    - `RandomForestClassifier`
    - `LogisticRegressionClassifier`
    - `BernoulliNaiveBayesClassifier`
    - `GaussianNaiveBayesClassifier`
    - `MultinomialNaiveBayesClassifier`
    - `KNearestNeighborClassifier`
    - `GradientBoosterClassifier`
    - `ExtraTreesClassifier`
    
## Tecnologias utilizadas
- [Django](https://www.djangoproject.com/) - Framework web Python.
- [NLTK](https://www.nltk.org/) - NLTK is a leading platform for building Python programs to work with human language data.
- [NLTK-Trainer](https://github.com/japerk/nltk-trainer) - NLTK Trainer exists to make training and evaluating NLTK objects as easy as possible.
