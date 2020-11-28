from typing import List, Tuple, Dict


class ErrorCorrector:

    def __init__(self, block_info: Tuple[int]):
        pass

    def generate_correction_bytes(self):
        pass

    def interleave(self):
        pass

    def get_generator(n: int, log_cache: Dict[int, int]) -> List[int]:
        """
        Computes the coefficients of the ErrorCorrector's generator polynomial.

        The generator polynomial is given by
            g(x) = (x - 2^(n-1))(x - 2^(n-1))...(x - 2^1)(x - 2^0)
        where n is the number of error correction bytes.

        Note that g(x) is an element of GF(2^8)[x].

        Parameters
        ----------
        n : int
            Degree of the generator polynomial.

        Returns
        -------
        List[int]
            The ordered coefficients of the generator polynomial.
        """
        pass


def _create_stores():
    """
    Helper function: creates maps from powers of 2 to the values of their
    exponents in GF(2^8) and vice versa.

    Returns
    -------
    Dict[int, int], Dict[int, int]
        Stores for computed values.
    """
    curr, exp, log = 1, {}, {}

    for k in range(255):
        log[curr], exp[k] = k, curr
        curr *= 2
        if curr > 255:
            curr ^= 285

    exp[255] = 1

    return exp, log
