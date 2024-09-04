# insper-nlp-relevance-search

Bluesky é um aplicativo relativamente novo que funciona de forma muito similar ao (falecido) Twitter. Com os recentes bloqueios ao X no Brasil, muitos usuários migraram para o Bluesky, e a plataforma tem crescido bastante. Fiz um pequeno projeto de NLP para analisar a relevância de posts no Bluesky, e implementei um sistema de busca que ranqueia os posts de acordo com a relevância.

## Instalação

Para instalar as dependências, basta rodar o seguinte comando:

```bash
pip install -r requirements.txt
```

## Como gerar o dataset

Para gerar o dataset, basta rodar o arquivo `download_posts.py`. O script conectará ao Firehose do Bluesky, e salvará todos os posts feitos em tempo real em `posts.csv`. Basta deixar rodando por alguns minutos para coletar uma boa quantidade de posts.

````bash
python download_posts.py
````

## Rodando o servidor

Com o dataset gerado, basta executar o seguinte comando para rodar o servidor:

```bash
python server.py
```

## Executando uma query

Para executar uma query, basta fazer uma requisição GET para `http://localhost:3000/query?q=QUERY`, onde `QUERY` é a sua query. O servidor retornará um JSON com os resultados.

Por exemplo, uma query para buscar posts sobre "elon musk" retorna:

```json
{
  "results": [
    {
      "cid": "bafyreich2qakfuger6r72wrvwy3oaer6gw7khudrrdcl3fx627aml6zxqu",
      "content": "te odeio elon musk",
      "relevance": 0.8586817654179242
    },
    {
      "cid": "bafyreibwy7frznlan4ooaatf3u2m4w4jahbpg3hvcm4z26pf67vv3uk3jy",
      "content": "elon musk vende o twitter pra narcisa e tudo vai ficar bem",
      "relevance": 0.5111486947629875
    },
    {
      "cid": "bafyreiglqpulqjgo2qwu36lf7ytevhydqbfskr4fhovm73wxvwujnm32bq",
      "content": "O foguete do Musk tem ré! 😂😂😂😂",
      "relevance": 0.44739076979532516
    },
    {
      "cid": "bafyreihq5c44lnus3zou6bgadus452d6trkrsynrurrzti4cc72c5etsfu",
      "content": "Culpem o Musk.",
      "relevance": 0.4352516153452149
    },
    ...
  ],
  "message": "OK"
}
```

## Exemplos de query:

### Query que retorna 10 resultados
https://insper-nlp-relevance-search.fly.dev/query?q=elon%20musk

"Elon Musk" é um tópico em alta no momento devido às polêmicas e bloqueio do X.

### Query que não retorna resultados
https://insper-nlp-relevance-search.fly.dev/query?q=insper

Durante o tempo de download do dataset, nenhum post sobre o Insper foi feito.

### Query interessante
https://insper-nlp-relevance-search.fly.dev/query?q=social

Mesmo pesquisando por "social", todos os posts retornados falam sobre "rede social", muito provavelmente devido aos acontecimentos recentes e a novidade de uma rede social nova no mercado.

