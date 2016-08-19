
# What do I want ...

# grouped by ID
# ordered by sum(char_count)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('comments.csv')
df.groupby('id').sum().to_csv('grouped.csv')

df = pd.read_csv('grouped.csv')
df = df.sort_values(by='char_count', ascending=False)
df.to_csv('grouped_sorted.csv')

df = pd.read_csv('grouped_sorted.csv')

wc = df.word_count

df2 = pd.DataFrame(wc)
df2['idx'] = np.array([int((x*100.0) / wc.size) for x in range(0, wc.size)])
# df2['antall_personer'] = np.array([1 for x in range(0, wc.size)])
# df2.to_csv('andel_av_kumulative_kommentarer.csv')

g = df2.groupby('idx').sum()
g.word_count = g.word_count.cumsum() * 100.0 / g.word_count.sum()
g.plot()
plt.show()

import ipdb; ipdb.set_trace()

