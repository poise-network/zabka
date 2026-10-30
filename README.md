# Żabka Data APIs

A collection of APIs for retrieving structured e-commerce data from Żabka's digital platforms.

## Features

| Module | Description |
|---|---|
| `stores/` | Store locations and information |
| `categories/` | Product categories and catalog structure |
| `products/` | Product listings and availability |
| `search/` | Product search results |
| `pdp/` | Product detail pages |

## Data

[categories.json](categories/categories.json): Product categories and their IDs.

```json
[
  {
    "name": "HERBATY, KAWY, KAKAO",
    "id": "a4f6d88c-44a8-4296-80d9-b2b1e793e595",
    "depth": 1
  },
  {
    "name": "SPIŻARNIA",
    "id": "5dcb98da-6f9b-49a1-91dd-a6e192be0439",
    "depth": 1
  },
  {
    "name": "DOM I PREZENTY",
    "id": "b83b69f3-918c-4f86-a45f-a3ddef97db79",
    "depth": 1
  },
  {
    "name": [
      "HERBATY, KAWY, KAKAO",
      "Kawy mrożone"
    ],
    "id": "c0a1dd99-9fb4-4fd3-8239-8590c403b6da",
    "depth": 2
  },
  {
    "name": [
      "DOM I PREZENTY",
      "Pomysł na prezent"
    ],
    "id": "4e2001d0-65ac-4fb8-93f1-0b166925fd06",
    "depth": 2
  }
]
```

## Purpose

The crawlers support automated collection of retail data for:

- Product and assortment monitoring
- Pricing intelligence
- Search result analysis
- Store-level data collection
- Historical data analysis

## About

Developed and maintained by **Poise Network**, providing resilient access to external data sources at scale.

Website: <a href="https://poise.network" target="_blank" rel="noopener noreferrer">poise.network</a>
