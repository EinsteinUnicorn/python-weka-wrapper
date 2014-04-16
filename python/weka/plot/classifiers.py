# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# classifiers.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import matplotlib.pyplot as plt
from weka.classifiers import NumericPrediction
from pygraphviz.agraph import AGraph
import tempfile
from PIL import Image


def plot_classifier_errors(predictions, absolute=True, max_relative_size=20, outfile=None):
    """
    Plots the classifers for the given list of predictions.
    NB: The plot window blocks execution till closed.
    :param predictions: the predictions to plot
    :param absolute: whether to use absolute errors as size or relative ones
    """
    actual    = []
    predicted = []
    error     = None
    for pred in predictions:
        actual.append(pred.actual())
        predicted.append(pred.predicted())
        if isinstance(pred, NumericPrediction):
            if error is None:
                error = []
            error.append(abs(pred.error()))
    fig, ax = plt.subplots()
    if error is None:
        ax.scatter(actual, predicted)
    else:
        if not absolute:
            min_err = min(error)
            max_err = max(error)
            factor  = (max_err  - min_err) / max_relative_size
            for i in xrange(len(error)):
                error[i] = error[i] / factor * max_relative_size
        ax.scatter(actual, predicted, s=error)
    ax.set_xlabel("actual")
    ax.set_ylabel("predicted")
    ax.set_title("Classifier errors")
    ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c="0.3")
    ax.grid(True)
    plt.draw()
    if not outfile is None:
        plt.savefig(outfile)
    plt.show()


def plot_dot_graph(graph, filename=None):
    """
    Plots a graph in graphviz dot notation.
    :param graph: the dot notation graph
    :param filename: the (optional) file to save the generated plot to. The extension determines the file format.
    """
    agraph = AGraph(graph)
    agraph.layout(prog='dot')
    if filename is None:
        filename = tempfile.mktemp(suffix=".png")
    agraph.draw(filename)
    image = Image.open(filename)
    image.show()