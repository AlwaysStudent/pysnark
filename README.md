# PySNARK

*(This is the original version of PySNARK. A rewrite with extra functionality is available [here](https://github.com/meilof/pysnark).)*

PySNARK is a Python-based system for easily performing verifiable computations based on the [Pinocchio](https://eprint.iacr.org/2013/279) zk-SNARK system and the [Geppetri](https://eprint.iacr.org/2017/013) extension for proofs on authenticated data. Verifiable computations can also be automatically turned into Solidity smart contracts for use on the Ethereum blockchain.

PySNARK may be used for non-commercial, experimental and research purposes; see `LICENSE.md` for details.

PySNARK is experimental and **not fit for production environment**. In particular, PySNARK does **not use cryptographically secure randomness**! See `base.cpp` and `modp.cpp` of `qaptools`.

## Installation

### Unix (Linux/MacOS/...)

First, download the PySNARK dependencies, `ate-pairing` and `xbyak`:

```
git submodule init
git submodule update
```

Build the `ate-pairing` library:

```
cd qaptools/ate-pairing
make SUPPORT_SNARK=1
```

Build the `qaptools` library:

```
cd ../..
cd qaptools
make
```

Build and install the `pysnark` library:

```
cd ..
python setup.py install
```

### Windows

PySNARK comes with precompiled Windows executables of `qaptools`, meaning it is possible to build an install PySNARK by just running

```
python setup.py install
```

To recompiling `qaptools` from source, set up a Unix-like build environment such as Mingw with MSYS and use the Unix instructions above.

### Using without installation

It is also possible to run PySNARK applications without installing PySNARK. For this, follow the above steps but run `python setup.py build` instead of `python setup.py install`. This makes sure all files are compiled and put in their correct locations. Then, run the application with the `PYTHONPATH` environment variable set to the PySNARK library, e.g.:

```
PYTHONPATH=/path/to/pysnark/sources python script.py
``` 

## The PySNARK toolchain

We discuss the usage of the PySNARK toolchain based on running one of the provided examples acting as each
of the different types of parties in a verifiable computation: trusted party, prover, or verifier.

### As trusted party

To try out running PySNARK as trusted party performing key generation, do the following:

```
cd examples
python cube.py 3
```

If PySNARK has been correctly installed, this will perform a verifiable computation that will compute the cube of the input value, `3`.
At the same time, it will generate all key material needed to verifiably perform the computation in the script.
(Performing an example computation is the only way to generate this key material.)
PySNARK produces the following files:

* Files that should be kept secret by the trusted party generating the key material:
    * `pysnark_mastersk`: zk-SNARK master secret key
* Files that the trusted party should distribute to provers along with the Python script (i.e., `cube.py` in this case):
    * `pysnark_schedule`: schedule of functions called in the computation
    * `pysnark_masterek`: master evaluation key
    * `pysnark_ek_main`: zk-SNARK evaluation
     key for the main function of the computation
    * `pysnark_eqs_main`: equations for the main function of the computation
* Files that the trusted party should distribute to verifiers:
    * `pysnark_schedule`: schedule of functions called in the computation
    * `pysnark_masterpk`: master public key
    * `pysnark_vk_main`: verificaiton key for the main function
* Files that the prover should distribute to verifiers:
    * `pysnark_proof`: proof that the particular computation was performed correctly
    * `pysnark_values`: input/output values of the computation
* Files that are not needed anymore after the execution:
    * `pysnark_eqs`: equations for the zk-SNARK
    * `pysnark_wires`: wire values of the computation
    
### As prover

To try out running PySNARK as a prover, put the files discussed above (i.e.,  `pysnark_schedule`, `pysnark_masterek`, `pysnark_ek_main`, and `pysnark_eqs_main`) together with `cube.py` in a directory and run the same command:

```
cd examples
python cube.py 3
```

This will perform a verifiable computation based on the previously generated key material.

### As verifier

To try out running PySNARK as a verifier, put the files discussed above (i.e.,  `pysnark_schedule`, `pysnark_masterpk` and `pysnark_vk_main` received from the trusted party, and `pysnark_proof` and `pysnark_values` received from the prover) in a folder and run

```
python -m pysnark.qaptools.runqapver
```

This will verify the computation proof with respect to the input/output values from the `pysnark_values` file, e.g,:

```
# PySNARK i/o
main/o_in: 21
main/o_out: 9261
```

In this case, we have verifiably computed the fact that the cube of 21 is 9261. See the `examples` folder for additional examples.


### Using commitments

PySNARK allows proofs to refer to committed data using [Geppetri](https://eprint.iacr.org/2017/013).
This has three applications:
 - it allows proofs to refer to external private inputs from parties other than the trusted third party;
 - it allows different verifiable computations to share secret data with each other; and
 - it allows to divide a verifiable computation into multiple subcomputations, each with their own evaluation and verification keys (but all based on the same master secret key)

All computations sharing committe data should use the same master secret key.
 
See `examples/testcomm.py` for examples.
 
#### External secret inputs
 
To commit to data, use `pysnark.qaptools.runqapinput`, e.g., to commit to values 1, 2, and 3 using a commitment named `test`, use:

```python -m pysnark.qaptools.runqapinput test 1 2 3```

Alternatively, use `pysnark.qaptools.runqapinput.gencomm` from a Python script.
Share `pysnark_wires_test` with any prover who wants to perform a computation with respect to this committed data, and `pysnark_comm_test` to any verifier. 

Import this data into the verifiable computation with 

```[one,two,three] = pysnark.runtime.importcomm("test")```

#### Sharing data between verifiable computations

In the first computation, do

```pysnark.runtime.exportcomm([Var(1),Var(2),Var(3)], "test")```

and share `pysnark_wires_test` and `pysnark_comm_test` with the other prover and the verifier, respectively.

In the second verifiable computation, do

```[one,two,three] = pysnark.runtime.importcomm("test")```

#### Sharing data between different parts of a verifiable computation

This is implicitly used whenever a function is called that is decorated with `@pysnark.runtime.subqap`.
When a particular functon is used multiple times in a verifiable computation, using `@pysnark.runtime.subqap` prevents the circuit for the function to be replicated, resulting in smaller key material (but slower verification). 

## Using PySNARK for smart contracts 

PySNARK supports the automatic generation of smart contracts that verify the correctness of the given zk-SNARK.
These smart contracts are written in Solidity and require support for the recent zkSNARK verification opcodes ([EIP 196](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-196.md), [EIP 197](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-197.md)) included in Ethereum Byzantium.
To test them out, install a development version of Truffle using [these instructions](https://github.com/trufflesuite/truffle/blob/develop/CONTRIBUTING.md).
This functionality is based on ideas from [ZoKrates](https://github.com/JacobEberhardt/ZoKrates).

Continuing the above example, suppose you have a verifiable computation proof as produced above (i.e., performing `runqapver` as described above works).
First run
```
truffle init
```
to initialise Truffle (to just see the Solidity code without installing Truffle, create two empty directories `contracts` and `test`).
Next, run 
```
python -m pysnark.contract
```
to generate smart contract `contracts/Pysnark.sol` to verify computations of the `cube.py` script (using library `contracts/Pairing.sol` that is also copied into the directory), and test script `test/TestPysnark.sol` that gives a test case for the contract based on the current I/O and proof.
Finally, run
```
truffle test
```
to run the test script and check that the given proof can indeed be verified in Solidity.

Note that `test/TestPysnark.sol` indeed contains the I/O from the computation:
```
pragma solidity ^0.4.2;

import "truffle/Assert.sol";
import "../contracts/Pysnark.sol";

contract TestPysnark {
    function testVerifies() public {
        Pysnark ps = new Pysnark();
        uint[] memory proof = new uint[](22);
        uint[] memory io = new uint[](2);
        proof[0] = ...;
        ...
        proof[21] = ...;
        io[0] = 21; // main/o_in
        io[1] = 9261; // main/o_out
        Assert.equal(ps.verify(proof, io), true, "Proof should verify");
    }
}
```

Smart contracts can also refer to commitments, e.g., as imported with the `pysnark.runtime.importcomm` API call. 
In this case, the commitment becomes an argument to the verification function (a six-valued integer array), and the test case shows how the commitment used in the present computation should be used as value for that argument, e.g.:

```
pragma solidity ^0.4.2;

import "truffle/Assert.sol";
import "../contracts/Pysnark.sol";

contract TestPysnark {
    function testVerifies() public {
        Pysnark ps = new Pysnark(); 
        uint[] memory pysnark_comm_test = new uint[](6);
        pysnark_comm_test[0] = ...;
        ...
        Assert.equal(ps.verify(proof, io, pysnark_comm_test), true, "Proof should verify");
    }
}
```

To get more detailed information about the gas usage of the smart contract, run with Ganache: start ``ganache-cli``; edit ``truffle.js`` to add a development network, e.g.:

```
module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*" // Match any network id
    }
  }
};
```
and finally, run ``truffle test --network development``.


### Documentation

To generate PySNARK's documentation, do:

```
cd docs
make html
```

Then, open `docs/_build/html/index.html`.

A compiled PDF of the documentation (generated with `make pdf`) is available as `docs/PySNARK.pdf` but this file may not always be up-to-date.

## Acknowledgements

This work is part of the [SODA](https://www.soda-project.eu/) project that has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 731583.
