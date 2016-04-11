from __future__ import division
import urllib2
from collections import Counter
from collections import defaultdict
import orchpy as op
import time

def split_partitions(sizes, num_partitions):
  total_size = sum(sizes)
  partition_size = (total_size + num_partitions - 1) // num_partitions
  perm = sorted(range(len(sizes)), key=lambda k: sizes[k])
  head, tail = perm, []
  result = [[] for i in range(num_partitions-1)]
  # first assign the first num_partitions - 1 partitions
  for partition in range(len(result)):
    cur_size = 0
    while len(head) > 0:
      elem = head.pop()
      if sizes[elem] <= partition_size - cur_size:
        result[partition].append(elem)
        cur_size += sizes[elem]
      else:
        tail.append(elem)
    head, tail = list(reversed(tail)), []
  # then assign the last partition
  result.append(head)
  return result


# files = books.values()

# data = urllib2.urlopen(files[0]).read()

# this is incorrect use default dict with a zero and accumulate into that!
# def sum_up(dict1, dict2):
#   result = {}
#   for key in dict1.keys():
#     result[key] = dict1[key] + dict2[key]
#   return result

@op.distributed([str], [str, int])
def load_textfile(url):
  # return urllib2.urlopen(url).read()
  result = open(url, "r").read()
  return result, len(result)

@op.distributed([str], [dict])
def count_words(data):
  word_list = data.split()
  return Counter(word_list)

# @op.distributed([str], [dict])
# def parse_time(data):
#   word_list = data.split()
#  d = Counter(word_list)

# @op.distributed
# def count_words(data: str) -> dict:
#     # ...

@op.distributed([str], [dict])
def count_words_fast(data):
 counter = defaultdict(int)
 for k in data:
   counter[k] += 1
 return dict(counter)

@op.distributed([dict, None], [dict])
def sum_by_key(*dicts):
  result = defaultdict(int)
  for d in dicts:
    d_get = d.get
    for key in d.keys():
      result[key] += d_get(key)
  return result

@op.distributed([dict, None], [int])
def sum_by_key_return_len(*dicts):
  result = defaultdict(int)
  for d in dicts:
    d_get = d.get
    for key in d.keys():
      result[key] += d_get(key)
  return len(result)

def red(*dicts):
  result = defaultdict(int)
  for d in dicts:
    d_get = d.get
    for key in d.keys():
      result[key] += d_get(key)
  return result

@op.distributed([str, None], [dict])
def map_reduce(*data):
  c = Counter()
  for s in data:
    c.update(s.split())
  return c

@op.distributed([str, None], [int])
def map_reduce2(*data):
  c = Counter()
  for s in data:
    c.update(s.split())
  return 1