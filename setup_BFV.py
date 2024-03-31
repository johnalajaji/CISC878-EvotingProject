import tenseal as ts  # to run this file make sure to install both tenseal and numpy


# Setup TenSEAL context
# Use CKKS homomorphic encryption algorithm
context = ts.context(
            ts.SCHEME_TYPE.BFV,
            poly_modulus_degree=8192,
            plain_modulus=1032193
        )

context.global_scale = 2**40

# Save private copy of context 
secret_context = context.copy()
secret_context = secret_context.serialize(save_secret_key=True)
secret_context = secret_context.hex()

file = open("privatekey_context_BFV","w")
file.write(secret_context)
file.close()

# Share public version of context with client (which doesn't contain private key)
client_context = context.copy()
client_context.make_context_public()
client_context = client_context.serialize()
client_context = client_context.hex()

file = open("publickey_context_BFV","w")
file.write(client_context)
file.close()