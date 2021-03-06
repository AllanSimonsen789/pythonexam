import settings
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import cm
import seaborn as sns
from itertools import cycle, islice



def plot(df, filename):
    fig = df.plot(
        kind='bar',
        x="AnimalName",
        figsize=(20, 20),
        legend=False,
        stacked=True,
        fontsize=26).get_figure()

    xlocs, xlabs = plt.xticks()
    #Adds text with percentage over each bar
    for i, v in enumerate(df['Percentage']):
        plt.text(xlocs[i] - 0.40, v + 0.2, str(f'{(v):.2f}')+"%", fontsize=30)
    plt.xlabel("Animal", fontsize=30)
    plt.ylabel("Percentage", fontsize=30)
    plt.xticks(rotation=90)
    fig.savefig(settings.FILEPATH + 'static/plot_files/' + filename + '.png')
    




