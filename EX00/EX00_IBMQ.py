# https://www.ibm.com/quantum?lnk=ProdC
# https://quantum.ibm.com/?src=ibm-quantum-homepage


from qiskit_ibm_runtime import QiskitRuntimeService
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TOKEN')

# single one
# service = QiskitRuntimeService(channel="ibm_quantum", token="")

# Save an IBM Quantum account and set it as your default account.
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token=token,
    set_as_default=True,
    # Use `overwrite=True` if you're updating your token.
    overwrite=True,
)

print("your account is ready to use")
# Load saved credentials