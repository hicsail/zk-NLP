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

