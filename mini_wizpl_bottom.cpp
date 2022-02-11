  int num_and_gates = CircuitExecution::circ_exec->num_and();
  cout << "Number of and gates executed: " << num_and_gates << "\n";
  cout << "Number of ram reads: " << ram_reads << "\n";
  cout << "Number of ram writes: " << ram_writes << "\n";
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
