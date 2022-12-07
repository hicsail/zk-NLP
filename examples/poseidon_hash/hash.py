import enum
import numpy as np
import galois

from math import log2, ceil
from typing import Optional

import round_constants as rc
import round_numbers as rn
from miniwizpl import *

class HashType(enum.Enum):
    CONSTINPUTLEN = "ConstInputLen"
    MERKLETREE = "MerkleTree"


def calculate_alpha(p):
    alpha = 2
    while np.gcd(alpha, p-1) != 1:
        alpha += 1
    return alpha

def calculate_length(p):
    security_level = 128
    t = 2
    while 2 ** security_level > p ** t:
        t += 1
    return t

class Poseidon:
    def __init__(self, p, security_level, alpha, input_rate, t, full_round: Optional[int] = None,
                 partial_round: Optional[int] = None, mds_matrix: Optional[list] = None,
                 rc_list: Optional[list] = None, prime_bit_len: Optional[int] = None):
        """

        :param int p: The prime field modulus.
        :param int security_level: The security level measured in bits. Denoted `M` in the Poseidon paper.
        :param int alpha: The power of S-box.
        :param int input_rate: The size of input.
        :param int t: The size of Poseidon's inner state.
        :param int full_round: (optional) Number of full rounds. Denoted `R_F` in the Poseidon paper.
            If parameter is empty it will be calculated.
        :param int partial_round: (optional) Number of partial rounds. Denoted `R_P` in the Poseidon paper.
            If parameter is empty it will be calculated.
        :param list mds_matrix: (optional) 2-dim array of size t*t. Consist of field elements in hex representation.
            Can be calculated.
        :param list rc_list: (optional) List of size t*(full_round + partial_round).
            Consist of field elements in hex representation. Can be calculated.
        :param int prime_bit_len: (optional) The number of bits of the Poseidon prime field modulus. Denoted `n` in
            the Poseidon paper (where `n = ceil(log2(p))`). However for simplicity of calculation, the nearest degree
            of two can be used (for example 256 instead of 255). Using powers of two bits for simplicity when operating
            on bytes as the single bit difference does not affect the round number security properties.
        """
        self.p = p
        self.security_level = security_level

        # TODO: For now alpha is fixed parameter
        # Needed to cast p into an unsigned long
        if np.gcd(alpha, p-1) == 1:
            self.alpha = alpha
        else:
            raise RuntimeError("Not available alpha")

        if prime_bit_len is not None:
            self.prime_bit_len = prime_bit_len
        else:
            self.prime_bit_len = ceil(log2(p))

        # TODO: For now available only for 1 element output.
        self.input_rate = input_rate
        self.t = t

        if 2 ** self.security_level > self.p ** self.t:
            raise RuntimeError("Not secure")

        if (full_round is not None) & (partial_round is not None):
            self.full_round, self.partial_round, self.half_full_round = full_round, partial_round, int(full_round / 2)
        else:
            self.full_round, self.partial_round, self.half_full_round = rn.calc_round_numbers(log2(self.p),
                                                                                              self.security_level,
                                                                                              self.t, self.alpha, True)

        self.field_p = galois.GF(p)

        if mds_matrix is not None:
            if (len(mds_matrix) != self.t) & (len(mds_matrix[0]) != self.t):
                raise ValueError('Invalid size of MDS matrix')
            self.mds_matrix = rc.get_field_matrix_from_hex_matrix(self.field_p, mds_matrix)
        else:
            self.mds_matrix = rc.mds_matrix_generator(self.field_p, self.t)

        if rc_list is not None:
            if len(rc_list) != self.t * (self.full_round + self.partial_round):
                raise ValueError('Invalid number of round constants')
            self.rc_field = self.field_p([int(x, 16) for x in rc_list])
        else:
            self.rc_field = rc.calc_round_constants(self.t, self.full_round, self.partial_round, self.p, self.field_p,
                                                    self.alpha, self.prime_bit_len)

        #self.rc_field = np.array([int(x) for x in self.rc_field])

        #self.mds_matrix = np.array(self.mds_matrix)
        self.state = np.zeros(self.t)
        self.rc_counter = 0

    def s_box(self, element):
        return pow(element, self.alpha, self.p)

    def full_rounds(self):
        for r in range(0, self.half_full_round):
            # add round constants, apply s-box
            for i in range(0, self.t):
                self.state[i] = self.state[i] + self.rc_field[self.rc_counter]
                self.rc_counter += 1

                self.state[i] = self.s_box(self.state[i])

            # apply MDS matrix
            self.state = dot(self.state, self.mds_matrix)

    def partial_rounds(self):
        for r in range(0, self.partial_round):
            # add round constants, apply s-box
            for i in range(0, self.t):
                self.state[i] = self.state[i] + self.rc_field[self.rc_counter]
                self.rc_counter += 1
            self.state[0] = self.s_box(self.state[0])

            # apply MDS matrix
            self.state = dot(self.state, self.mds_matrix)

    def run_hash(self, input_vec: list):
        """

        :param input_vec:
        :return:
        """
        # TODO: This is not right
        if isinstance(input_vec, SecretList):
            new_vec = [SecretInt(v) for v in input_vec.val]
            if len(input_vec.val) < self.t:
                new_vec.extend([0] * (self.t - len(input_vec.val)))
        else:
            new_vec = input_vec
            if len(input_vec) < self.t:
                new_vec.extend([0] * (self.t - len(input_vec)))

        #self.state = self.field_p(new_vec)
        self.state = new_vec
        self.rc_counter = 0

        # First full rounds
        self.full_rounds()
        #print('first round done')
        #output = public_foreach(SecretList(new_vec), self.full_rounds(), 0)
        # Middle partial rounds
        self.partial_rounds()
        #print('second round done')
        #print(self.state)
        #output += public_foreach(SecretList(self.state), self.partial_rounds(), 0)

        # Last full rounds
        self.full_rounds()
        #print('third round done')
        #print(self.state)
        #output += public_foreach(SecretList(self.state), self.full_rounds(), 0)

        return self.state[1]

