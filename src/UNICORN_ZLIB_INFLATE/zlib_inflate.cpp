#include <string.h>
#include "zlib.h"

//Code borrowed from: https://gist.github.com/arq5x/5315739

//Compile with: g++ main.cpp -lz -o zlib-example
//or for static binary: g++ main.cpp -lz -static -o zlib-example
//to get entry point address: readelf -h zlib-example-static
//then to convert the static binary to a raw binary: objcopy -O binary zlib-example-static zlib-example-static.bin 

char compressed_input[50] = "Placeholder";
char uncompressed_output[50];

int main(int argc, char* argv[])
{
	
	//Use zlib to inflate
	z_stream infstream;
	infstream.zalloc = Z_NULL;
	infstream.zfree = Z_NULL;
	infstream.opaque = Z_NULL;
	
	infstream.avail_in = (uInt)strlen(compressed_input) + 1;
	infstream.next_in = (Bytef *)compressed_input;
	infstream.avail_out = (uInt)sizeof(uncompressed_output);
	infstream.next_out = (Bytef *)uncompressed_output;
	
	inflateInit(&infstream);
	inflate(&infstream, Z_NO_FLUSH);
	inflateEnd(&infstream);
	
	return 0;
}
