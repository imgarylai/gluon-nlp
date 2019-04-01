# coding: utf-8

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Test BERTEmbedding."""
import subprocess
import time

import pytest

from ..bert.embedding import BertEmbedding
from ..bert.dataset import BertEmbeddingDataset


def test_bert_embedding_dataset():
    sentence = u'is this jacksonville ?'
    dataset = BertEmbeddingDataset([sentence])
    assert len(dataset) == 1


def test_bert_embedding_data_loader():
    sentence = u'is this jacksonville ?'
    bert = BertEmbedding(max_seq_length=10)
    first_sentence = None
    for i in bert.data_loader([sentence]):
        first_sentence = i
        break
    assert len(first_sentence[0][0]) == 10


def test_bert_embedding_data_loader_works_with_cased_data():
    bert = BertEmbedding(dataset_name="book_corpus_wiki_en_cased")
    assert bert.tokenizer.basic_tokenizer.lower == False


def test_bert_embedding_data_loader_works_with_uncased_data():
    bert = BertEmbedding(dataset_name="book_corpus_wiki_en_uncased")
    assert bert.tokenizer.basic_tokenizer.lower == True


@pytest.mark.serial
@pytest.mark.remote_required
@pytest.mark.gpu
def test_bert_embedding():
    # Test command line interface.
    # Sentences are passed through arguments.
    process = subprocess.check_call(['python', './scripts/bert/embedding.py', '--gpu', '0', '--dtype', 'float32',
                                     '--model', 'bert_12_768_12', '--dataset_name', 'book_corpus_wiki_en_uncased',
                                     '--max_seq_length', '25', '--batch_size', '256',
                                     '--oov_way', 'avg', '--sentences', '"is this jacksonville ?"'])
    time.sleep(5)
    # Load params.
    process = subprocess.check_call(['python', './scripts/bert/embedding.py', '--gpu', '0', '--dtype', 'float32',
                                     '--model', 'bert_12_768_12', '--dataset_name', 'book_corpus_wiki_en_uncased',
                                     '--max_seq_length', '25', '--batch_size', '256',
                                     '--params_path',
                                     '~/.mxnet/models/bert_12_768_12_book_corpus_wiki_en_uncased-75cc780f.params',
                                     '--oov_way', 'avg', '--sentences', '"is this jacksonville ?"', '--verbose'])
    time.sleep(5)
