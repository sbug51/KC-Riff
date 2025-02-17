package llama

/*
#cgo CFLAGS: -std=c11
#cgo CXXFLAGS: -std=c++17
#cgo CPPFLAGS: -I${SRCDIR}/llama.cpp/include
#cgo CPPFLAGS: -I${SRCDIR}/llama.cpp/common
#cgo CPPFLAGS: -I${SRCDIR}/llama.cpp/examples/llava
#cgo CPPFLAGS: -I${SRCDIR}/llama.cpp/src
#cgo CPPFLAGS: -I${SRCDIR}/../ml/backend/ggml/ggml/include

#include <stdlib.h>
#include "ggml.h"
#include "llama.h"
#include "clip.h"
#include "llava.h"

#include "mllama.h"
#include "sampling_ext.h"
*/
import "C"

import (
	"errors"
	"fmt"
	"unsafe"
)

// BackendInit initializes the GPU backend
func BackendInit() {
	C.llama_backend_init()
}

// PrintSystemInfo prints system info for debugging
func PrintSystemInfo() string {
	return C.GoString(C.llama_print_system_info())
}

// Execute runs the Llama model execution
func Execute(args []string) error {
	if len(args) == 0 {
		return errors.New("no arguments provided")
	}
	fmt.Println("Executing Llama model with arguments:", args)
	// Simulate model execution
	return nil
}

// GetModelArch returns the architecture of the model file
func GetModelArch(modelPath string) (string, error) {
	mp := C.CString(modelPath)
	defer C.free(unsafe.Pointer(mp))

	gguf_ctx := C.gguf_init_from_file(mp, C.struct_gguf_init_params{no_alloc: true, ctx: (**C.struct_ggml_context)(C.NULL)})
	if gguf_ctx == nil {
		return "", errors.New("unable to load model file")
	}
	defer C.gguf_free(gguf_ctx)

	key := C.CString("general.architecture")
	defer C.free(unsafe.Pointer(key))
	arch_index := C.gguf_find_key(gguf_ctx, key)
	if int(arch_index) < 0 {
		return "", errors.New("unknown model architecture")
	}

	arch := C.gguf_get_val_str(gguf_ctx, arch_index)

	return C.GoString(arch), nil
}
