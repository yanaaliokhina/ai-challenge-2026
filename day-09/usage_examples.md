# Day 9 – Usage Examples

## How to Run

### Basic query against a candidates file

```bash
python src/main.py --query "What is a neural network?" --file candidates.txt
```

Expected output:

```
Rank   Score    Text
----------------------------------------------------------------------
1      0.9312   A neural network is a machine learning model inspired by the brain.
2      0.8741   Deep learning uses layers of neurons to learn representations.
3      0.6103   Python is a popular programming language for data science.
4      0.4892   The Eiffel Tower is located in Paris, France.
5      0.3201   Photosynthesis is the process by which plants convert light to energy.
```

### With a custom model

```bash
python src/main.py --query "climate change" --file candidates.txt --model voyage-large-2
```

### Missing required arguments

```bash
python src/main.py --query "hello"
# error: the following arguments are required: --file

python src/main.py --file candidates.txt
# error: the following arguments are required: --query
```

### Example candidates.txt format

```
A neural network is a machine learning model inspired by the brain.
Deep learning uses layers of neurons to learn representations.
Python is a popular programming language for data science.
The Eiffel Tower is located in Paris, France.
Photosynthesis is the process by which plants convert light to energy.
```

## How to Run Tests

```bash
# All tests
python -m pytest day-09/tests/ -v

# Similarity logic only
python -m pytest day-09/tests/test_similarity.py -v

# Embedding client only
python -m pytest day-09/tests/test_embedding_client.py -v

# CLI / file loading only
python -m pytest day-09/tests/test_main.py -v
```
