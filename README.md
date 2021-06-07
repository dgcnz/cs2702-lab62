# Lab 6.1: Inverted Index


## Preprocessor class

Wrapper class for text normalization functions.

```python
# Returns normalized word
Preprocessor.clean(word: str) -> str
```

```python
# Returns normalized text as list of tokens
Preprocessor.clean_text(text: str) -> List[str]
```

## Inverted Index class

```python
# Builds inverted index with set of documents, preprocessor and number of words (most frequent)
build_inverted_index(documents: List[str], p: Preprocessor, k: int) -> InvertedIndex
```

```python
# Returns indexes of documents containing word
InvertedIndex.sources(word: str) -> List[int]
```

## Operators

```python
# Returns union of sorted lists a and b
OR(a: List[int], b: List[int]) -> List[int]
```

```python
# Returns conjunction of sorted lists a and b
AND(a: List[int], b: List[int]) -> List[int]
```

```python
# Returns conjunction of sorted lists a and negation of b
ANDNOT(a: List[int], b: List[int]) -> List[int]
```


## Parsing

Parsing is done with pyparsing library according to this grammar:

```
EXPR    := RET | OPRET
RET     := RET ( word )
OPRET   := OP ( EXPR , EXPR )
OP      := AND | OR | ANDNOT
```

Check parse.py for more details.
