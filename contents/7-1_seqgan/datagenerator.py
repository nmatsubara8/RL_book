import linecache
import random

import numpy as np
from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import to_categorical


class Vocab(object):
    def __init__(self, sentences_path):
        self.PAD = 0
        self.BOS = 1
        self.EOS = 2
        self.UNK = 3
        self.PAD_TOKEN = '<PAD>'
        self.BOS_TOKEN = '<S>'
        self.EOS_TOKEN = '</S>'
        self.UNK_TOKEN = '<UNK>'
        self.word2id = {
            self.PAD_TOKEN: self.PAD,
            self.BOS_TOKEN: self.BOS,
            self.EOS_TOKEN: self.EOS,
            self.UNK_TOKEN: self.UNK,
        }
        self.id2word = {v: k for k, v in self.word2id.items()}
        self.sentences = load_data(sentences_path)
        self.build_vocab(self.sentences)
        self.vocab_num = len(self.word2id)
        self.sentence_num = len(self.sentences)

    def build_vocab(self, sentences, min_count=1):
        word_counter = {}
        for sentence in sentences:
            for word in sentence:
                word_counter[word] = word_counter.get(word, 0) + 1
        for word, count in sorted(
            word_counter.items(), key=lambda x: x[1], reverse=True
        ):
            if count < min_count:
                break
            _id = len(self.word2id)
            self.word2id.setdefault(word, _id)
            self.id2word[_id] = word

    def write_word2id(self, sentences_path, output_path):
        ids_sentences = []
        for line in open(sentences_path, encoding='utf-8'):
            words = line.strip().split()
            ids_words = [
                str(self.word2id.get(word, self.UNK)) for word in words
            ]
            ids_sentences.append(ids_words)
        self.data_num = len(ids_sentences)
        output_str = ''
        for i in range(count_data(sentences_path)):
            output_str += ' '.join(ids_sentences[i]) + '\n'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_str)

    def write_id2word(self, ids_path, output_path):
        sentences = []
        for line in open(ids_path, encoding='utf-8'):
            ids = line.strip().split()
            words_ids = [
                self.id2word.get(int(id), self.UNK_TOKEN) for id in ids
            ]
            sentences.append(words_ids)
        output_str = ''
        for i in range(count_data(ids_path)):
            output_str += ' '.join(sentences[i]) + '\n'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_str)


def load_data(file_path):
    data = []
    for line in open(file_path, encoding='utf-8'):
        words = line.strip().split()
        data.append(words)
    return data


def count_data(file_path):
    data_num = 0
    for line in open(file_path, encoding='utf-8'):
        data_num += 1
    return data_num


def padding(sentences, T, PAD=0):
    sentences += [PAD for i in range(T - len(sentences))]
    return sentences


def sentence_to_ids(vocab, sentence, UNK=3):
    ids = [vocab.word2id.get(word, UNK) for word in sentence]
    return ids


class DataForGenerator(Sequence):
    def __init__(self, ids_path, batch_size, T, vocab, shuffle=True):
        self.ids_path = ids_path
        self.batch_size = batch_size
        self.n_data = count_data(ids_path)
        self.T = T
        self.shuffle = shuffle
        self.vocab = vocab
        self.reset()

    def __len__(self):
        return self.n_data // self.batch_size

    def __getitem__(self, idx):
        batch_x = []
        batch_y = []
        batch_start = idx * self.batch_size
        batch_end = (idx + 1) * self.batch_size
        for i in range(batch_start, batch_end):
            each_x = []
            each_y = []
            line_index = self.shuffled_indices[i] + 1
            id_sentence = linecache.getline(self.ids_path, line_index)
            id_words = id_sentence.strip().split()

            each_x = [self.vocab.BOS, *id_words, self.vocab.EOS]
            batch_x.append(each_x)

            each_y = [*id_words, self.vocab.EOS]
            batch_y.append(each_y)

        for i, id_words in enumerate(batch_x):
            batch_x[i] = batch_x[i][:self.T]
        for i, id_words in enumerate(batch_y):
            batch_y[i] = batch_y[i][:self.T]

        batch_x = [padding(sentences, self.T) for sentences in batch_x]
        batch_x = np.array(batch_x, dtype=np.int32)

        batch_y = [padding(sentences, self.T) for sentences in batch_y]
        batch_y = np.array(batch_y, dtype=np.int32)
        batch_y = to_categorical(batch_y, num_classes=self.vocab.vocab_num)

        return batch_x, batch_y

    def reset(self):
        self.idx = 0
        if self.shuffle:
            self.shuffled_indices = np.arange(self.n_data)
            random.shuffle(self.shuffled_indices)

    def on_epoch_end(self):
        self.reset()


class DataForDiscriminator(Sequence):
    def __init__(self, pos_path, neg_path, batch_size, T, vocab, shuffle=True):
        self.pos_path = pos_path
        self.neg_path = neg_path
        self.batch_size = batch_size
        self.T = T
        self.shuffle = shuffle
        self.vocab = vocab
        self.pos_n_data = count_data(pos_path)
        self.neg_n_data = count_data(neg_path)
        self.n_data = self.pos_n_data + self.neg_n_data
        self.reset()

    def __len__(self):
        return self.n_data // self.batch_size

    def __getitem__(self, idx):
        batch_x = []
        batch_y = []
        batch_start = idx * self.batch_size
        batch_end = (idx + 1) * self.batch_size
        for i in range(batch_start, batch_end):
            each_x = []
            line_index = self.shuffled_indices[i] + 1
            if line_index < self.pos_n_data:
                id_sentence = linecache.getline(self.pos_path, line_index)
                is_pos = 1
            else:
                line_index = line_index - self.pos_n_data
                id_sentence = linecache.getline(self.neg_path, line_index)
                is_pos = 0
            id_words = id_sentence.strip().split()

            each_x = [*id_words, self.vocab.EOS]
            batch_x.append(each_x)
            batch_y.append(is_pos)
            linecache.clearcache()

        for i, id_words in enumerate(batch_x):
            batch_x[i] = batch_x[i][:self.T]

        batch_x = [padding(sentences, self.T) for sentences in batch_x]
        batch_x = np.array(batch_x, dtype=np.int32)

        return batch_x, batch_y

    def reset(self):
        self.idx = 0
        if self.shuffle:
            self.shuffled_indices = np.arange(self.n_data)
            random.shuffle(self.shuffled_indices)

    def on_epoch_end(self):
        self.reset()
