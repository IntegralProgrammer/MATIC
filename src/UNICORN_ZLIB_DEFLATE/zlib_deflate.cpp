#include <string.h>
#include "zlib.h"

//Code borrowed from: https://gist.github.com/arq5x/5315739

//Compile with: g++ main.cpp -lz -o zlib-example
//or for static binary: g++ main.cpp -lz -static -o zlib-example
//to get entry point address: readelf -h zlib-example-static
//then to convert the static binary to a raw binary: objcopy -O binary zlib-example-static zlib-example-static.bin 

//Original Data
char a_original_buffer[50] = "Hello Hello Hello Hello Hello Hello!";

//Compressed Data
char b_compressed_buffer[50] = "Placeholder";

//Compressed Data Size
int compressed_size = 0;


int main(int argc, char* argv[])
{
	
	//printf("Uncompressed size is: %lu\n", strlen(a_original_buffer));
	
	z_stream defstream;
	defstream.zalloc = Z_NULL;
	defstream.zfree = Z_NULL;
	defstream.opaque = Z_NULL;
	//Setup "a" as the input and "b" as the compressed output
	defstream.avail_in = (uInt)strlen(a_original_buffer) + 1;
	defstream.next_in = (Bytef *)a_original_buffer; //input char array
	defstream.avail_out = (uInt)sizeof(b_compressed_buffer); //size of output
	defstream.next_out = (Bytef *)b_compressed_buffer; //Output char array
	
	//Run compression algorithm
	deflateInit(&defstream, Z_BEST_COMPRESSION);
	deflate(&defstream, Z_FINISH);
	deflateEnd(&defstream);
	
	compressed_size = defstream.total_out;
	
	//Print compressed output size
	//printf("Compressed size is %lu\n", defstream.total_out);
	printf("%s", b_compressed_buffer);
	
	return 0;
	
}
