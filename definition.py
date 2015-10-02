#!/usr/bin/python

word_count = []

word_count.extend([13, 14, 13, 13, 9])
word_count.extend([11, 13, 12, 5])
word_count.extend([11, 16, 12, 12, 13, 15])
word_count.extend([4, 12, 11, 13, 15, 12, 12])
word_count.extend([11, 14, 16, 14, 14, 5])
word_count.extend([14, 12, 9, 14, 4])

# 435 sider * 388 ord per side?
# == 170 000 ord
print sum(word_count)

