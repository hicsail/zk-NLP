#include "emp-zk/emp-zk.h"
#include <iostream>
#include "emp-tool/emp-tool.h"
#include "ram-zk/ro-zk-mem.h"
using namespace emp;
using namespace std;

int port, party;
const int threads = 1;
int ram_reads, ram_writes = 0;
const int index_sz = 20, val_sz = 32;

int memops_since_check = 0;


Integer conv(Bit x) {
  return Integer(32, 0, PUBLIC).select(x, Integer(32, 1, PUBLIC));
}

Integer conv(Integer x) {
  return Integer(x);
}


void matrix_set(Integer* Array, int Width, int X, int Y, Integer val){
  int index = (Width * Y) + X;
  Array[index] = val;
}

Integer matrix_get(Integer* Array, int Width, int X, int Y){
  int index = (Width * Y) + X;
  return Array[index];
}

void matrix_relu(Integer* in, int r1, int c1, Integer* out) {
  Integer zero = Integer(32, 0, PUBLIC);

  for(int i = 0; i < r1; ++i)
    for(int j = 0; j < c1; ++j)
      {
        Integer val = matrix_get(in, r1, i, j);
        matrix_set(out, r1, i, j,
                   val.select(val > zero, zero));
      }
}

void matrix_mult(Integer* m1, Integer* m2, int r1, int c1, int r2, int c2, Integer* out){
  for(int i = 0; i < r1; ++i)
    for(int j = 0; j < c2; ++j)
      {
        matrix_set(out, r1, i, j, Integer(32, 0, PUBLIC));
      }

  for(int i = 0; i < r1; ++i)
    for(int j = 0; j < c2; ++j)
      for(int k = 0; k < c1; ++k)
        {
          matrix_set(out, r1, i, j,
                     matrix_get(out, r1, i, j) +
                     (matrix_get(m1, r1, i, k) * matrix_get(m2, r2, k, j)));
        }
}

void matrix_plus(Integer* m1, Integer* m2, int r1, int c1, int r2, int c2, Integer* out){
  for(int i = 0; i < r1; ++i)
    for(int j = 0; j < c2; ++j)
      {
        matrix_set(out, r1, i, j, matrix_get(m1, r1, i, j) + matrix_get(m2, r2, i, j));
      }
}

void test(BoolIO<NetIO> *ios[threads], int party) {
  setup_zk_bool<BoolIO<NetIO>>(ios, threads, party);

  cout << "!!\n";
