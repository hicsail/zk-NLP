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
