#include <stdio.h>
#include <string.h>
#include "tweetnacl.h"

//Compile with gcc sign_and_verify.c -lsodium -o S_AND_V

unsigned char pk[crypto_sign_PUBLICKEYBYTES] = {
  0x67, 0x6b, 0xbf, 0x80, 0x53, 0x08, 0x1d, 0xca, 0x14, 0xe5, 0x89, 0x23,
  0x43, 0x69, 0x85, 0x5e, 0xb9, 0xfc, 0x0e, 0xb6, 0x67, 0x75, 0xd7, 0xc4,
  0x07, 0xa2, 0x54, 0x99, 0x14, 0xb4, 0x29, 0xb0
};

unsigned char sk[crypto_sign_SECRETKEYBYTES] = {
  0xe0, 0x8f, 0x53, 0x7c, 0x08, 0x2b, 0x13, 0xdb, 0xcc, 0x39, 0xde, 0x58,
  0xcd, 0x3a, 0xb2, 0xfc, 0x8c, 0x2f, 0xb2, 0xcf, 0x59, 0x95, 0x19, 0x85,
  0x2f, 0x3f, 0x42, 0xa0, 0x6e, 0x58, 0xb8, 0x26, 0x67, 0x6b, 0xbf, 0x80,
  0x53, 0x08, 0x1d, 0xca, 0x14, 0xe5, 0x89, 0x23, 0x43, 0x69, 0x85, 0x5e,
  0xb9, 0xfc, 0x0e, 0xb6, 0x67, 0x75, 0xd7, 0xc4, 0x07, 0xa2, 0x54, 0x99,
  0x14, 0xb4, 0x29, 0xb0
};

unsigned char unprotected_msg[50] = "Hello, World3213!";


unsigned char unprotected_copy[50] = "Hello, World3213!";

unsigned long long mlen = 50;
unsigned long long new_mlen;
unsigned long long smlen; //Holds the length of the signed message
unsigned char protected_msg[50 + crypto_sign_BYTES]; //Maximum possible length is mlen+crypto_sign_BYTES

//Fuzz test ME!
unsigned char tampered_msg[50 + crypto_sign_BYTES]; //Maximum possible length is mlen+crypto_sign_BYTES

int verification_status = -1; //-1 if signature verification fails, 0 if signature verification is sucessful

int main(int argc, char **argv)
{
	//Generate a keypair
	//crypto_sign_keypair(pk, sk);
	
	//Debug message printing
	//printf("Public key is: %s\n", pk);
	//printf("Secret key is: %s\n", sk);
	//printf("\n");
	//printf("Our unprotected message is: %s\n", unprotected_msg);
	
	//Sign our message
	crypto_sign(protected_msg, &smlen, unprotected_msg, mlen, sk);
	
	//Debug message printing
	//printf("\n");
	//printf("Our signed message is: %s\n", protected_msg);
	
	//Copy protected_msg, then modify it
	memcpy(&tampered_msg, &protected_msg, sizeof(tampered_msg));
	//tampered_msg[3] = 'f';
	
	//Verify our message
	verification_status = crypto_sign_open(unprotected_copy, &new_mlen, tampered_msg, smlen, pk);
	
	//Debug message printing
	//printf("\n");
	//printf("crypto_sign_open has returned: %d\n", verification_status);
	
	//Let us know if this message is authentic or not
	//if (verification_status == 0)
	//{
		//printf("Message is legitimate\n");
	//}
	//else
	//{
		//printf("Message may be illegitimate\n");
	//}
	
	return 0;
}
