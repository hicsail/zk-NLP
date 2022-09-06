#include "emp-zk/emp-zk.h"
#include <iostream>
#include "emp-tool/emp-tool.h"
#include "ram-zk/zk-mem.h"
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
      Bit t = zero.less_equal(val);
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

Integer mux(Bit s, Integer a, Integer b) {
  return b.select(s, a);
}

// *************************************************************************

void test(BoolIO<NetIO> *ios[threads], int party) {
  setup_zk_bool<BoolIO<NetIO>>(ios, threads, party);

  cout << "!!\n";

  Float pub_zero = Float(0.0, PUBLIC);

  cout << "starting defs\n";

  static int list_1_init[] = {3, 4, 5, 3, 4, 5, 3, 4, 5, 1, 2, 0, 2, 1, 0, 0, 1, 2};
  ZKRAM<BoolIO<NetIO>> *list_1 = new ZKRAM<BoolIO<NetIO>>(party, index_sz, step_sz, val_sz);
  for (int i = 0; i < 18; ++i)
    list_1->write(Integer(index_sz, i, PUBLIC), Integer(32, list_1_init[i], ALICE));


  static int stack_2_init[] = {0, 1, 2};
  ZKRAM<BoolIO<NetIO>> *stack_2 = new ZKRAM<BoolIO<NetIO>>(party, index_sz, step_sz, val_sz);
  for (int i = 0; i < 3; ++i)
    stack_2->write(Integer(index_sz, i, PUBLIC), Integer(32, stack_2_init[i], ALICE));
  Integer stack_2_top = Integer(32, 2, ALICE);


  static int list_3_init[] = {-1, -1, -1};
  ZKRAM<BoolIO<NetIO>> *list_3 = new ZKRAM<BoolIO<NetIO>>(party, index_sz, step_sz, val_sz);
  for (int i = 0; i < 3; ++i)
    list_3->write(Integer(index_sz, i, PUBLIC), Integer(32, list_3_init[i], ALICE));


  static int list_4_init[] = {0, 0, 0};
  ZKRAM<BoolIO<NetIO>> *list_4 = new ZKRAM<BoolIO<NetIO>>(party, index_sz, step_sz, val_sz);
  for (int i = 0; i < 3; ++i)
    list_4->write(Integer(index_sz, i, PUBLIC), Integer(32, list_4_init[i], ALICE));


  cout << "defs complete\n";

  Integer stack_val_75 = stack_2->read(stack_2_top);
  stack_2_top = stack_2_top - Integer(32, 1, ALICE);
  Integer stack_val_5 = stack_val_75;

  // COMMENT: set w
  Integer listref_result_76 = list_4->read(stack_val_5);
  Integer list_val_6 = listref_result_76;
  Integer public_int_3 = Integer(32, 3, PUBLIC);

  Integer result_intval_77 = stack_val_5 * public_int_3;

  Integer result_intval_78 = result_intval_77 + list_val_6;

  Integer listref_result_79 = list_1->read(result_intval_78);
  Integer list_val_7 = listref_result_79;

  // COMMENT: next proposal
  Integer listref_result_80 = list_4->read(stack_val_5);
  Integer list_val_8 = listref_result_80;
  Integer public_int_1 = Integer(32, 1, PUBLIC);

  Integer result_intval_81 = list_val_8 + public_int_1;

  list_4->write(stack_val_5, result_intval_81);
  int log_val_82 = stack_val_5.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposer:: " << log_val_82 << "\n";
  int log_val_83 = list_val_7.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposes TO:: " << log_val_83 << "\n";

  // COMMENT: conditional branch 1
  Integer result_intval_84 = list_val_7 - public_int_3;

  Integer listref_result_85 = list_3->read(result_intval_84);
  Integer list_val_9 = listref_result_85;
  Integer result_intval_86 = list_val_7 - public_int_3;

  Integer listref_result_87 = list_3->read(result_intval_86);
  Integer list_val_10 = listref_result_87;
  Integer result_intval_88 = list_val_7 - public_int_3;

  Integer public_int_minus1 = Integer(32, -1, PUBLIC);

  Bit result_bitval_89 = list_val_9 == public_int_minus1;

  Integer result_int_90 = mux(result_bitval_89, stack_val_5, list_val_10);

  list_3->write(result_intval_88, result_int_90);

  // COMMENT: conditional branch 2
  Integer result_intval_91 = list_val_7 - public_int_3;

  Integer listref_result_92 = list_3->read(result_intval_91);
  Integer list_val_11 = listref_result_92;

  // COMMENT: first index
  Integer result_intval_93 = list_val_7 * public_int_3;

  Integer listidx_result_94 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_93 + idx);
    listidx_result_94 = mux(val == stack_val_5, idx, listidx_result_94);
  }
  Integer list_idx_12 = listidx_result_94;

  // COMMENT: second index
  Integer result_intval_95 = list_val_7 * public_int_3;

  Integer listidx_result_96 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_95 + idx);
    listidx_result_96 = mux(val == list_val_11, idx, listidx_result_96);
  }
  Integer list_idx_13 = listidx_result_96;

  // COMMENT: comparison
  Integer result_intval_97 = list_val_7 - public_int_3;

  Integer listref_result_98 = list_3->read(result_intval_97);
  Integer list_val_14 = listref_result_98;
  Bit result_bitval_99 = list_idx_12 < list_idx_13;

  Bit result_bitval_100 = list_val_9 == public_int_minus1;

  Bit result_bitval_101 = !result_bitval_100;

  Bit result_bitval_102 = result_bitval_99 & result_bitval_101;

  stack_2_top = mux(result_bitval_102, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_103 = mux(result_bitval_102, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_103, mux(result_bitval_102, list_val_14, stack_2->read(cond_addr_103)));
  Integer result_intval_104 = list_val_7 - public_int_3;

  Integer listref_result_105 = list_3->read(result_intval_104);
  Integer list_val_15 = listref_result_105;
  Integer result_intval_106 = list_val_7 - public_int_3;

  Bit result_bitval_107 = list_idx_12 < list_idx_13;

  Bit result_bitval_108 = list_val_9 == public_int_minus1;

  Bit result_bitval_109 = !result_bitval_108;

  Bit result_bitval_110 = result_bitval_107 & result_bitval_109;

  Integer result_int_111 = mux(result_bitval_110, stack_val_5, list_val_15);

  list_3->write(result_intval_106, result_int_111);

  // COMMENT: conditional branch 3 (else)
  Bit result_bitval_112 = list_val_9 == public_int_minus1;

  Bit result_bitval_113 = !result_bitval_112;

  Bit result_bitval_114 = list_idx_12 < list_idx_13;

  Bit result_bitval_115 = !result_bitval_114;

  Bit result_bitval_116 = result_bitval_113 & result_bitval_115;

  stack_2_top = mux(result_bitval_116, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_117 = mux(result_bitval_116, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_117, mux(result_bitval_116, stack_val_5, stack_2->read(cond_addr_117)));
  Integer stack_val_118 = stack_2->read(stack_2_top);
  stack_2_top = stack_2_top - Integer(32, 1, ALICE);
  Integer stack_val_16 = stack_val_118;

  // COMMENT: set w
  Integer listref_result_119 = list_4->read(stack_val_16);
  Integer list_val_17 = listref_result_119;
  Integer result_intval_120 = stack_val_16 * public_int_3;

  Integer result_intval_121 = result_intval_120 + list_val_17;

  Integer listref_result_122 = list_1->read(result_intval_121);
  Integer list_val_18 = listref_result_122;

  // COMMENT: next proposal
  Integer listref_result_123 = list_4->read(stack_val_16);
  Integer list_val_19 = listref_result_123;
  Integer result_intval_124 = list_val_19 + public_int_1;

  list_4->write(stack_val_16, result_intval_124);
  int log_val_125 = stack_val_16.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposer:: " << log_val_125 << "\n";
  int log_val_126 = list_val_18.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposes TO:: " << log_val_126 << "\n";

  // COMMENT: conditional branch 1
  Integer result_intval_127 = list_val_18 - public_int_3;

  Integer listref_result_128 = list_3->read(result_intval_127);
  Integer list_val_20 = listref_result_128;
  Integer result_intval_129 = list_val_18 - public_int_3;

  Integer listref_result_130 = list_3->read(result_intval_129);
  Integer list_val_21 = listref_result_130;
  Integer result_intval_131 = list_val_18 - public_int_3;

  Bit result_bitval_132 = list_val_20 == public_int_minus1;

  Integer result_int_133 = mux(result_bitval_132, stack_val_16, list_val_21);

  list_3->write(result_intval_131, result_int_133);

  // COMMENT: conditional branch 2
  Integer result_intval_134 = list_val_18 - public_int_3;

  Integer listref_result_135 = list_3->read(result_intval_134);
  Integer list_val_22 = listref_result_135;

  // COMMENT: first index
  Integer result_intval_136 = list_val_18 * public_int_3;

  Integer listidx_result_137 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_136 + idx);
    listidx_result_137 = mux(val == stack_val_16, idx, listidx_result_137);
  }
  Integer list_idx_23 = listidx_result_137;

  // COMMENT: second index
  Integer result_intval_138 = list_val_18 * public_int_3;

  Integer listidx_result_139 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_138 + idx);
    listidx_result_139 = mux(val == list_val_22, idx, listidx_result_139);
  }
  Integer list_idx_24 = listidx_result_139;

  // COMMENT: comparison
  Integer result_intval_140 = list_val_18 - public_int_3;

  Integer listref_result_141 = list_3->read(result_intval_140);
  Integer list_val_25 = listref_result_141;
  Bit result_bitval_142 = list_idx_23 < list_idx_24;

  Bit result_bitval_143 = list_val_20 == public_int_minus1;

  Bit result_bitval_144 = !result_bitval_143;

  Bit result_bitval_145 = result_bitval_142 & result_bitval_144;

  stack_2_top = mux(result_bitval_145, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_146 = mux(result_bitval_145, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_146, mux(result_bitval_145, list_val_25, stack_2->read(cond_addr_146)));
  Integer result_intval_147 = list_val_18 - public_int_3;

  Integer listref_result_148 = list_3->read(result_intval_147);
  Integer list_val_26 = listref_result_148;
  Integer result_intval_149 = list_val_18 - public_int_3;

  Bit result_bitval_150 = list_idx_23 < list_idx_24;

  Bit result_bitval_151 = list_val_20 == public_int_minus1;

  Bit result_bitval_152 = !result_bitval_151;

  Bit result_bitval_153 = result_bitval_150 & result_bitval_152;

  Integer result_int_154 = mux(result_bitval_153, stack_val_16, list_val_26);

  list_3->write(result_intval_149, result_int_154);

  // COMMENT: conditional branch 3 (else)
  Bit result_bitval_155 = list_val_20 == public_int_minus1;

  Bit result_bitval_156 = !result_bitval_155;

  Bit result_bitval_157 = list_idx_23 < list_idx_24;

  Bit result_bitval_158 = !result_bitval_157;

  Bit result_bitval_159 = result_bitval_156 & result_bitval_158;

  stack_2_top = mux(result_bitval_159, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_160 = mux(result_bitval_159, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_160, mux(result_bitval_159, stack_val_16, stack_2->read(cond_addr_160)));
  Integer stack_val_161 = stack_2->read(stack_2_top);
  stack_2_top = stack_2_top - Integer(32, 1, ALICE);
  Integer stack_val_27 = stack_val_161;

  // COMMENT: set w
  Integer listref_result_162 = list_4->read(stack_val_27);
  Integer list_val_28 = listref_result_162;
  Integer result_intval_163 = stack_val_27 * public_int_3;

  Integer result_intval_164 = result_intval_163 + list_val_28;

  Integer listref_result_165 = list_1->read(result_intval_164);
  Integer list_val_29 = listref_result_165;

  // COMMENT: next proposal
  Integer listref_result_166 = list_4->read(stack_val_27);
  Integer list_val_30 = listref_result_166;
  Integer result_intval_167 = list_val_30 + public_int_1;

  list_4->write(stack_val_27, result_intval_167);
  int log_val_168 = stack_val_27.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposer:: " << log_val_168 << "\n";
  int log_val_169 = list_val_29.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposes TO:: " << log_val_169 << "\n";

  // COMMENT: conditional branch 1
  Integer result_intval_170 = list_val_29 - public_int_3;

  Integer listref_result_171 = list_3->read(result_intval_170);
  Integer list_val_31 = listref_result_171;
  Integer result_intval_172 = list_val_29 - public_int_3;

  Integer listref_result_173 = list_3->read(result_intval_172);
  Integer list_val_32 = listref_result_173;
  Integer result_intval_174 = list_val_29 - public_int_3;

  Bit result_bitval_175 = list_val_31 == public_int_minus1;

  Integer result_int_176 = mux(result_bitval_175, stack_val_27, list_val_32);

  list_3->write(result_intval_174, result_int_176);

  // COMMENT: conditional branch 2
  Integer result_intval_177 = list_val_29 - public_int_3;

  Integer listref_result_178 = list_3->read(result_intval_177);
  Integer list_val_33 = listref_result_178;

  // COMMENT: first index
  Integer result_intval_179 = list_val_29 * public_int_3;

  Integer listidx_result_180 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_179 + idx);
    listidx_result_180 = mux(val == stack_val_27, idx, listidx_result_180);
  }
  Integer list_idx_34 = listidx_result_180;

  // COMMENT: second index
  Integer result_intval_181 = list_val_29 * public_int_3;

  Integer listidx_result_182 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_181 + idx);
    listidx_result_182 = mux(val == list_val_33, idx, listidx_result_182);
  }
  Integer list_idx_35 = listidx_result_182;

  // COMMENT: comparison
  Integer result_intval_183 = list_val_29 - public_int_3;

  Integer listref_result_184 = list_3->read(result_intval_183);
  Integer list_val_36 = listref_result_184;
  Bit result_bitval_185 = list_idx_34 < list_idx_35;

  Bit result_bitval_186 = list_val_31 == public_int_minus1;

  Bit result_bitval_187 = !result_bitval_186;

  Bit result_bitval_188 = result_bitval_185 & result_bitval_187;

  stack_2_top = mux(result_bitval_188, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_189 = mux(result_bitval_188, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_189, mux(result_bitval_188, list_val_36, stack_2->read(cond_addr_189)));
  Integer result_intval_190 = list_val_29 - public_int_3;

  Integer listref_result_191 = list_3->read(result_intval_190);
  Integer list_val_37 = listref_result_191;
  Integer result_intval_192 = list_val_29 - public_int_3;

  Bit result_bitval_193 = list_idx_34 < list_idx_35;

  Bit result_bitval_194 = list_val_31 == public_int_minus1;

  Bit result_bitval_195 = !result_bitval_194;

  Bit result_bitval_196 = result_bitval_193 & result_bitval_195;

  Integer result_int_197 = mux(result_bitval_196, stack_val_27, list_val_37);

  list_3->write(result_intval_192, result_int_197);

  // COMMENT: conditional branch 3 (else)
  Bit result_bitval_198 = list_val_31 == public_int_minus1;

  Bit result_bitval_199 = !result_bitval_198;

  Bit result_bitval_200 = list_idx_34 < list_idx_35;

  Bit result_bitval_201 = !result_bitval_200;

  Bit result_bitval_202 = result_bitval_199 & result_bitval_201;

  stack_2_top = mux(result_bitval_202, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_203 = mux(result_bitval_202, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_203, mux(result_bitval_202, stack_val_27, stack_2->read(cond_addr_203)));
  Integer stack_val_204 = stack_2->read(stack_2_top);
  stack_2_top = stack_2_top - Integer(32, 1, ALICE);
  Integer stack_val_38 = stack_val_204;

  // COMMENT: set w
  Integer listref_result_205 = list_4->read(stack_val_38);
  Integer list_val_39 = listref_result_205;
  Integer result_intval_206 = stack_val_38 * public_int_3;

  Integer result_intval_207 = result_intval_206 + list_val_39;

  Integer listref_result_208 = list_1->read(result_intval_207);
  Integer list_val_40 = listref_result_208;

  // COMMENT: next proposal
  Integer listref_result_209 = list_4->read(stack_val_38);
  Integer list_val_41 = listref_result_209;
  Integer result_intval_210 = list_val_41 + public_int_1;

  list_4->write(stack_val_38, result_intval_210);
  int log_val_211 = stack_val_38.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposer:: " << log_val_211 << "\n";
  int log_val_212 = list_val_40.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposes TO:: " << log_val_212 << "\n";

  // COMMENT: conditional branch 1
  Integer result_intval_213 = list_val_40 - public_int_3;

  Integer listref_result_214 = list_3->read(result_intval_213);
  Integer list_val_42 = listref_result_214;
  Integer result_intval_215 = list_val_40 - public_int_3;

  Integer listref_result_216 = list_3->read(result_intval_215);
  Integer list_val_43 = listref_result_216;
  Integer result_intval_217 = list_val_40 - public_int_3;

  Bit result_bitval_218 = list_val_42 == public_int_minus1;

  Integer result_int_219 = mux(result_bitval_218, stack_val_38, list_val_43);

  list_3->write(result_intval_217, result_int_219);

  // COMMENT: conditional branch 2
  Integer result_intval_220 = list_val_40 - public_int_3;

  Integer listref_result_221 = list_3->read(result_intval_220);
  Integer list_val_44 = listref_result_221;

  // COMMENT: first index
  Integer result_intval_222 = list_val_40 * public_int_3;

  Integer listidx_result_223 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_222 + idx);
    listidx_result_223 = mux(val == stack_val_38, idx, listidx_result_223);
  }
  Integer list_idx_45 = listidx_result_223;

  // COMMENT: second index
  Integer result_intval_224 = list_val_40 * public_int_3;

  Integer listidx_result_225 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_224 + idx);
    listidx_result_225 = mux(val == list_val_44, idx, listidx_result_225);
  }
  Integer list_idx_46 = listidx_result_225;

  // COMMENT: comparison
  Integer result_intval_226 = list_val_40 - public_int_3;

  Integer listref_result_227 = list_3->read(result_intval_226);
  Integer list_val_47 = listref_result_227;
  Bit result_bitval_228 = list_idx_45 < list_idx_46;

  Bit result_bitval_229 = list_val_42 == public_int_minus1;

  Bit result_bitval_230 = !result_bitval_229;

  Bit result_bitval_231 = result_bitval_228 & result_bitval_230;

  stack_2_top = mux(result_bitval_231, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_232 = mux(result_bitval_231, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_232, mux(result_bitval_231, list_val_47, stack_2->read(cond_addr_232)));
  Integer result_intval_233 = list_val_40 - public_int_3;

  Integer listref_result_234 = list_3->read(result_intval_233);
  Integer list_val_48 = listref_result_234;
  Integer result_intval_235 = list_val_40 - public_int_3;

  Bit result_bitval_236 = list_idx_45 < list_idx_46;

  Bit result_bitval_237 = list_val_42 == public_int_minus1;

  Bit result_bitval_238 = !result_bitval_237;

  Bit result_bitval_239 = result_bitval_236 & result_bitval_238;

  Integer result_int_240 = mux(result_bitval_239, stack_val_38, list_val_48);

  list_3->write(result_intval_235, result_int_240);

  // COMMENT: conditional branch 3 (else)
  Bit result_bitval_241 = list_val_42 == public_int_minus1;

  Bit result_bitval_242 = !result_bitval_241;

  Bit result_bitval_243 = list_idx_45 < list_idx_46;

  Bit result_bitval_244 = !result_bitval_243;

  Bit result_bitval_245 = result_bitval_242 & result_bitval_244;

  stack_2_top = mux(result_bitval_245, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_246 = mux(result_bitval_245, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_246, mux(result_bitval_245, stack_val_38, stack_2->read(cond_addr_246)));
  Integer stack_val_247 = stack_2->read(stack_2_top);
  stack_2_top = stack_2_top - Integer(32, 1, ALICE);
  Integer stack_val_49 = stack_val_247;

  // COMMENT: set w
  Integer listref_result_248 = list_4->read(stack_val_49);
  Integer list_val_50 = listref_result_248;
  Integer result_intval_249 = stack_val_49 * public_int_3;

  Integer result_intval_250 = result_intval_249 + list_val_50;

  Integer listref_result_251 = list_1->read(result_intval_250);
  Integer list_val_51 = listref_result_251;

  // COMMENT: next proposal
  Integer listref_result_252 = list_4->read(stack_val_49);
  Integer list_val_52 = listref_result_252;
  Integer result_intval_253 = list_val_52 + public_int_1;

  list_4->write(stack_val_49, result_intval_253);
  int log_val_254 = stack_val_49.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposer:: " << log_val_254 << "\n";
  int log_val_255 = list_val_51.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposes TO:: " << log_val_255 << "\n";

  // COMMENT: conditional branch 1
  Integer result_intval_256 = list_val_51 - public_int_3;

  Integer listref_result_257 = list_3->read(result_intval_256);
  Integer list_val_53 = listref_result_257;
  Integer result_intval_258 = list_val_51 - public_int_3;

  Integer listref_result_259 = list_3->read(result_intval_258);
  Integer list_val_54 = listref_result_259;
  Integer result_intval_260 = list_val_51 - public_int_3;

  Bit result_bitval_261 = list_val_53 == public_int_minus1;

  Integer result_int_262 = mux(result_bitval_261, stack_val_49, list_val_54);

  list_3->write(result_intval_260, result_int_262);

  // COMMENT: conditional branch 2
  Integer result_intval_263 = list_val_51 - public_int_3;

  Integer listref_result_264 = list_3->read(result_intval_263);
  Integer list_val_55 = listref_result_264;

  // COMMENT: first index
  Integer result_intval_265 = list_val_51 * public_int_3;

  Integer listidx_result_266 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_265 + idx);
    listidx_result_266 = mux(val == stack_val_49, idx, listidx_result_266);
  }
  Integer list_idx_56 = listidx_result_266;

  // COMMENT: second index
  Integer result_intval_267 = list_val_51 * public_int_3;

  Integer listidx_result_268 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_267 + idx);
    listidx_result_268 = mux(val == list_val_55, idx, listidx_result_268);
  }
  Integer list_idx_57 = listidx_result_268;

  // COMMENT: comparison
  Integer result_intval_269 = list_val_51 - public_int_3;

  Integer listref_result_270 = list_3->read(result_intval_269);
  Integer list_val_58 = listref_result_270;
  Bit result_bitval_271 = list_idx_56 < list_idx_57;

  Bit result_bitval_272 = list_val_53 == public_int_minus1;

  Bit result_bitval_273 = !result_bitval_272;

  Bit result_bitval_274 = result_bitval_271 & result_bitval_273;

  stack_2_top = mux(result_bitval_274, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_275 = mux(result_bitval_274, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_275, mux(result_bitval_274, list_val_58, stack_2->read(cond_addr_275)));
  Integer result_intval_276 = list_val_51 - public_int_3;

  Integer listref_result_277 = list_3->read(result_intval_276);
  Integer list_val_59 = listref_result_277;
  Integer result_intval_278 = list_val_51 - public_int_3;

  Bit result_bitval_279 = list_idx_56 < list_idx_57;

  Bit result_bitval_280 = list_val_53 == public_int_minus1;

  Bit result_bitval_281 = !result_bitval_280;

  Bit result_bitval_282 = result_bitval_279 & result_bitval_281;

  Integer result_int_283 = mux(result_bitval_282, stack_val_49, list_val_59);

  list_3->write(result_intval_278, result_int_283);

  // COMMENT: conditional branch 3 (else)
  Bit result_bitval_284 = list_val_53 == public_int_minus1;

  Bit result_bitval_285 = !result_bitval_284;

  Bit result_bitval_286 = list_idx_56 < list_idx_57;

  Bit result_bitval_287 = !result_bitval_286;

  Bit result_bitval_288 = result_bitval_285 & result_bitval_287;

  stack_2_top = mux(result_bitval_288, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_289 = mux(result_bitval_288, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_289, mux(result_bitval_288, stack_val_49, stack_2->read(cond_addr_289)));
  Integer stack_val_290 = stack_2->read(stack_2_top);
  stack_2_top = stack_2_top - Integer(32, 1, ALICE);
  Integer stack_val_60 = stack_val_290;

  // COMMENT: set w
  Integer listref_result_291 = list_4->read(stack_val_60);
  Integer list_val_61 = listref_result_291;
  Integer result_intval_292 = stack_val_60 * public_int_3;

  Integer result_intval_293 = result_intval_292 + list_val_61;

  Integer listref_result_294 = list_1->read(result_intval_293);
  Integer list_val_62 = listref_result_294;

  // COMMENT: next proposal
  Integer listref_result_295 = list_4->read(stack_val_60);
  Integer list_val_63 = listref_result_295;
  Integer result_intval_296 = list_val_63 + public_int_1;

  list_4->write(stack_val_60, result_intval_296);
  int log_val_297 = stack_val_60.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposer:: " << log_val_297 << "\n";
  int log_val_298 = list_val_62.reveal<int>(PUBLIC);
  cout << "P" << party << " NEW ROUND!!!! proposes TO:: " << log_val_298 << "\n";

  // COMMENT: conditional branch 1
  Integer result_intval_299 = list_val_62 - public_int_3;

  Integer listref_result_300 = list_3->read(result_intval_299);
  Integer list_val_64 = listref_result_300;
  Integer result_intval_301 = list_val_62 - public_int_3;

  Integer listref_result_302 = list_3->read(result_intval_301);
  Integer list_val_65 = listref_result_302;
  Integer result_intval_303 = list_val_62 - public_int_3;

  Bit result_bitval_304 = list_val_64 == public_int_minus1;

  Integer result_int_305 = mux(result_bitval_304, stack_val_60, list_val_65);

  list_3->write(result_intval_303, result_int_305);

  // COMMENT: conditional branch 2
  Integer result_intval_306 = list_val_62 - public_int_3;

  Integer listref_result_307 = list_3->read(result_intval_306);
  Integer list_val_66 = listref_result_307;

  // COMMENT: first index
  Integer result_intval_308 = list_val_62 * public_int_3;

  Integer listidx_result_309 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_308 + idx);
    listidx_result_309 = mux(val == stack_val_60, idx, listidx_result_309);
  }
  Integer list_idx_67 = listidx_result_309;

  // COMMENT: second index
  Integer result_intval_310 = list_val_62 * public_int_3;

  Integer listidx_result_311 = Integer(32, -1, PUBLIC);
  for (int i = 0; i < 3; i++) {
    Integer idx = Integer(32, i, PUBLIC);
    Integer val = list_1->read(result_intval_310 + idx);
    listidx_result_311 = mux(val == list_val_66, idx, listidx_result_311);
  }
  Integer list_idx_68 = listidx_result_311;

  // COMMENT: comparison
  Integer result_intval_312 = list_val_62 - public_int_3;

  Integer listref_result_313 = list_3->read(result_intval_312);
  Integer list_val_69 = listref_result_313;
  Bit result_bitval_314 = list_idx_67 < list_idx_68;

  Bit result_bitval_315 = list_val_64 == public_int_minus1;

  Bit result_bitval_316 = !result_bitval_315;

  Bit result_bitval_317 = result_bitval_314 & result_bitval_316;

  stack_2_top = mux(result_bitval_317, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_318 = mux(result_bitval_317, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_318, mux(result_bitval_317, list_val_69, stack_2->read(cond_addr_318)));
  Integer result_intval_319 = list_val_62 - public_int_3;

  Integer listref_result_320 = list_3->read(result_intval_319);
  Integer list_val_70 = listref_result_320;
  Integer result_intval_321 = list_val_62 - public_int_3;

  Bit result_bitval_322 = list_idx_67 < list_idx_68;

  Bit result_bitval_323 = list_val_64 == public_int_minus1;

  Bit result_bitval_324 = !result_bitval_323;

  Bit result_bitval_325 = result_bitval_322 & result_bitval_324;

  Integer result_int_326 = mux(result_bitval_325, stack_val_60, list_val_70);

  list_3->write(result_intval_321, result_int_326);

  // COMMENT: conditional branch 3 (else)
  Bit result_bitval_327 = list_val_64 == public_int_minus1;

  Bit result_bitval_328 = !result_bitval_327;

  Bit result_bitval_329 = list_idx_67 < list_idx_68;

  Bit result_bitval_330 = !result_bitval_329;

  Bit result_bitval_331 = result_bitval_328 & result_bitval_330;

  stack_2_top = mux(result_bitval_331, stack_2_top + Integer(32, 1, ALICE), stack_2_top);
  Integer cond_addr_332 = mux(result_bitval_331, stack_2_top, Integer(32, 0, ALICE));
  stack_2->write(cond_addr_332, mux(result_bitval_331, stack_val_60, stack_2->read(cond_addr_332)));
  Integer public_int_0 = Integer(32, 0, PUBLIC);

  Integer listref_result_333 = list_3->read(public_int_0);
  Integer list_val_71 = listref_result_333;
  int log_val_334 = list_val_71.reveal<int>(PUBLIC);
  cout << "P" << party << " marriage of woman 3: " << log_val_334 << "\n";
  Integer listref_result_335 = list_3->read(public_int_1);
  Integer list_val_72 = listref_result_335;
  int log_val_336 = list_val_72.reveal<int>(PUBLIC);
  cout << "P" << party << " marriage of woman 4: " << log_val_336 << "\n";
  Integer public_int_2 = Integer(32, 2, PUBLIC);

  Integer listref_result_337 = list_3->read(public_int_2);
  Integer list_val_73 = listref_result_337;
  int log_val_338 = list_val_73.reveal<int>(PUBLIC);
  cout << "P" << party << " marriage of woman 5: " << log_val_338 << "\n";
  Integer listref_result_339 = list_3->read(public_int_0);
  Integer list_val_74 = listref_result_339;
  int final_result = list_val_74.reveal<int>(PUBLIC);
  cout << "final result:" << final_result << "\n";

  list_1->check();
  list_3->check();
  list_4->check();
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

