import numpy as np
from nose.tools import assert_true, assert_false, assert_equal, assert_almost_equal, assert_raises
from numpy.testing import assert_array_equal
from dipy.reconst.recspeed import (peak_finding, local_maxima,
                                   remove_similar_vertices)
from dipy.data import get_sphere, get_data
from dipy.core.sphere import reduce_antipodal, unique_edges
from dipy.sims.voxel import all_tensor_evecs, multi_tensor_odf

def test_local_maxima():
    vertices, faces=get_sphere('symmetric724')
    edges = unique_edges(faces)
    odf = abs(vertices.sum(-1))
    odf[1] = 10.
    odf[143] = 143.
    odf[505] = 505

    peak_values, peak_index = local_maxima(odf, edges)
    assert_array_equal(peak_values, [505, 143, 10])
    assert_array_equal(peak_index, [505, 143, 1])

    vertices_half, edges_half, faces_half = reduce_antipodal(vertices, faces)
    odf = abs(vertices_half.sum(-1))
    odf[1] = 10.
    odf[143] = 143.

    peak_value, peak_index = local_maxima(odf, edges_half)
    assert_array_equal(peak_value, [143, 10])
    assert_array_equal(peak_index, [143, 1])

    odf[20] = np.nan
    assert_raises(ValueError, local_maxima, odf, edges_half)

def test_peak_finding():

    vertices, faces=get_sphere('symmetric724')
    odf=np.zeros(len(vertices))
    odf = np.abs(vertices.sum(-1))

    odf[1] = 10.
    odf[505] = 505.
    odf[143] = 143.

    peaks, inds=peak_finding(odf.astype('f8'), faces.astype('uint16'))
    print peaks, inds
    edges = unique_edges(faces)
    peaks, inds = local_maxima(odf, edges)
    print peaks, inds
    vertices_half, edges_half, faces_half = reduce_antipodal(vertices, faces)
    n = len(vertices_half)
    peaks, inds = local_maxima(odf[:n], edges_half)
    print peaks, inds
    mevals=np.array(([0.0015,0.0003,0.0003],
                    [0.0015,0.0003,0.0003]))
    e0=np.array([1,0,0.])
    e1=np.array([0.,1,0])
    mevecs=[all_tensor_evecs(e0),all_tensor_evecs(e1)]
    odf = multi_tensor_odf(vertices, [0.5,0.5], mevals, mevecs)
    peaks, inds=peak_finding(odf, faces)
    print peaks, inds
    peaks2, inds2 = local_maxima(odf[:n], edges_half)
    print peaks2, inds2
    assert_equal(len(peaks), 2)
    assert_equal(len(peaks2), 2)

def test_filter_peaks():
    vertices = np.array([[1., 0., 0.],
                         [0., 1., 0.],
                         [0., 0., 1.],
                         [1.1, 1., 0.],
                         [0., 2., 1.],
                         [2., 1., 0.],
                         [1., 0., 0.]])
    norms = np.sqrt((vertices*vertices).sum(-1))
    vertices = vertices/norms[:, None]

    uv, mapping = remove_similar_vertices(vertices, .01)
    assert_array_equal(uv, vertices[:6])
    assert_array_equal(mapping, range(6) + [0])
    uv, mapping = remove_similar_vertices(vertices, 30)
    assert_array_equal(uv, vertices[:4])
    assert_array_equal(mapping, range(4) + [1, 0, 0])
    uv, mapping = remove_similar_vertices(vertices, 60)
    assert_array_equal(uv, vertices[:3])
    assert_array_equal(mapping, range(3) + [0, 1, 0, 0])

if __name__ == '__main__':
    test_peak_finding()

