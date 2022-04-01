#include "emp-zk/emp-zk.h"
#include <iostream>
#include "emp-tool/emp-tool.h"
#include "ram-zk/ro-zk-mem.h"
#include "matrix.h"
using namespace emp;
using namespace std;

int port, party;
const int threads = 1;
const int index_sz = 20, val_sz = 32;

QSMatrix<Float> relu(const QSMatrix<Float>& mat) {
  unsigned rows = mat.get_rows();
  unsigned cols = mat.get_cols();

  QSMatrix<Float> result(rows, cols, 0.0);
  Float zero = Float(0.0, PUBLIC);

  for (unsigned i=0; i<rows; i++) {
    for (unsigned j=0; j<cols; j++) {
      Float val = mat(i, j);
      Bit t = zero.less_equal(val);
      result(i,j) = val.If(t, zero);
    }
  }

  return result;
}

// *************************************************************************

void test(BoolIO<NetIO> *ios[threads], int party) {
  setup_zk_bool<BoolIO<NetIO>>(ios, threads, party);

  cout << "!!\n";

  Float pub_zero = Float(0.0, PUBLIC);


  float mat_1_init[1][7] = {{-9, -7, -7, -9, -1, 0, -3}};
  QSMatrix<Float> mat_1(1, 7, pub_zero);
  for (int i = 0; i < 1; ++i)
    for (int j = 0; j < 7; ++j) {
      mat_1(i, j) = Float(mat_1_init[i][j], ALICE);
    }


  float mat_2_init[7][12] = {{6, -7, -2, -7, -3, -2, 1, 8, 3, 0, -1, -2}, {7, 5, 8, -5, -3, -5, -10, -8, -4, -10, 3, 2}, {5, -10, -8, -7, -6, -5, -3, 1, -8, 9, 0, -3}, {3, 7, 4, -10, -5, 3, 1, 9, 0, -2, -7, 7}, {-1, -6, 0, -6, -1, 5, -9, -5, 3, 4, -6, -3}, {-6, 8, -1, -9, 3, -7, 8, -8, 2, -5, -8, 6}, {9, -10, 6, -2, -6, 0, -5, 7, -1, 3, 4, 3}};
  QSMatrix<Float> mat_2(7, 12, pub_zero);
  for (int i = 0; i < 7; ++i)
    for (int j = 0; j < 12; ++j) {
      mat_2(i, j) = Float(mat_2_init[i][j], ALICE);
    }


  float mat_3_init[12][12] = {{-1, -9, 9, -1, 7, 0, 5, 8, -8, 2, -8, -8}, {8, 3, 8, 5, 5, 1, -1, -4, 1, 9, 1, -5}, {2, -4, 8, -9, -2, -5, -1, 8, 9, -7, -3, 5}, {7, -6, 0, -7, -7, -9, -6, 4, 3, -9, 9, -3}, {-4, -1, -2, 6, -5, -7, 5, -4, -10, 2, 5, -5}, {8, 8, -2, -10, 8, -9, 0, -1, 7, -10, 0, 1}, {6, 2, -4, -8, 9, 6, -7, -6, -3, -5, -10, -2}, {-1, -7, 2, 7, 3, -10, -2, 1, 8, 6, -1, -8}, {-6, -1, -3, -6, 9, 3, -6, 1, -7, -9, 5, -1}, {1, 7, -7, -3, -6, -10, -1, -10, 1, -10, -5, 6}, {-4, 4, -8, 5, -9, 3, 0, 8, -4, 5, 3, -10}, {-8, 2, 4, 4, -7, -9, -3, 7, -7, 4, 0, 3}};
  QSMatrix<Float> mat_3(12, 12, pub_zero);
  for (int i = 0; i < 12; ++i)
    for (int j = 0; j < 12; ++j) {
      mat_3(i, j) = Float(mat_3_init[i][j], ALICE);
    }


  float mat_4_init[12][12] = {{3, -5, -9, -10, -1, -1, 0, 5, 2, 3, 4, 1}, {-4, 7, -1, 7, 5, 3, -1, -10, 1, -3, -10, 8}, {4, 4, -4, 3, -8, 1, 5, 8, 3, -9, 4, 5}, {0, -8, 7, -4, -7, -6, 0, 5, -4, -7, 2, 0}, {-9, -9, 1, 7, 9, -10, 3, 4, -1, -10, 9, 5}, {2, -2, 8, -2, 5, -8, 0, 8, 1, 6, 9, -4}, {-4, -8, -6, -10, -4, 4, 2, 6, 8, 6, 2, 3}, {7, 4, 2, 6, 4, 9, 2, -5, 4, 3, -8, 6}, {1, 1, 9, -1, 2, -4, -4, 7, 5, -4, -7, -5}, {-4, 3, -8, 0, 8, 6, 7, -5, 7, 5, 5, 7}, {-1, -6, 6, -10, 3, 6, 0, -9, 9, -8, 9, -8}, {6, 4, 8, -7, 0, 7, 0, 6, 6, 4, 0, 5}};
  QSMatrix<Float> mat_4(12, 12, pub_zero);
  for (int i = 0; i < 12; ++i)
    for (int j = 0; j < 12; ++j) {
      mat_4(i, j) = Float(mat_4_init[i][j], ALICE);
    }


  float mat_5_init[12][12] = {{-2, 7, -9, -4, -10, -2, 2, 6, -6, -9, 4, -9}, {3, -3, -3, 8, -2, 4, 0, 3, 4, -3, -10, 1}, {-7, -3, -9, -10, 2, -6, 8, 9, -6, -6, -4, 0}, {-3, 1, 0, -3, 5, -2, -1, 3, 9, -8, 9, -4}, {-5, 5, 3, -10, -1, 3, -10, -8, 2, 1, -8, 0}, {4, -10, -1, 5, 0, 0, -6, 6, 6, 2, -4, -9}, {-10, 4, 2, 6, 2, -9, -6, -8, 5, -4, -5, 8}, {6, 6, -2, 1, 6, 7, -5, 6, 2, 5, -3, -10}, {-1, -9, -7, -6, -4, -6, 3, 5, -5, -5, -6, 7}, {-9, 9, -4, 7, -9, 1, -7, 2, 6, -8, -10, 6}, {0, -9, -2, 2, -9, 3, -2, -9, 2, 4, -6, 0}, {-5, 0, -2, 2, -8, 3, 3, -1, 8, 4, 5, -4}};
  QSMatrix<Float> mat_5(12, 12, pub_zero);
  for (int i = 0; i < 12; ++i)
    for (int j = 0; j < 12; ++j) {
      mat_5(i, j) = Float(mat_5_init[i][j], ALICE);
    }


  float mat_6_init[12][2] = {{-9, -3}, {-1, -9}, {-9, -10}, {0, -9}, {7, 9}, {1, 7}, {-5, -8}, {-6, -1}, {4, 9}, {8, -10}, {-8, -5}, {5, 2}};
  QSMatrix<Float> mat_6(12, 2, pub_zero);
  for (int i = 0; i < 12; ++i)
    for (int j = 0; j < 2; ++j) {
      mat_6(i, j) = Float(mat_6_init[i][j], ALICE);
    }


  cout << "defs complete\n";

  QSMatrix<Float> result_mat_7 = mat_1 * mat_2;
  QSMatrix<Float> result_mat_8 = relu(result_mat_7);

  QSMatrix<Float> result_mat_9 = result_mat_8 * mat_3;
  QSMatrix<Float> result_mat_10 = relu(result_mat_9);

  QSMatrix<Float> result_mat_11 = result_mat_10 * mat_4;
  QSMatrix<Float> result_mat_12 = relu(result_mat_11);

  QSMatrix<Float> result_mat_13 = result_mat_12 * mat_5;
  QSMatrix<Float> result_mat_14 = relu(result_mat_13);

  QSMatrix<Float> result_mat_15 = result_mat_14 * mat_6;
  int num_and_gates = CircuitExecution::circ_exec->num_and();
  cout << "Number of and gates executed: " << num_and_gates << "\n";
  finalize_zk_bool<BoolIO<NetIO>>();
  cout <<"done\n";
}



int main(int argc, char** argv) {
  parse_party_and_port(argv, &party, &port);
  BoolIO<NetIO>* ios[threads];
  for(int i = 0; i < threads; ++i)
    ios[i] = new BoolIO<NetIO>(new NetIO(party == ALICE?nullptr:"127.0.0.1",port), party==ALICE);

  test(ios, party);

  for(int i = 0; i < threads; ++i) {
    delete ios[i]->io;
    delete ios[i];
  }
  return 0;
}

