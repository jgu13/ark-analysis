from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
import umap.umap_ as umap
import os


def plot_dim_reduced_data(component_one, component_two, fig_id, hue, cell_data,
                          title, title_fontsize=24, palette="Spectral", alpha=0.3,
                          legend_type="full", bbox_to_anchor=(1.05, 1), legend_loc=2,
                          legend_borderaxespad=0., save_dir=None, save_file=None):
    """Helper function to visualize_dimensionality_reduction

    Args:
        component_one (pandas.Series):
            the data corresponding to the first component
        component_two (pandas.Series):
            the data corresponding to the second component
        fig_id (int):
            the figure identifier for the visualization
        hue (pandas.Series):
            define the hue for each data point
        cell_data (pandas.DataFrame):
            Dataframe containing columns for dimensionality reduction and category
        title (str):
            the title we wish to set for the graph
        title_fontsize (int):
            the fontsize of the title we want
        palette (str):
            the color palette we wish to visualize with
        alpha (float):
            a value to define the opacity of the points visualized
        legend_type (str):
            what type of legend we wish to specify
        bbox_to_anchor (tuple):
            the bounding box of the legend
        legend_loc (str):
            an string describing where we want the legend located
        legend_borderaxespad (float):
            the pad between the axes and legend border
        save_dir (str):
            Directory to save plots, default is None
        save_file (str):
            If save_dir specified, specify a file name you wish to save to.
            Ignored if save_dir is None
    """

    fig = plt.figure(fig_id)
    sns.scatterplot(x=component_one, y=component_two, hue=hue, palette=palette,
                    data=cell_data, legend=legend_type, alpha=alpha)

    plt.legend(bbox_to_anchor=bbox_to_anchor, loc=legend_loc, borderaxespad=legend_borderaxespad)
    plt.title(title, fontsize=title_fontsize)

    if save_dir is not None:
        if not os.path.exists(save_dir):
            raise ValueError("save_dir %s does not exist" % save_dir)

        if save_file is None:
            raise ValueError("save_dir specified but no save_file specified")

        plt.savefig(os.path.join(save_dir, save_file))


def visualize_dimensionality_reduction(cell_data, columns, category, color_map="Spectral",
                                       algorithm="UMAP", save_dir=None):
    """Plots the dimensionality reduction of specified population columns

    Args:
        cell_data (pandas.DataFrame):
            Dataframe containing columns for dimensionality reduction and category
        columns (list):
            List of column names that are included for dimensionality reduction
        category (str):
            Name of column in dataframe containing population or patient data
        color_map (str):
            Name of MatPlotLib ColorMap used, default is Spectral
        algorithm (str):
            Name of dimensionality reduction algorithm, default is UMAP
        save_dir (str):
            Directory to save plots, default is None
    """

    cell_data = cell_data.dropna()

    # check if the algorithm is valid
    if algorithm not in ["UMAP", "PCA", "tSNE"]:
        raise ValueError(f"The algorithm specified must be one of the following: "
                         f"{['UMAP', 'PCA', 'tSNE']}")

    # set the title of the graph
    graph_title = "%s projection of data" % algorithm

    # create a function mapping from each algorithm name
    # to their respective Python algorithm calls
    dim_red_map = {
        'UMAP': umap.UMAP,
        'PCA': PCA,
        'tSNE': TSNE
    }

    # just map cell_data[columns].values to fit_transform of the dimensionality reduction
    # function if not UMAP, otherwise we will need to run an additional StandardScalar
    # transform beforehand
    dim_red_reducer = dim_red_map[algorithm]()
    dim_red_results = dim_red_reducer.fit_transform(
        cell_data[columns].values if algorithm != 'UMAP'
        else StandardScaler().fit_transform(cell_data[columns].values)
    )

    # now plot the results of the dimensionality reduction
    plot_dim_reduced_data(dim_red_results[:, 0], dim_red_results[:, 1],
                          fig_id=list(dim_red_map.keys()).index(algorithm),
                          hue=cell_data[category], cell_data=cell_data,
                          title=graph_title, save_dir=save_dir,
                          save_file=f"{algorithm}Visualization.png")
