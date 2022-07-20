#include "emp-zk/emp-zk.h"
#include "emp-zk/extensions/ram-zk/zk-mem.h"
#include <iostream>
#include "emp-tool/emp-tool.h"
#include "matrix.h"
using namespace emp;
using namespace std;

int port, party;
const int threads = 1;
const int index_sz = 20, step_sz = 25, val_sz = 32;

QSMatrix<Float> relu(const QSMatrix<Float>& mat) {
  unsigned rows = mat.get_rows();
  unsigned cols = mat.get_cols();

  QSMatrix<Float> result(rows, cols, 0.0);
  Float zero = Float(0.0, PUBLIC);

  for (unsigned i=0; i<rows; i++) {
    for (unsigned j=0; j<cols; j++) {
      Float val = mat(i, j);
      Bit t = val.less_equal(zero);
      result(i,j) = val.If(t, zero);
    }
  }

  return result;
}

QSMatrix<Float> log_softmax(const QSMatrix<Float>& mat) {
  unsigned rows = mat.get_rows();
  unsigned cols = mat.get_cols();

  QSMatrix<Float> result(rows, cols, 0.0);

  Float sum = Float(0.0, PUBLIC);
  for (unsigned i=0; i<rows; i++) {
    for (unsigned j=0; j<cols; j++) {
      sum = sum + mat(i, j).exp();
    }
  }

  for (unsigned i=0; i<rows; i++) {
    for (unsigned j=0; j<cols; j++) {
      result(i, j) = (mat(i, j).exp() / sum).ln();
    }
  }

  return result;
}

bool compare_qs_matrices(const QSMatrix<Float>& a, const QSMatrix<Float>& b) {
  if (a.get_rows() != b.get_rows()) return false;
  if (a.get_cols() != b.get_cols()) return false;

  for (unsigned i = 0; i < a.get_rows(); i++) {
    for (unsigned j = 0; j < a.get_cols(); j++) {
      if (a(i, j).reveal<double>(PUBLIC) - b(i, j).reveal<double>(PUBLIC) > .001) return false;
    }
  }
  return true;
}

bool compare_qs_matrices(const QSMatrix<float>& a, const QSMatrix<Float>& b) {
  if (a.get_rows() != b.get_rows()) return false;
  if (a.get_cols() != b.get_cols()) return false;

  for (unsigned i = 0; i < a.get_rows(); i++) {
    for (unsigned j = 0; j < a.get_cols(); j++) {
      if (a(i, j) - b(i, j).reveal<double>(PUBLIC) > .001) return false;
    }
  }
  return true;
}

bool compare_qs_matrices(const QSMatrix<Float>& a, const QSMatrix<float>& b) {
  if (a.get_rows() != b.get_rows()) return false;
  if (a.get_cols() != b.get_cols()) return false;

  for (unsigned i = 0; i < a.get_rows(); i++) {
    for (unsigned j = 0; j < a.get_cols(); j++) {
      if (a(i, j).reveal<double>(PUBLIC) - b(i, j) > .001) return false;
    }
  }
  return true;
}

bool compare_qs_matrices(const QSMatrix<float>& a, const QSMatrix<float>& b) {
  if (a.get_rows() != b.get_rows()) return false;
  if (a.get_cols() != b.get_cols()) return false;

  for (unsigned i = 0; i < a.get_rows(); i++) {
    for (unsigned j = 0; j < a.get_cols(); j++) {
      if (a(i, j) - b(i, j) > .001) return false;
    }
  }
  return true;
}

Integer mux(Bit s, Integer a, Integer b) {
  return b.select(s, a);
}

// *************************************************************************

void test(BoolIO<NetIO> *ios[threads], int party) {
  setup_zk_bool<BoolIO<NetIO>>(ios, threads, party);

  cout << "!!\n";

  Float pub_zero = Float(0.0, PUBLIC);
