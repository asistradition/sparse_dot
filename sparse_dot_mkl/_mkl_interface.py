import ctypes as _ctypes
import numpy as np
import scipy.sparse as _spsparse
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

    # Import function for matmul single dense
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-spmm
    _mkl_sparse_s_spmmd = _libmkl.mkl_sparse_s_spmmd

    # Import function for matmul double dense
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-spmm
    _mkl_sparse_d_spmmd = _libmkl.mkl_sparse_d_spmmd

    # Import function for matmul single sparse*dense
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-mm
    _mkl_sparse_s_mm = _libmkl.mkl_sparse_s_mm

    # Import function for matmul double sparse*dense
    # https://software.intel.com/en-us/mkl-developer-reference-c-mkl-sparse-mm
    _mkl_sparse_d_mm = _libmkl.mkl_sparse_d_mm

    # Import function for matmul single dense*dense
    # https://software.intel.com/en-us/mkl-developer-reference-c-cblas-gemm
    _cblas_sgemm = _libmkl.cblas_sgemm

    # Import function for matmul double dense*dense
    # https://software.intel.com/en-us/mkl-developer-reference-c-cblas-gemm
    _cblas_dgemm = _libmkl.cblas_dgemm

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

        cls._mkl_sparse_s_spmmd.argtypes = [_ctypes.c_int,
                                            sparse_matrix_t,
                                            sparse_matrix_t,
                                            _ctypes.c_int,
                                            _ctypes.POINTER(_ctypes.c_float),
                                            MKL.MKL_INT]
        cls._mkl_sparse_s_spmmd.restypes = _ctypes.c_int

        cls._mkl_sparse_d_spmmd.argtypes = [_ctypes.c_int,
                                            sparse_matrix_t,
                                            sparse_matrix_t,
                                            _ctypes.c_int,
                                            _ctypes.POINTER(_ctypes.c_double),
                                            MKL.MKL_INT]
        cls._mkl_sparse_d_spmmd.restypes = _ctypes.c_int

        cls._mkl_sparse_s_mm.argtypes = [_ctypes.c_int,
                                         _ctypes.c_float,
                                         sparse_matrix_t,
                                         matrix_descr,
                                         _ctypes.c_int,
                                         ndpointer(dtype=_ctypes.c_float, ndim=2, flags='C_CONTIGUOUS'),
                                         MKL.MKL_INT,
                                         MKL.MKL_INT,
                                         _ctypes.c_float,
                                         _ctypes.POINTER(_ctypes.c_float),
                                         MKL.MKL_INT]
        cls._mkl_sparse_s_mm.restypes = _ctypes.c_int

        cls._mkl_sparse_d_mm.argtypes = [_ctypes.c_int,
                                         _ctypes.c_double,
                                         sparse_matrix_t,
                                         matrix_descr,
                                         _ctypes.c_int,
                                         ndpointer(dtype=_ctypes.c_double, ndim=2, flags='C_CONTIGUOUS'),
                                         MKL.MKL_INT,
                                         MKL.MKL_INT,
                                         _ctypes.c_double,
                                         _ctypes.POINTER(_ctypes.c_double),
                                         MKL.MKL_INT]
        cls._mkl_sparse_d_mm.restypes = _ctypes.c_int

        cls._cblas_sgemm.argtypes = [_ctypes.c_int,
                                     _ctypes.c_int,
                                     _ctypes.c_int,
                                     MKL.MKL_INT,
                                     MKL.MKL_INT,
                                     MKL.MKL_INT,
                                     _ctypes.c_float,
                                     ndpointer(dtype=_ctypes.c_float, ndim=2, flags='C_CONTIGUOUS'),
                                     MKL.MKL_INT,
                                     ndpointer(dtype=_ctypes.c_float, ndim=2, flags='C_CONTIGUOUS'),
                                     MKL.MKL_INT,
                                     _ctypes.c_float,
                                     _ctypes.POINTER(_ctypes.c_float),
                                     MKL.MKL_INT]
        cls._cblas_sgemm.restypes = None

        cls._cblas_dgemm.argtypes = [_ctypes.c_int,
                                     _ctypes.c_int,
                                     _ctypes.c_int,
                                     MKL.MKL_INT,
                                     MKL.MKL_INT,
                                     MKL.MKL_INT,
                                     _ctypes.c_double,
                                     ndpointer(dtype=_ctypes.c_double, ndim=2, flags='C_CONTIGUOUS'),
                                     MKL.MKL_INT,
                                     ndpointer(dtype=_ctypes.c_double, ndim=2, flags='C_CONTIGUOUS'),
                                     MKL.MKL_INT,
                                     _ctypes.c_double,
                                     _ctypes.POINTER(_ctypes.c_double),
                                     MKL.MKL_INT]
        cls._cblas_dgemm.restypes = None

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


# Matrix description struct
class matrix_descr(_ctypes.Structure):
    _fields_ = [("sparse_matrix_type_t", _ctypes.c_int),
                ("sparse_fill_mode_t", _ctypes.c_int),
                ("sparse_diag_type_t", _ctypes.c_int)]

    def __init__(self, sparse_matrix_type_t=20, sparse_fill_mode_t=0, sparse_diag_type_t=0):
        super(matrix_descr, self).__init__(sparse_matrix_type_t, sparse_fill_mode_t, sparse_diag_type_t)


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


