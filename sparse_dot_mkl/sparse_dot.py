import time
import ctypes as _ctypes
import numpy as np
import scipy.sparse as _spsparse
from scipy.sparse import isspmatrix_csr as is_csr
from numpy.ctypeslib import ndpointer, as_array
from numpy.testing import assert_array_almost_equal


# Load mkl_spblas.so through the common interface
_libmkl = _ctypes.cdll.LoadLibrary("libmkl_rt.so")
NUMPY_FLOAT_DTYPES = [np.float32, np.float64]


class MKL:
    """ This class holds shared object references to C functions with arg and returntypes that can be adjusted"""

    MKL_INT = None
    MKL_INT_NUMPY = None

    # Import function for creating a MKL CSR object
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-create-csr
    _mkl_sparse_d_create_csr = _libmkl.mkl_sparse_d_create_csr

    # Import function for creating a MKL CSR object
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-create-csr
    _mkl_sparse_s_create_csr = _libmkl.mkl_sparse_s_create_csr

    # Import function for creating a MKL CSC object
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-create-csc
    _mkl_sparse_d_create_csc = _libmkl.mkl_sparse_d_create_csc

    # Import function for creating a MKL CSC object
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-create-csc
    _mkl_sparse_s_create_csc = _libmkl.mkl_sparse_s_create_csc

    # Export function for exporting a MKL CSR object
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-export-csr
    _mkl_sparse_d_export_csr = _libmkl.mkl_sparse_d_export_csr

    # Export function for exporting a MKL CSR object
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-export-csr
    _mkl_sparse_s_export_csr = _libmkl.mkl_sparse_s_export_csr

    # Export function for exporting a MKL CSC object
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-export-csc
    _mkl_sparse_d_export_csc = _libmkl.mkl_sparse_d_export_csc

    # Export function for exporting a MKL CSC object
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-export-csc
    _mkl_sparse_s_export_csc = _libmkl.mkl_sparse_s_export_csc

    # Import function for matmul
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-spmm
    _mkl_sparse_spmm = _libmkl.mkl_sparse_spmm

    # Import function for cleaning up MKL objects
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-destroy
    _mkl_sparse_destroy = _libmkl.mkl_sparse_destroy

    # Import function for ordering MKL objects
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-order
    _mkl_sparse_order = _libmkl.mkl_sparse_order

    # Import function for coverting to CSR
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-convert-csr
    _mkl_sparse_convert_csr = _libmkl.mkl_sparse_convert_csr

    @classmethod
    def _set_int_type(cls, c_type, np_type):
        cls.MKL_INT = c_type
        cls.MKL_INT_NUMPY = np_type

        create_argtypes = [_ctypes.POINTER(sparse_matrix_t),
                           _ctypes.c_int,
                           cls.MKL_INT,
                           cls.MKL_INT,
                           ndpointer(dtype=cls.MKL_INT, ndim=1, flags='C_CONTIGUOUS'),
                           ndpointer(dtype=cls.MKL_INT, ndim=1, flags='C_CONTIGUOUS'),
                           ndpointer(dtype=cls.MKL_INT, ndim=1, flags='C_CONTIGUOUS')]

        export_argtypes = [sparse_matrix_t,
                           _ctypes.POINTER(_ctypes.c_int),
                           _ctypes.POINTER(cls.MKL_INT),
                           _ctypes.POINTER(cls.MKL_INT),
                           _ctypes.POINTER(_ctypes.POINTER(cls.MKL_INT)),
                           _ctypes.POINTER(_ctypes.POINTER(cls.MKL_INT)),
                           _ctypes.POINTER(_ctypes.POINTER(cls.MKL_INT))]

        ndpt_double = ndpointer(dtype=_ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')
        ndpt_single = ndpointer(dtype=_ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')

        cls._mkl_sparse_d_create_csr.argtypes = create_argtypes + [ndpt_double]
        cls._mkl_sparse_d_create_csr.restypes = _ctypes.c_int

        cls._mkl_sparse_s_create_csr.argtypes = create_argtypes + [ndpt_single]
        cls._mkl_sparse_s_create_csr.restypes = _ctypes.c_int

        cls._mkl_sparse_d_create_csc.argtypes = create_argtypes + [ndpt_double]
        cls._mkl_sparse_d_create_csc.restypes = _ctypes.c_int

        cls._mkl_sparse_s_create_csc.argtypes = create_argtypes + [ndpt_single]
        cls._mkl_sparse_s_create_csc.restypes = _ctypes.c_int

        cls._mkl_sparse_d_export_csr.argtypes = export_argtypes + [_ctypes.POINTER(_ctypes.POINTER(_ctypes.c_double))]
        cls._mkl_sparse_d_export_csr.restypes = _ctypes.c_int

        cls._mkl_sparse_s_export_csr.argtypes = export_argtypes + [_ctypes.POINTER(_ctypes.POINTER(_ctypes.c_float))]
        cls._mkl_sparse_s_export_csr.restypes = _ctypes.c_int

        cls._mkl_sparse_d_export_csc.argtypes = export_argtypes + [_ctypes.POINTER(_ctypes.POINTER(_ctypes.c_double))]
        cls._mkl_sparse_d_export_csc.restypes = _ctypes.c_int

        cls._mkl_sparse_s_export_csr.argtypes = export_argtypes + [_ctypes.POINTER(_ctypes.POINTER(_ctypes.c_float))]
        cls._mkl_sparse_s_export_csr.restypes = _ctypes.c_int

        cls._mkl_sparse_spmm.argtypes = [_ctypes.c_int,
                                         sparse_matrix_t,
                                         sparse_matrix_t,
                                         _ctypes.POINTER(sparse_matrix_t)]
        cls._mkl_sparse_spmm.restypes = _ctypes.c_int

        cls._mkl_sparse_destroy.argtypes = [sparse_matrix_t]
        cls._mkl_sparse_destroy.restypes = _ctypes.c_int

        cls._mkl_sparse_order.argtypes = [sparse_matrix_t]
        cls._mkl_sparse_order.restypes = _ctypes.c_int

    def __init__(self):
        raise NotImplementedError("This class is not intended to be instanced")


# Construct opaque struct & type
class _sparse_matrix(_ctypes.Structure):
    pass


sparse_matrix_t = _ctypes.POINTER(_sparse_matrix)

# Define standard return codes
RETURN_CODES = {0: "SPARSE_STATUS_SUCCESS",
                1: "SPARSE_STATUS_NOT_INITIALIZED",
                2: "SPARSE_STATUS_ALLOC_FAILED",
                3: "SPARSE_STATUS_INVALID_VALUE",
                4: "SPARSE_STATUS_EXECUTION_FAILED",
                5: "SPARSE_STATUS_INTERNAL_ERROR",
                6: "SPARSE_STATUS_NOT_SUPPORTED"}


def _check_scipy_index_typing(sparse_matrix):
    """
    Ensure that the sparse matrix indicies are in the correct integer type

    :param sparse_matrix: Scipy matrix in CSC or CSR format
    :type sparse_matrix: scipy.sparse.spmatrix
    """

    # Cast indexes to MKL_INT type
    if sparse_matrix.indptr.dtype != MKL.MKL_INT_NUMPY:
        sparse_matrix.indptr = sparse_matrix.indptr.astype(MKL.MKL_INT_NUMPY)
    if sparse_matrix.indices.dtype != MKL.MKL_INT_NUMPY:
        sparse_matrix.indices = sparse_matrix.indices.astype(MKL.MKL_INT_NUMPY)


def _create_mkl_sparse(matrix, cast=False):
    """
    Create MKL internal representation

    :param matrix: Sparse data in CSR or CSC format
    :type matrix: scipy.sparse.spmatrix
    :param cast: If the dtype isn't float32 or float64, cast it to float64.
        Note that this changes the data in the CSR matrix.
    :type cast: bool

    :return ref, double_precision: Handle for the MKL internal representation and boolean for double precision
    :rtype: sparse_matrix_t, float
    """

    # Figure out which dtype for data
    if matrix.dtype == np.float32:
        double_precision = False
    elif matrix.dtype == np.float64:
        double_precision = True
    elif cast:
        matrix.data = matrix.data.astype(np.float64)
        double_precision = True
    else:
        raise ValueError("Only float32 or float64 dtypes are supported")

    # Cast indexes to MKL_INT type
    _check_scipy_index_typing(matrix)

    assert matrix.data.shape[0] == matrix.indices.shape[0]

    if _spsparse.isspmatrix_csr(matrix):
        csr_func = MKL._mkl_sparse_d_create_csr if double_precision else MKL._mkl_sparse_s_create_csr
        assert matrix.indptr.shape[0] == matrix.shape[0] + 1
        return _pass_mkl_handle(matrix, csr_func), double_precision
    elif _spsparse.isspmatrix_csc(matrix):
        assert matrix.indptr.shape[0] == matrix.shape[1] + 1
        csc_func = MKL._mkl_sparse_d_create_csc if double_precision else MKL._mkl_sparse_s_create_csc
        return _pass_mkl_handle(matrix, csc_func), double_precision
    else:
        raise ValueError("Matrix is not CSC or CSR")


def _pass_mkl_handle(data, handle_func):
    """
    Create MKL internal representation

    :param data: Sparse data
    :type data: scipy.sparse.spmatrix
    :return ref: Handle for the MKL internal representation
    :rtype: sparse_matrix_t
    """

    # Create a pointer for the output matrix
    ref = sparse_matrix_t()

    # Load into a MKL data structure and check return
    ret_val = handle_func(_ctypes.byref(ref),
                          _ctypes.c_int(0),
                          MKL.MKL_INT(data.shape[0]),
                          MKL.MKL_INT(data.shape[1]),
                          data.indptr[0:-1],
                          data.indptr[1:],
                          data.indices,
                          data.data)

    # Check return
    if ret_val != 0:
        err_msg = "{fn} returned {v} ({e})".format(fn=handle_func.__name__, v=ret_val, e=RETURN_CODES[ret_val])
        raise ValueError(err_msg)

    return ref


def _export_mkl(csr_mkl_handle, double_precision, output_type="csr", copy=False):
    """
    Export a MKL sparse handle

    :param csr_mkl_handle: Handle for the MKL internal representation
    :type csr_mkl_handle: sparse_matrix_t
    :param double_precision: Use float64 if True, float32 if False. This MUST match the underlying float type - this
        defines a memory view, it does not cast.
    :type double_precision: bool
    :param output_type: The structure of the MKL handle (and therefore the type of scipy sparse to create)
    :type output_type: str
    :param copy: Should the MKL arrays get copied and then explicitly deallocated.
    If set to True, there is a copy, but there is less risk of memory leaking.
    If set to False, numpy arrays will be created from C pointers without a copy.
    I don't know if these arrays will be garbage collected correctly by python.
    They seem to, so this defaults to False.
    :type copy: bool

    :return:
    """

    # Create the pointers for the output data
    indptrb = _ctypes.POINTER(MKL.MKL_INT)()
    indptren = _ctypes.POINTER(MKL.MKL_INT)()
    indices = _ctypes.POINTER(MKL.MKL_INT)()

    ordering = _ctypes.c_int()
    nrows = MKL.MKL_INT()
    ncols = MKL.MKL_INT()

    output_type = output_type.lower()

    if output_type == "csr":
        out_func = MKL._mkl_sparse_d_export_csr if double_precision else MKL._mkl_sparse_s_export_csr
        sp_matrix_constructor = _spsparse.csr_matrix
    elif output_type == "csc":
        out_func = MKL._mkl_sparse_d_export_csc if double_precision else MKL._mkl_sparse_s_export_csc
        sp_matrix_constructor = _spsparse.csc_matrix
    else:
        raise ValueError("Only CSR and CSC output types are supported")

    if double_precision:
        data = _ctypes.POINTER(_ctypes.c_double)()
        final_dtype = np.float64
    else:
        data = _ctypes.POINTER(_ctypes.c_float)()
        final_dtype = np.float32

    ret_val = out_func(csr_mkl_handle,
                       _ctypes.byref(ordering),
                       _ctypes.byref(nrows),
                       _ctypes.byref(ncols),
                       _ctypes.byref(indptrb),
                       _ctypes.byref(indptren),
                       _ctypes.byref(indices),
                       _ctypes.byref(data))

    # Check return
    if ret_val != 0:
        err_msg = "{fn} returned {v} ({e})".format(fn=out_func.__name__, v=ret_val, e=RETURN_CODES[ret_val])
        raise ValueError(err_msg)

    # Check ordering
    if ordering.value != 0:
        raise ValueError("1-indexing (F-style) is not supported")

    # Get matrix dims
    ncols = ncols.value
    nrows = nrows.value

    # If any axis is 0 return an empty matrix
    if nrows == 0 or ncols == 0:
        return sp_matrix_constructor((nrows, ncols), dtype=final_dtype)

    # Get the index dimension
    index_dim = nrows if output_type == "csr" else ncols

    # Construct a numpy array and add 0 to first position for scipy.sparse's 3-array indexing
    indptrb = as_array(indptrb, shape=(index_dim,))
    indptren = as_array(indptren, shape=(index_dim,))

    indptren = np.insert(indptren, 0, indptrb[0])
    nnz = indptren[-1] - indptrb[0]

    # If there are no non-zeros, return an empty matrix
    # If the number of non-zeros is insane, raise a ValueError
    if nnz == 0:
        return sp_matrix_constructor((nrows, ncols), dtype=final_dtype)
    elif nnz < 0 or nnz > ncols * nrows:
        raise ValueError("Matrix ({m} x {n}) is attempting to index {z} elements".format(m=nrows, n=ncols, z=nnz))

    # Construct numpy arrays from data pointer and from indicies pointer
    data = np.array(as_array(data, shape=(nnz,)), copy=copy)
    indices = np.array(as_array(indices, shape=(nnz,)), copy=copy)

    # Pack and return the matrix
    return sp_matrix_constructor((data, indices, indptren), shape=(nrows, ncols))


def _matmul_mkl(mat_ref_a, mat_ref_b, sp_ref_a, sp_ref_b):
    """
    Dot product two MKL objects together and return a handle to the result

    :param sp_ref_a: Sparse matrix A handle
    :type sp_ref_a: sparse_matrix_t
    :param sp_ref_b: Sparse matrix B handle
    :param sp_ref_b: sparse_matrix_t
    :return: Sparse matrix handle that is the dot product A * B
    :rtype: sparse_matrix_t
    """

    ref_handle = sparse_matrix_t()
    ret_val = MKL._mkl_sparse_spmm(_ctypes.c_int(10),
                                   sp_ref_a,
                                   sp_ref_b,
                                   _ctypes.byref(ref_handle))

    # Check return
    if ret_val != 0:
        raise ValueError("mkl_sparse_spmm returned {v} ({e})".format(v=ret_val, e=RETURN_CODES[ret_val]))

    assert mat_ref_a.data.shape[0] == mat_ref_a.indices.shape[0]
    assert mat_ref_b.data.shape[0] == mat_ref_b.indices.shape[0]

    return ref_handle


def _destroy_mkl_handle(ref_handle):
    """
    Deallocate a MKL sparse handle

    :param ref_handle:
    :type ref_handle: sparse_matrix_t
    :return:
    """

    ret_val = MKL._mkl_sparse_destroy(ref_handle)

    if ret_val != 0:
        raise ValueError("mkl_sparse_destroy returned {v} ({e})".format(v=ret_val, e=RETURN_CODES[ret_val]))


def _order_mkl_handle(ref_handle):
    """
    Reorder indexes in a MKL sparse handle

    :param ref_handle:
    :type ref_handle: sparse_matrix_t
    :return:
    """

    ret_val = MKL._mkl_sparse_order(ref_handle)

    if ret_val != 0:
        raise ValueError("mkl_sparse_order returned {v} ({e})".format(v=ret_val, e=RETURN_CODES[ret_val]))


def _convert_to_csr(ref_handle):
    """
    Convert a MKL sparse handle to CSR format

    :param ref_handle:
    :type ref_handle: sparse_matrix_t
    :return:
    """

    csr_ref = sparse_matrix_t()

    if MKL._mkl_sparse_convert_csr(ref_handle, _ctypes.c_int(10), _ctypes.byref(csr_ref)) != 0:
        _destroy_mkl_handle(csr_ref)
        raise ValueError("CSC to CSR Conversion failed")

    return csr_ref


def _validate_dtype():
    """
    Test to make sure that this library works by creating a random sparse array in CSC format,
    then converting it to CSR format and making sure is has not raised an exception.

    """

    test_array = _spsparse.random(5, 5, density=0.5, format="csc", dtype=np.float32, random_state=50)
    test_comparison = test_array.A

    csc_ref, precision_flag = _create_mkl_sparse(test_array)

    csr_ref = _convert_to_csr(csc_ref)
    final_array = _export_mkl(csr_ref, precision_flag)
    assert_array_almost_equal(test_comparison, final_array.A)


# Define dtypes empirically
# Basically just try with int64s and if that doesn't work try with int32s
if MKL.MKL_INT is None:

    MKL._set_int_type(_ctypes.c_longlong, np.int64)

    try:
        _validate_dtype()
    except (AssertionError, ValueError) as err:

        MKL._set_int_type(_ctypes.c_int, np.int32)

        try:
            _validate_dtype()
        except (AssertionError, ValueError):
            raise ImportError("Unable to set MKL numeric types")


def dot_product_mkl(matrix_a, matrix_b, cast=False, copy=False, reorder_output=False, debug=False):
    """
    Multiply together two scipy sparse matrixes using the intel Math Kernel Library.
    This currently only supports float32 and float64 data

    :param matrix_a: Sparse matrix A in CSC/CSR format
    :type matrix_a: scipy.sparse.spmatrix
    :param matrix_b: Sparse matrix B in CSC/CSR format
    :type matrix_b: scipy.sparse.spmatrix
    :param cast: Should the data be coerced into float64 if it isn't float32 or float64
    If set to True and any other dtype is passed, the matrix data will be modified in-place
    If set to False and any dtype that isn't float32 or float64 is passed, a ValueError will be raised
    Defaults to False
    :param copy: Should the MKL arrays get copied and then explicitly deallocated.
    If set to True, there is a copy, but there is less risk of memory leaking.
    If set to False, numpy arrays will be created from C pointers without a copy.
    I don't know if these arrays will be garbage collected correctly by python.
    They seem to, so this defaults to False.
    :type copy: bool
    :param reorder_output: Should the array indices be reordered using MKL
    If set to True, the object in C will be ordered and then exported into python
    If set to False, the array column indices will not be ordered.
    The scipy sparse dot product does not yield ordered column indices so this defaults to False
    :type reorder_output: bool
    :param debug: Should debug and timing messages be printed. Defaults to false.
    :type debug: bool
    :return: Sparse matrix that is the result of A * B in CSR format
    :rtype: scipy.sparse.csr_matrix
    """

    dprint = print if debug else lambda x: x

    # Check for allowed sparse matrix types
    if not is_csr(matrix_a) or not is_csr(matrix_b):
        raise ValueError("Both input matrices to csr_dot_product_mkl must be CSR")

    # Check to make sure that this multiplication can work
    if matrix_a.shape[1] != matrix_b.shape[0]:
        err_msg = "Matrix alignment error: {m1} * {m2}".format(m1=matrix_a.shape, m2=matrix_b.shape)
        raise ValueError(err_msg)

    # Check for edge condition inputs which result in empty outputs
    if min(matrix_a.shape[0],
           matrix_a.shape[1],
           matrix_b.shape[0],
           matrix_b.shape[1],
           matrix_a.data.shape[0],
           matrix_b.data.shape[0],
           matrix_a.indices.shape[0],
           matrix_b.indices.shape[0]) == 0:

        final_dtype = np.float64 if matrix_a.dtype != matrix_b.dtype or matrix_a.dtype != np.float32 else np.float32
        return _spsparse.csr_matrix((matrix_a.shape[0], matrix_b.shape[0]), dtype=final_dtype)

    # Check dtypes
    if matrix_a.dtype != matrix_b.dtype and cast:
        dprint("Recasting matrix data types {a} and {b} to np.float64".format(a=matrix_a.data.dtype,
                                                                              b=matrix_b.data.dtype))
        matrix_a.data = matrix_a.data if matrix_a.dtype == np.float64 else matrix_a.data.astype(np.float64)
        matrix_b.data = matrix_b.data if matrix_b.dtype == np.float64 else matrix_b.data.astype(np.float64)
    elif matrix_a.dtype != matrix_b.dtype:
        err_msg = "Matrix data types must be in concordance; {a} and {b} provided".format(a=matrix_a.dtype,
                                                                                          b=matrix_b.dtype)
        raise ValueError(err_msg)

    if debug:
        stat_str = "\tMin: {mi:.4f}, Max: {ma:.4f}, Density: {d:.4f}, Data Type: {t}, Index Type: {it}"
        dprint("Matrix A: {sh}, ({nnz} nnz), ({nr} leading axis index)".format(sh=matrix_a.shape,
                                                                               nnz=matrix_a.data.shape[0],
                                                                               nr=matrix_a.indptr.shape[0]))
        dprint(stat_str.format(mi=matrix_a.data.min(),
                               ma=matrix_a.data.max(),
                               t=matrix_a.data.dtype,
                               it=matrix_a.indices.dtype,
                               d=matrix_a.data.shape[0] / (matrix_a.shape[0] * matrix_a.shape[1])))

        dprint("Matrix B: {sh}, ({nnz} nnz), ({nr} leading axis index)".format(sh=matrix_b.shape,
                                                                               nnz=matrix_b.data.shape[0],
                                                                               nr=matrix_b.indptr.shape[0]))
        dprint(stat_str.format(mi=matrix_b.data.min(),
                               ma=matrix_b.data.max(),
                               t=matrix_b.data.dtype,
                               it=matrix_b.indices.dtype,
                               d=matrix_b.data.shape[0] / (matrix_b.shape[0] * matrix_b.shape[1])))

    t0 = time.time()

    # Create intel MKL objects
    mkl_a, a_dbl = _create_mkl_sparse(matrix_a, cast=cast)
    mkl_b, b_dbl = _create_mkl_sparse(matrix_b, cast=cast)

    _order_mkl_handle(mkl_a)
    _order_mkl_handle(mkl_b)

    if debug:
        t0_1 = time.time()
        dprint("Created MKL sparse handles: {0:.6f} seconds".format(t0_1 - t0))

        dbg_a = _export_mkl(mkl_a, a_dbl, copy=False, output_type="csr" if is_csr(matrix_a) else "csc")
        dbg_b = _export_mkl(mkl_b, b_dbl, copy=False, output_type="csr" if is_csr(matrix_b) else "csc")

        assert dbg_a.shape == matrix_a.shape
        assert dbg_b.shape == matrix_b.shape

        dprint("\tMatrix A: {n} / {sz} non-finite".format(n=(~np.isfinite(dbg_a.data)).sum(),
                                                          sz=dbg_a.shape[0] * dbg_a.shape[1]))
        dprint("\tMatrix B: {n} / {sz} non-finite".format(n=(~np.isfinite(dbg_b.data)).sum(),
                                                          sz=dbg_b.shape[0] * dbg_b.shape[1]))

        dprint("Validated MKL sparse handles: {0:.6f} seconds".format(time.time() - t0_1))

    t1 = time.time()

    # Dot product
    mkl_c = _matmul_mkl(matrix_a, matrix_b, mkl_a, mkl_b)

    t2 = time.time()
    dprint("Multiplied matrices: {0:.6f} seconds".format(t2 - t1))

    # Reorder
    if reorder_output:
        _order_mkl_handle(mkl_c)

        t2_1 = time.time()
        dprint("Reordered indicies: {0:.6f} seconds".format(t2_1 - t2))
        t2 = t2_1

    # Extract
    python_c = _export_mkl(mkl_c, a_dbl or b_dbl, copy=copy, output_type="csr")

    t3 = time.time()
    dprint("Created python handle: {0:.6f} seconds".format(t3 - t2))

    if debug:
        stat_str = "\tMin: {mi:.4f}, Max: {ma:.4f}, Density: {d:.4f}, Data Type: {t}, Index Type: {it}"
        dprint("Output: {sh}, ({nnz} nnz), ({nr} leading axis index)".format(sh=python_c.shape,
                                                                             nnz=python_c.data.shape[0],
                                                                             nr=python_c.indptr.shape[0]))
        dprint(stat_str.format(mi=python_c.data.min(),
                               ma=python_c.data.max(),
                               t=python_c.data.dtype,
                               it=python_c.indices.dtype,
                               d=python_c.data.shape[0] / (python_c.shape[0] * python_c.shape[1])))

    # Destroy
    if copy:
        _destroy_mkl_handle(mkl_c)

        t4 = time.time()
        dprint("Cleaned up MKL object: {0:.6f} seconds".format(t4 - t3))

    return python_c