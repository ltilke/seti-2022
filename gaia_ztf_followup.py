import pandas as pd
import eleanor
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def get_data():
    data = pd.read_csv('candidates.csv')
    data = data.rename(columns={data.columns[0]: 'tic'})
    data['sec'] = 6
    confidence_mask = data['dip_confidence'] >= 1.0
    data_confident = data[confidence_mask]
    return data_confident


def in_ztf(data):
    pass


def in_gaia(data):
    pass


def graph_tess_lc(lc, tic, fig_path):
    plt.clf()

    # plt.scatter(lc.time, lc.pca_flux/np.nanmedian(lc.pca_flux), label='PCA', s=10)
    q = lc.quality == 0
    plt.scatter(lc.time[q], lc.pca_flux[q]/np.nanmedian(lc.pca_flux[q]), label='PCA (q == 0)', s=10)

    plt.ylabel('Normalized Flux')
    plt.xlabel('Time [BJD - 2457000]')
    plt.title('TESS: TIC ' + str(tic))

    plt.savefig(fig_path, dpi=150, bbox_inches='tight')


def get_tess_lc(row):
    tic = int(row['tic'])
    sec = int(row['sec'])

    fig_path = Path('figs/S' + str(sec) + 'TIC' + str(tic) + '.png')
    star = eleanor.Source(tic=tic, sector=sec)
    lc = eleanor.TargetData(star, height=15, width=15, bkg_size=31, do_pca=True, regressors='corner')
    graph_tess_lc(lc, tic, fig_path)


def process_data(data):
    total = len(data.index)
    for index, row in data.iterrows():
        get_tess_lc(row)
        current = index + 1
        print('TESS LC SAVED: ', current, '/', total)
    # in_ztf(data)
    # in_gaia(data)


def main():
    data = get_data()
    # print(data)
    # columns: 'in_gaia' (boolean), 'in_ztf' (boolean), 'tess_lc' (.png file)
    process_data(data)


if __name__ == '__main__':
    main()