def _create_mkl_sparse(matrix):
    """
    Create MKL internal representation

    :param matrix: Sparse data in CSR or CSC format
    :type matrix: scipy.sparse.spmatrix

    :return ref, double_precision: Handle for the MKL internal representation and boolean for double precision
    :rtype: sparse_matrix_t, float
    """

    # Figure out which dtype for data
    if matrix.dtype == np.float32:
        double_precision = False
    elif matrix.dtype == np.float64:
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


def _export_mkl(csr_mkl_handle, double_precision, output_type="csr"):
    """
    Export a MKL sparse handle

    :param csr_mkl_handle: Handle for the MKL internal representation
    :type csr_mkl_handle: sparse_matrix_t
    :param double_precision: Use float64 if True, float32 if False. This MUST match the underlying float type - this
        defines a memory view, it does not cast.
    :type double_precision: bool
    :param output_type: The structure of the MKL handle (and therefore the type of scipy sparse to create)
    :type output_type: str

    :return: Sparse matrix in scipy format
    :rtype: scipy.spmatrix
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
    data = np.array(as_array(data, shape=(nnz,)), copy=True)
    indices = np.array(as_array(indices, shape=(nnz,)), copy=True)

    # Pack and return the matrix
    return sp_matrix_constructor((data, indices, indptren), shape=(nrows, ncols))


def _destroy_mkl_handle(ref_handle):
    """
    Deallocate a MKL sparse handle

    :param ref_handle:
    :type ref_handle: sparse_matrix_t
    """

    ret_val = MKL._mkl_sparse_destroy(ref_handle)

    if ret_val != 0:
        raise ValueError("mkl_sparse_destroy returned {v} ({e})".format(v=ret_val, e=RETURN_CODES[ret_val]))


def _order_mkl_handle(ref_handle):
    """
    Reorder indexes in a MKL sparse handle

    :param ref_handle:
    :type ref_handle: sparse_matrix_t
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


def _matrix_stats(matrix, name="", pfunc=print):
    stat_str = "\tMin: {mi:.4f}, Max: {ma:.4f}, Density: {d:.4f}, Data Type: {t}, Index Type: {it}"
    pfunc("Matrix {name}: {sh}, ({nnz} nnz), ({nr} leading axis index)".format(name=name,
                                                                               sh=matrix.shape,
                                                                               nnz=matrix.data.shape[0],
                                                                               nr=matrix.indptr.shape[0]))
    pfunc(stat_str.format(mi=matrix.data.min(),
                          ma=matrix.data.max(),
                          t=matrix.data.dtype,
                          it=matrix.indices.dtype,
                          d=matrix.data.shape[0] / (matrix.shape[0] * matrix.shape[1])))


def _sanity_check(matrix_a, matrix_b):

    # Check to make sure that this multiplication can work
    if matrix_a.shape[1] != matrix_b.shape[0]:
        err_msg = "Matrix alignment error: {m1} * {m2}".format(m1=matrix_a.shape, m2=matrix_b.shape)
        raise ValueError(err_msg)


def _cast_to_float64(matrix):
    if _spsparse.issparse(matrix) and matrix.data.dtype != np.float64:
        matrix.data = matrix.data.astype(np.float64)
    elif matrix.dtype != np.float64:
        matrix = matrix.astype(np.float64)

    return matrix


def _type_check(matrix_a, matrix_b, cast=False, dprint=print):

    # Check dtypes
    if matrix_a.dtype == np.float32 and matrix_b.dtype == np.float32:
        return matrix_a, matrix_b

    elif matrix_a.dtype == np.float64 and matrix_b.dtype == np.float64:
        return matrix_a, matrix_b

    elif (matrix_a.dtype != np.float64 or matrix_b.dtype != np.float64) and cast:
        dprint("Recasting matrix data types {a} and {b} to np.float64".format(a=matrix_a.dtype,
                                                                              b=matrix_b.dtype))
        return _cast_to_float64(matrix_a), _cast_to_float64(matrix_b)

    elif matrix_a.dtype != np.float64 or matrix_b.dtype != np.float64:
        err_msg = "Matrix data types must be in concordance; {a} and {b} provided".format(a=matrix_a.dtype,
                                                                                          b=matrix_b.dtype)
        raise ValueError(err_msg)


def _empty_output_check(matrix_a, matrix_b):
    # Check for edge condition inputs which result in empty outputs
    if min(matrix_a.shape[0],
           matrix_a.shape[1],
           matrix_b.shape[0],
           matrix_b.shape[1]) == 0:
        return True
    elif _spsparse.issparse(matrix_a) and min(matrix_a.data.shape[0], matrix_a.indices.shape[0]) == 0:
        return True
    elif _spsparse.issparse(matrix_b) and min(matrix_b.data.shape[0], matrix_b.indices.shape[0]) == 0:
        return True
    else:
        return False


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