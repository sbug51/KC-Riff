package main

/*
#cgo LDFLAGS: -L F:/KillChaos/KC-Riff/ggml/build/bin/Debug -lggml
#cgo CFLAGS: -I F:/KillChaos/KC-Riff/ggml/include
#include <stdlib.h>
#include "ggml.h"
*/
import "C"

import "fmt"

func main() {
	fmt.Println("KC-Riff using GGML")

	// Manually allocate memory for GGML
	memSize := C.size_t(1024 * 1024) // 1MB memory buffer
	memBuffer := C.malloc(memSize)
	if memBuffer == nil {
		fmt.Println("Memory allocation failed")
		return
	}
	defer C.free(memBuffer)

	// Set up GGML initialization parameters
	params := C.struct_ggml_init_params{
		mem_size:   memSize,
		mem_buffer: memBuffer,
		no_alloc:   C.bool(false),
	}

	// Initialize GGML context
	ctx := C.ggml_init(params)
	if ctx == nil {
		fmt.Println("Failed to initialize GGML context")
		return
	}

	fmt.Println("GGML context initialized successfully")

	// Clean up GGML context
	C.ggml_free(ctx)
	fmt.Println("GGML context freed successfully")
}
