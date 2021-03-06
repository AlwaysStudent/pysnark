# Copyright (c) 2016-2018 Koninklijke Philips N.V. All rights reserved. A
# copyright license for redistribution and use in source and binary forms,
# with or without modification, is hereby granted for non-commercial,
# experimental and research purposes, provided that the following conditions
# are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimers.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimers in the
#   documentation and/or other materials provided with the distribution. If
#   you wish to use this software commercially, kindly contact
#   info.licensing@philips.com to obtain a commercial license.
#
# This license extends only to copyright and does not include or grant any
# patent license or other license whatsoever.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os

vc_p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
""" The modulus used in the verifiable computation. All computations are performed using modular arithmetic with this modulus. """

ignore_errors = False
""" If set to True, ValueErrors will not be raised. This allows, e.g., to
    build key material for a verification computation without knowing
    the witness"""

def do_pysnark():
    if "PYSNARK_ENABLED" in os.environ: return os.environ["PYSNARK_ENABLED"]=="1"
    return True

def do_rebuild():
    if "PYSNARK_REBUILD" in os.environ: return os.environ["PYSNARK_REBUILD"]=="1"

    return os.path.isfile(get_mskey_file()) or \
        (not os.path.isfile(get_mpkey_file()) and not os.path.isfile(get_mkey_file()))

def do_proof():
    if "PYSNARK_PROVE" in os.environ: return os.environ["PYSNARK_PROVE"]=="1"
    return True

datadir = os.environ["PYSNARK_KEYDIR"] if "PYSNARK_KEYDIR" in os.environ else ""
pdatadir = os.environ["PYSNARK_PROOFDIR"] if "PYSNARK_PROOFDIR" in os.environ else datadir

_ROOT = os.path.abspath(os.path.dirname(__file__))
qaptoolsdir = os.path.join(_ROOT, 'qaptools', '')
qaptoolsdir = os.environ["QAPTOOLS_BIN"] if "QAPTOOLS_BIN" in os.environ else qaptoolsdir

exefix = '.exe' if os.name == 'nt' else ''

def get_qaptool_exe(tool): return os.path.join(qaptoolsdir, tool+exefix)
def get_block_comm(bname): return os.path.join(datadir, "pysnark_comm_" + bname)
def get_block_file(bname): return os.path.join(datadir, "pysnark_wires_" + bname)
def get_cache_file(sz):    return os.path.join(datadir, "pysnark_coeffcache_" + str(sz))
def get_contract_dir():    return os.path.join(datadir, "contracts")
def get_conttest_dir():    return os.path.join(datadir, "test")
def get_ek_file(fn):       return os.path.join(datadir, "pysnark_ek_" + fn)
def get_eqs_file():        return os.path.join(datadir, "pysnark_eqs")
def get_eqs_file_fn(fn):   return os.path.join(datadir, "pysnark_eqs_" + fn)
def get_io_file():         return os.path.join(pdatadir, "pysnark_values")
def get_mkey_file():       return os.path.join(datadir, "pysnark_masterek")
def get_mpkey_file():      return os.path.join(datadir, "pysnark_masterpk")
def get_mskey_file():      return os.path.join(datadir, "pysnark_mastersk")
def get_proof_file():      return os.path.join(pdatadir, "pysnark_proof")
def get_schedule_file():   return os.path.join(datadir, "pysnark_schedule")
def get_vk_file(fn):       return os.path.join(datadir, "pysnark_vk_" + fn)
def get_wire_file():       return os.path.join(pdatadir, "pysnark_wires")