class OptimizedPoseidon(Poseidon):
    def __init__(self, h_type, p, security_level, alpha, input_rate, t,
                 full_round: Optional[int] = None, partial_round: Optional[int] = None,
                 mds_matrix: Optional[list] = None, rc_list: Optional[list] = None,
                 prime_bit_len: Optional[int] = None):
        """

        :param HashType h_type: Type of input data.
        :param int p: The prime field modulus.
        :param int security_level: The security level measured in bits. Denoted `M` in the Poseidon paper.
        :param int alpha: The power of S-box.
        :param int input_rate: The size of input.
        :param int t: The size of Poseidon's inner state.
        :param int full_round: (optional) Number of full rounds. Denoted `R_F` in the Poseidon paper.
            If parameter is empty it will be calculated.
        :param int partial_round: (optional) Number of partial rounds. Denoted `R_P` in the Poseidon paper.
            If parameter is empty it will be calculated.
        :param list mds_matrix: (optional) 2-dim array of size t*t. Consist of field elements in hex representation.
            Can be calculated.
        :param list rc_list: (optional) List of size t*(full_round + partial_round).
            Consist of field elements in hex representation. Can be calculated.
        :param int prime_bit_len: (optional) The number of bits of the Poseidon prime field modulus. Denoted `n` in
            the Poseidon paper (where `n = ceil(log2(p))`). However for simplicity of calculation, the nearest degree
            of two can be used (for example 256 instead of 255). Using powers of two bits for simplicity when operating
            on bytes as the single bit difference does not affect the round number security properties.
        """
        super().__init__(p, security_level, alpha, input_rate, t, full_round, partial_round,
                         mds_matrix, rc_list, prime_bit_len)
        self.hash_type = h_type

        print("Initialize optimized RC")
        split_rc = [self.field_p(x.tolist()) for x in np.array_split(self.rc_field, len(self.rc_field) / self.t)]
        self.opt_rc_field = rc.optimized_rc(split_rc, self.half_full_round, self.partial_round, self.mds_matrix)
        print("Initialize optimized MDS")
        self.pre_matrix, self.spase_matrices = rc.optimized_matrix(self.mds_matrix, self.partial_round, self.field_p)

    def domain_separation(self, input_vec):
        """

        :param input_vec:
        :return:
        """
        domain_tag = 0
        lv = len(input_vec)
        padding = []
        if self.hash_type == HashType.MERKLETREE:
            domain_tag = 2 ** lv - 1
        elif self.hash_type == HashType.CONSTINPUTLEN:
            domain_tag = lv * (2 ** 64)
            padding = [int(0)] * (self.input_rate - lv)

        return [domain_tag, *input_vec, *padding]

    def full_rounds(self):
        for r in range(0, self.half_full_round - 1):
            # apply s-box, add round constants
            for i in range(0, self.t):
                self.state[i] = self.s_box(self.state[i])
                self.state[i] = self.state[i] + self.opt_rc_field[self.rc_counter]
                self.rc_counter += 1

            self.state = np.dot(self.state, self.mds_matrix)

    def partial_rounds(self):
        for r in range(0, self.partial_round):
            # apply s-box, add round constants
            self.state[0] = self.s_box(self.state[0])
            self.state[0] = self.state[0] + self.opt_rc_field[self.rc_counter]
            self.rc_counter += 1

            # apply MDS matrix
            self.state = np.dot(self.state, self.spase_matrices[r])

    def run_hash(self, input_vec):
        """

        :param input_vec:
        :return:
        """
        if len(input_vec) >= self.t:
            raise ValueError('Invalid length of input data')
        self.rc_counter = 0

        st = self.domain_separation(input_vec)
        self.state = self.field_p(st)

        # add pre-round constant
        for i in range(0, self.t):
            self.state[i] = self.state[i] + self.opt_rc_field[self.rc_counter]
            self.rc_counter += 1

        # First full rounds
        self.full_rounds()

        for i in range(0, self.t):
            self.state[i] = self.s_box(self.state[i])
            self.state[i] = self.state[i] + self.opt_rc_field[self.rc_counter]
            self.rc_counter += 1
        self.state = np.dot(self.state, self.pre_matrix)

        # Middle partial rounds
        self.partial_rounds()

        # Last full rounds
        self.full_rounds()

        # do once for r = R - 1
        for i in range(0, self.t):
            self.state[i] = self.s_box(self.state[i])
        self.state = np.dot(self.state, self.mds_matrix)

        return self.state[1]

